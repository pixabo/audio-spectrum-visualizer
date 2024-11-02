import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import os

def create_audio_visualization(audio_path, output_path):
    # Set parameters
    fps = 30
    
    # Load the audio file
    y, sr = librosa.load(audio_path)
    
    # Calculate the spectrogram
    D = librosa.stft(y)
    D_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
    ax.set_facecolor('black')
    
    # Initialize the visualization
    img = ax.imshow(D_db, aspect='auto', origin='lower', 
                   cmap='magma', animated=True)
    plt.colorbar(img, ax=ax)
    
    # Remove axes for cleaner look
    plt.axis('off')
    
    # Animation function
    def update(frame):
        # Rotate the data
        data = np.roll(D_db, frame, axis=1)
        img.set_array(data)
        return [img]
    
    # Create the animation
    frames = D_db.shape[1]  # Number of frames based on audio length
    anim = FuncAnimation(fig, update, frames=frames, 
                        interval=1000/fps, blit=True)
    
    # Save the animation
    anim.save(output_path, fps=fps, writer='ffmpeg')
    plt.close()

def main():
    print("\nWelcome to Audio Visualizer!")
    print("----------------------------")
    print("Supported formats: .wav, .mp3, .m4a")
    
    while True:
        audio_file = input("\nPlease enter the path to your audio file: ").strip()
        
        if not os.path.exists(audio_file):
            print("Error: File not found. Please check the path and try again.")
            continue
            
        valid_extensions = ['.wav', '.mp3', '.m4a']
        if not any(audio_file.lower().endswith(ext) for ext in valid_extensions):
            print(f"Error: File must be one of these types: {', '.join(valid_extensions)}")
            continue
            
        break
    
    output_file = 'visualization.mp4'
    print("\nProcessing... Please wait...")
    
    try:
        create_audio_visualization(audio_file, output_file)
        print(f"\nSuccess! Visualization saved as '{output_file}'")
    except Exception as e:
        print(f"\nError creating visualization: {str(e)}")

if __name__ == "__main__":
    main()
