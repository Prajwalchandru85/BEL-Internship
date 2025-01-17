# Employee Registration System with AI-Powered Verification

A modern employee registration system that combines facial recognition, real-time liveness detection, and secure data storage. The system uses advanced AI models to ensure secure and authentic user registration.

## 🌟 Key Features

### 1. Employee Information Management
- Secure employee data collection
- Password protection
- Security question/answer system for account recovery
- JSON-based secure storage system


### 2. AI-Powered Verification System

#### Face Detection and Recognition
![changes_made](https://github.com/user-attachments/assets/b2d15b50-1b15-4db2-bc58-8a6a6e53c87c)

- Uses `face_recognition` library powered by dlib's CNN
- Automatic face detection in uploaded photos
- Real-time face matching with 99.38% accuracy
- Secure comparison between passport photo and live capture

#### Liveness Detection System
![python_zXByqakIhJ](https://github.com/user-attachments/assets/431a14da-9f80-4518-bcad-214104a1830e)

### 3. Json based storage system
![Code_gUTlrtvbfa](https://github.com/user-attachments/assets/b8ee84de-36e9-4b5a-a007-a00c570a56b8)

### 4.Compares clicked photo with the the passport size photo uploaded and lets the user register
![Code_F4Q5AqorHY](https://github.com/user-attachments/assets/2f4fc01e-3aa8-4176-8bf3-72557f943439)
![Code_U6vXL2qa4e](https://github.com/user-attachments/assets/19c894bc-809d-4f32-805e-bf3281038155)


   

The system implements a two-step verification process:
1. **Blink Detection**
   - Requires 3 natural blinks
   - Uses MediaPipe's face mesh for precise eye tracking
   - Real-time eye aspect ratio (EAR) calculation

2. **Nod detection**
   - Requires 2 natural head nods
   - Tracks 468 facial landmarks in real-time
   - Prevents photo and video spoofing attempts

## 🤖 AI Models Used

### 1. MediaPipe Face Mesh
- **Purpose**: Real-time facial landmark detection
- **Features**: 
  - Tracks 468 facial landmarks
  - 3D face mesh construction
  - Used for blink detection and nod detection 

### 2. dlib's CNN Face Detector
- **Purpose**: Face detection in photos
- **Features**:
  - Deep learning-based detection
  - High accuracy in varying conditions
  - Multi-scale face detection

### 3. Face Recognition Model
- **Purpose**: Face matching and verification
- **Features**:
  - 128-dimensional face encodings
  - State-of-the-art recognition accuracy
  - Robust to lighting variations

## 📋 Requirements

```plaintext
Python 3.8+
opencv-python
mediapipe
face_recognition
Pillow
numpy
tkinter (usually comes with Python)
```

## 🚀 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/employee-registration-system.git
cd employee-registration-system
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python registration_app.py
```

## 💡 How to Use

### 1. Employee Registration
![Code_9laXS3k7YQ](https://github.com/user-attachments/assets/183a9cef-2a8d-49ed-a649-a0afe91547d3)

- Fill in required employee information
- Create secure password
- Select and answer security question

### 2. Photo Upload
- Click "Upload Passport Photo"
- System automatically verifies face presence
- Preview option available

### 3. Liveness Verification
1. Click "Verify Live" to start
2. Follow on-screen instructions:
   - Complete 3 blinks
   - Perform 2 head nods
3. System captures best frame automatically
4. Verifies face match with passport photo

### 4. Registration Completion
- Review information
- Click "Register" to complete
- Data securely stored in JSON format

## 🔒 Security Features

1. **Anti-Spoofing Protection**
   - Multi-step liveness detection
   - Real-time movement verification
   - Face matching threshold validation

2. **Data Security**
   - Secure file handling
   - Error logging
   - Input validation

## 🛠️ Technical Details

### Liveness Detection Parameters
- Blink threshold: 0.25 (EAR value)
- Nod threshold: 0.02 (displacement value)
- Face match threshold: 0.6 (similarity score)
- Verification timeout: 60 seconds

### Frame Capture
- Resolution: 640x480
- Best frame selection algorithm
- Multiple frame buffering

## 📊 Performance

- Face Detection Accuracy: ~99%
- Liveness Detection Success Rate: ~95%
- Average Registration Time: < 2 minutes
- Face Matching Accuracy: > 99%

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
