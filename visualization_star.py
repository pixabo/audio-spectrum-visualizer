import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import os
import time

def create_audio_visualization(audio_path, output_path):
    print(f"\nStarting visualization process...")
    start_time = time.time()
    
    # Set parameters - reduced for faster processing
    fps = 24  # Reduced from 30
    hop_length = 512  # Increase for faster processing
    n_fft = 2048  # Reduced window size
    
    try:
        # Load audio with reduced duration
        print(f"Loading audio file: {audio_path}")
        y, sr = librosa.load(audio_path, duration=60)  # Limit to 60 seconds
        print(f"Audio loaded: {len(y)} samples, {sr}Hz")
        
        # Calculate spectrogram with optimized parameters
        print("Calculating spectrogram...")
        D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        D_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        
        # Reduce spectrogram size
        D_db = D_db[::2, ::2]  # Downsample by factor of 2
        print(f"Spectrogram shape: {D_db.shape}")
        
        # Create figure with smaller size
        print("Creating matplotlib figure...")
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='black')
        ax.set_facecolor('black')
        
        img = ax.imshow(D_db, aspect='auto', origin='lower', 
                       cmap='magma', animated=True)
        plt.axis('off')
        
        def update(frame):
            data = np.roll(D_db, frame, axis=1)
            img.set_array(data)
            return [img]
        
        print(f"Creating animation...")
        anim = FuncAnimation(fig, update, frames=min(500, D_db.shape[1]), 
                           interval=1000/fps, blit=True)
        
        print(f"Saving animation to: {output_path}")
        anim.save(output_path, fps=fps, writer='ffmpeg', 
                 bitrate=2000)  # Reduced bitrate
        
        plt.close()
        
        end_time = time.time()
        print(f"Visualization complete! Time taken: {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        print(f"Error in visualization: {str(e)}")
        raise

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
