import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import face_recognition
import json
import time
import os
from tkinter import filedialog
import numpy as np

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Registration")
        self.root.geometry("800x900")
        self.root.configure(bg='#f0f0f0')
        
        
        self.name_var = tk.StringVar()
        self.emp_id_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.security_question_var = tk.StringVar()
        self.security_answer_var = tk.StringVar()
        self.passport_photo_path = None
        self.verification_complete = False
        
        # MediaPipe and Detection Variables
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.7)
        self.blinks = 0
        self.nods = 0
        self.blink_detected = False
        self.nod_detected = False
        self.nod_reset_time = 1.0
        self.nod_timer = time.time()
        self.blink_phase_completed = False
        self.nod_phase_started = False
        self.prev_nose_y = None
        self.captured_frames = []  # Buffer for smooth capture
        
        self.create_widgets()

    def create_widgets(self):
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # stydling
        style = ttk.Style()
        style.configure('Custom.TLabel', font=('Arial', 12))
        style.configure('Custom.TEntry', font=('Arial', 12))
        style.configure('Custom.TButton', font=('Arial', 12))
        
        # Form
        ttk.Label(main_frame, text="Employee Registration", font=('Arial', 16, 'bold')).pack(pady=10)
        
        
        ttk.Label(main_frame, text="Name:", style='Custom.TLabel').pack(pady=5)
        ttk.Entry(main_frame, textvariable=self.name_var, style='Custom.TEntry').pack(pady=5, fill=tk.X)
        
        
        ttk.Label(main_frame, text="Employee ID:", style='Custom.TLabel').pack(pady=5)
        ttk.Entry(main_frame, textvariable=self.emp_id_var, style='Custom.TEntry').pack(pady=5, fill=tk.X)
        
        
        ttk.Label(main_frame, text="Password:", style='Custom.TLabel').pack(pady=5)
        ttk.Entry(main_frame, textvariable=self.password_var, show="*", style='Custom.TEntry').pack(pady=5, fill=tk.X)
        
        ttk.Label(main_frame, text="Security Question:", style='Custom.TLabel').pack(pady=5)
        security_questions = [
            "What is your mother's maiden name?",
            "What was your first pet's name?",
            "What city were you born in?",
            "What was your first car?",
            "What is your favorite book?"
        ]
        question_combobox = ttk.Combobox(main_frame, textvariable=self.security_question_var, values=security_questions)
        question_combobox.pack(pady=5, fill=tk.X)
        
        
        ttk.Label(main_frame, text="Security Answer:", style='Custom.TLabel').pack(pady=5)
        ttk.Entry(main_frame, textvariable=self.security_answer_var, style='Custom.TEntry').pack(pady=5, fill=tk.X)
        
        #uploading photo button
        ttk.Button(main_frame, text="Upload Passport Photo", command=self.upload_photo, style='Custom.TButton').pack(pady=10)
        
        # photo preview button
        self.view_photo_button = ttk.Button(main_frame, text="View Uploaded Photo", command=self.view_photo, style='Custom.TButton', state='disabled')
        self.view_photo_button.pack(pady=10)
        
        
        self.verify_button = ttk.Button(main_frame, text="Verify Live", command=self.start_verification, style='Custom.TButton', state='disabled')
        self.verify_button.pack(pady=10)
        
        
        self.register_button = ttk.Button(main_frame, text="Register", command=self.register, style='Custom.TButton', state='disabled')
        self.register_button.pack(pady=10)

        self.status_label = ttk.Label(main_frame, text="", style='Custom.TLabel')
        self.status_label.pack(pady=10)

    def view_photo(self):
        if self.passport_photo_path:
            try:
                
                photo_window = tk.Toplevel(self.root)
                photo_window.title("Uploaded Passport Photo")
                
                
                img = Image.open(self.passport_photo_path)
                
                display_size = (300, 300)
                img.thumbnail(display_size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                
                # Create label and display image
                label = ttk.Label(photo_window, image=photo)
                label.image = photo  # Keep a reference
                label.pack(padx=10, pady=10)
                
                ttk.Button(photo_window, text="Close", command=photo_window.destroy).pack(pady=5)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error displaying image: {str(e)}")

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                # Verify the image can be loaded and must contain a face
                img = face_recognition.load_image_file(file_path)
                if len(face_recognition.face_locations(img)) > 0:
                    self.passport_photo_path = file_path
                    self.verify_button.config(state='normal')
                    self.view_photo_button.config(state='normal')  #if contains face thern only view button will be enabled 
                    self.status_label.config(text="Photo uploaded successfully!", foreground="green")
                else:
                    messagebox.showerror("Error", "No face detected in the uploaded photo!")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image: {str(e)}")

    def calculate_ear(self, landmarks, eye_indices):
        left = landmarks[eye_indices[0]]
        right = landmarks[eye_indices[3]]
        top1 = landmarks[eye_indices[1]]
        top2 = landmarks[eye_indices[2]]
        bottom1 = landmarks[eye_indices[5]]
        bottom2 = landmarks[eye_indices[4]]

        vertical_dist1 = ((top1.x - bottom1.x)**2 + (top1.y - bottom1.y)**2) ** 0.5
        vertical_dist2 = ((top2.x - bottom2.x)**2 + (top2.y - bottom2.y)**2) ** 0.5
        vertical_mean = (vertical_dist1 + vertical_dist2) / 2

        horizontal_dist = ((left.x - right.x)**2 + (left.y - right.y)**2) ** 0.5
        return vertical_mean / horizontal_dist

    def detect_blink(self, landmarks):
        left_eye_indices = [33, 160, 158, 133, 153, 144]
        right_eye_indices = [362, 385, 387, 263, 373, 380]

        left_ear = self.calculate_ear(landmarks, left_eye_indices)
        right_ear = self.calculate_ear(landmarks, right_eye_indices)
        
        ear = (left_ear + right_ear) / 2
        return ear < 0.25

    def detect_nod(self, landmarks, prev_nose_y, nod_threshold=0.02):
        current_nose_y = landmarks[1].y
        displacement = abs(current_nose_y - prev_nose_y) if prev_nose_y is not None else 0
        return displacement > nod_threshold, current_nose_y

    def capture_best_frame(self):
        if not self.captured_frames:
            return None
            
        best_frame = None
        best_score = -1
        
        for frame in self.captured_frames:
            try:
                face_locations = face_recognition.face_locations(frame)
                if face_locations:
                    top, right, bottom, left = face_locations[0]
                    face_size = (right - left) * (bottom - top)
                    center_score = abs((left + right) / 2 - frame.shape[1] / 2)
                    score = face_size - center_score
                    
                    if score > best_score:
                        best_score = score
                        best_frame = frame
            except:
                continue
                
        return best_frame if best_frame is not None else self.captured_frames[-1]

    def start_verification(self):
        
        self.blinks = 0
        self.nods = 0
        self.blink_phase_completed = False
        self.nod_phase_started = False
        self.prev_nose_y = None
        self.captured_frames = []
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        verification_start_time = time.time()
        success_frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark

                if not self.blink_phase_completed:
                    if self.detect_blink(landmarks):
                        if not self.blink_detected:
                            self.blinks += 1
                            self.blink_detected = True
                            print(f"Blink detected! ({self.blinks}/3)")
                        
                        if self.blinks >= 3:
                            self.blink_phase_completed = True
                            self.nod_phase_started = True
                            self.nods = 0
                    else:
                        self.blink_detected = False

                if self.nod_phase_started:
                    nod, self.prev_nose_y = self.detect_nod(landmarks, self.prev_nose_y)
                    if nod and (time.time() - self.nod_timer > self.nod_reset_time):
                        self.nods += 1
                        self.nod_timer = time.time()
                        print(f"Nod detected! ({self.nods}/2)")

                cv2.putText(frame, f"Blinks: {self.blinks}/3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Nods(Up to down): {self.nods}/2", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if self.blinks >= 3 and self.nods >= 2:
                    success_frame_count += 1
                    if success_frame_count >= 10:
                        self.captured_frames.append(rgb_frame)
                    
                    cv2.putText(frame, "Capturing photo...", (10, 110), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    if success_frame_count >= 20:
                        best_frame = self.capture_best_frame()
                        if best_frame is not None:
                            captured_photo_path = "captured_photo.jpg"
                            cv2.imwrite(captured_photo_path, cv2.cvtColor(best_frame, cv2.COLOR_RGB2BGR))
                            
                            if self.compare_faces(self.passport_photo_path, captured_photo_path):
                                self.verification_complete = True
                                self.status_label.config(text="Verification Successful!", foreground="green")
                                self.register_button.config(state='normal')
                            else:
                                self.status_label.config(text="Face Verification Failed!", foreground="red")
                            break

            cv2.imshow("Liveness Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if time.time() - verification_start_time > 60:
                messagebox.showwarning("Timeout", "Verification timed out. Please try again.")
                break

        cap.release()
        cv2.destroyAllWindows()

    def compare_faces(self, known_image_path, test_image_path):
        try:
            known_image = face_recognition.load_image_file(known_image_path)
            test_image = face_recognition.load_image_file(test_image_path)
            
            known_face_locations = face_recognition.face_locations(known_image)
            test_face_locations = face_recognition.face_locations(test_image)
            
            if not known_face_locations or not test_face_locations:
                return False
            
            known_encoding = face_recognition.face_encodings(known_image, known_face_locations)[0]
            test_encoding = face_recognition.face_encodings(test_image, test_face_locations)[0]
            
            distance = face_recognition.face_distance([known_encoding], test_encoding)[0]
            return distance < 0.6
            
        except Exception as e:
            print(f"Face comparison error: {e}")
            return False

    def register(self):
        if not self.verification_complete:
            messagebox.showerror("Error", "Please complete the verification first!")
            return
            
        data = {
            "name": self.name_var.get(),
            "employee_id": self.emp_id_var.get(),
            "password": self.password_var.get(),
            "security_question": self.security_question_var.get(),
            "security_answer": self.security_answer_var.get(),
            "passport_photo_path": self.passport_photo_path
        }
        try:
            with open('registrations.json', 'a+') as f:
                f.seek(0)
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
                
                if not isinstance(existing_data, list):
                    existing_data = []
                    
                existing_data.append(data)
                
                f.seek(0)
                f.truncate()
                json.dump(existing_data, f, indent=4)
                
            messagebox.showinfo("Success", "Registration Successful!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

def main():
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()