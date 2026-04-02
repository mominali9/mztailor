import cv2
import mediapipe as mp
import numpy as np

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def extract_measurements(image_bytes, height_cm):
    """
    Process image bytes using MediaPipe Pose to extract body landmarks.
    Estimates chest, waist, shoulder, and arm length based on the provided real-world height.
    """
    mp_pose = mp.solutions.pose
    
    # Convert image bytes to OpenCV format
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"error": "Invalid image format"}
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(img_rgb)
        
        if not results.pose_landmarks:
            return {"error": "Could not detect a full body in the image. Please ensure you are standing clearly in the frame."}
            
        landmarks = results.pose_landmarks.landmark
        
        # Determine if it's a half-body shot based on visibility of hips/heels
        left_heel = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
        right_heel = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value]
        
        is_half_body = (left_heel.visibility < 0.3 and right_heel.visibility < 0.3)
        
        y_top = landmarks[mp_pose.PoseLandmark.NOSE.value].y - 0.05
        
        if not is_half_body:
            y_bottom = max(left_heel.y, right_heel.y)
            pixel_height = y_bottom - y_top
            if pixel_height <= 0:
                pixel_height = 0.1
            cm_per_pixel_unit = float(height_cm) / pixel_height
        else:
            # It's a half body. People usually provide full height, but the image only shows torso.
            # A standard torso (shoulder to hip) is roughly 25% of the total body height
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            torso_pixel_height = calculate_distance(left_shoulder, left_hip)
            if torso_pixel_height <= 0:
                torso_pixel_height = 0.1
            # 25% of height is torso
            torso_cm = float(height_cm) * 0.25
            cm_per_pixel_unit = torso_cm / torso_pixel_height
            
        # 1. Shoulder width (Distance between Left and Right Shoulder)
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        shoulder_width_pixel = calculate_distance(left_shoulder, right_shoulder)
        # Multiply by a factor to account for true shoulder arc vs straight line
        shoulder_cm = round(shoulder_width_pixel * cm_per_pixel_unit * 1.1, 1)
        
        # 2. Chest (Approximate width around shoulders/chest area)
        chest_cm = round(shoulder_cm * 2.2, 1) # Simple approximation for perimeter
        
        # 3. Waist (Approximate width between hips)
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        if left_hip.visibility > 0.3 and right_hip.visibility > 0.3:
            waist_width_pixel = calculate_distance(left_hip, right_hip)
            waist_cm = round(waist_width_pixel * cm_per_pixel_unit * 2.5, 1) # Perimeter approx
        else:
            # If completely cut off before hips, estimate from chest
            waist_cm = round(chest_cm * 0.85, 1)
        
        # 4. Arm length (Shoulder to Wrist)
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        arm_length_pixel = calculate_distance(left_shoulder, left_wrist)
        arm_length_cm = round(arm_length_pixel * cm_per_pixel_unit, 1)
        
        # Basic Size Recommendation Logic
        size = "M"
        if chest_cm < 90:
            size = "S"
        elif chest_cm < 105:
            size = "M"
        elif chest_cm < 115:
            size = "L"
        else:
            size = "XL"
            
        return {
            "shoulder_cm": shoulder_cm,
            "chest_cm": chest_cm,
            "waist_cm": waist_cm,
            "arm_length_cm": arm_length_cm,
            "recommended_size": size
        }
