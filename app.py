from flask import Flask, request, send_file, render_template
import os
from visualization_star import create_audio_visualization as create_visualization
import uuid
import subprocess

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'private/temp_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    # Generate unique filename
    filename = str(uuid.uuid4())
    audio_path = os.path.join(UPLOAD_FOLDER, f"{filename}.wav")
    video_path = os.path.join(UPLOAD_FOLDER, f"{filename}.mp4")
    
    print(f"Processing file: {file.filename}")  # Debug
    print(f"Saving to: {audio_path}")          # Debug
    
    # Convert m4a to wav if needed
    if file.filename.endswith('.m4a'):
        temp_m4a = os.path.join(UPLOAD_FOLDER, f"{filename}.m4a")
        print(f"Converting {temp_m4a} to {audio_path}")  # Debug
        file.save(temp_m4a)
        subprocess.run(['ffmpeg', '-i', temp_m4a, audio_path], capture_output=True)
        os.remove(temp_m4a)
    else:
        file.save(audio_path)
    
    print(f"Creating visualization at: {video_path}")  # Debug
    create_visualization(audio_path, video_path)
    
    return {'video_id': filename}

@app.route('/download/<video_id>')
def download(video_id):
    video_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 