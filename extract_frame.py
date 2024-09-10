import cv2
import os

def extract_frames(video_path, output_folder, fps=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(frame_rate // fps)
    
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f'frame_{count:04d}.png')
            cv2.imwrite(frame_filename, frame)
        
        count += 1
    
    cap.release()

# Usage
extract_frames('path/to/your/video.mp4', 'frames', fps=1)
