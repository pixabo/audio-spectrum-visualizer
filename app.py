from flask import Flask, request, send_file, render_template
import os
from werkzeug.utils import secure_filename
import uuid
from visualization import create_audio_visualization  # your current script

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'temp_files'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_temp_files(session_id):
    """Remove temporary files after processing"""
    temp_audio = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_audio.*")
    temp_video = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_output.mp4")
    for file in [temp_audio, temp_video]:
        try:
            os.remove(file)
        except:
            pass

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
    
    if file and allowed_file(file.filename):
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        temp_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_audio.{filename.split('.')[-1]}")
        temp_video_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_output.mp4")
        
        file.save(temp_audio_path)
        
        try:
            # Create visualization
            create_audio_visualization(temp_audio_path, temp_video_path)
            
            # Send file to user
            response = send_file(
                temp_video_path,
                as_attachment=True,
                download_name=f"visualization_{filename}.mp4"
            )
            
            # Cleanup after sending
            @response.call_on_close
        except Exception as e:
            return f"Error creating visualization: {e}", 500
    
    return 'Processing complete', 200 