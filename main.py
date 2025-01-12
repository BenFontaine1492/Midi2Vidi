import sys
import os

# Add src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Import the class
from src.MidiVideoGenerator import MidiVideoGenerator

if __name__ == "__main__":
    # Timestamps for the notes
    timestamps = [
        0.00, 4.70, 9.067, 12.86, 16.66, 20.23, 24.26, 27.46, 31.00, 34.86, 38.40,
        42.23, 46.36, 50.53, 54.80, 58.73, 63.00, 66.93, 70.30, 74.63, 78.26, 81.46,
        84.90, 87.60, 91.86, 94.83, 98.43, 103.50, 106.03, 109.30, 112.26, 115.80,
        118.70, 121.60, 124.36, 127.13, 130.03, 132.53, 135.23, 138.10, 140.83,
        143.33, 145.83, 148.70, 151.23, 153.73, 156.03, 158.46, 160.83, 163.10,
        165.43, 167.90, 170.23, 172.43, 174.76, 176.76
    ]

    # File paths
    midi_path = "./assets/fuchs.mid"
    video_path = "./assets/notes.mp4"
    output_path = "./output/video.mp4"

    # Generate the video
    print("generation started")
    generator = MidiVideoGenerator(midi_path, video_path, timestamps, output_path)
    generator.generate_video()
    print ("generation stopped/finished")