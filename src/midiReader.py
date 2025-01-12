import mido
from moviepy.editor import VideoFileClip, concatenate_videoclips

# MIDI note names in scientific pitch notation
note_names = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]

# Generate the table of MIDI values and corresponding notes
midi_note_table = {}
for midi_value in range(21, 109):  # Standard range for piano
    octave = (midi_value // 12) - 1
    note_name = note_names[midi_value % 12]
    note = f"{note_name}{octave}"
    midi_note_table[note] = midi_value

# Define the timestamps for notes beginning with D
timestamps = [
    0.00, 4.70, 9.067, 12.86, 16.66, 20.23, 24.26, 27.46, 31.00, 34.86, 38.40,
    42.23, 46.36, 50.53, 54.80, 58.73, 63.00, 66.93, 70.30, 74.63, 78.26, 81.46,
    84.90, 87.60, 91.86, 94.83, 98.43, 103.50, 106.03, 109.30, 112.26, 115.80,
    118.70, 121.60, 124.36, 127.13, 130.03, 132.53, 135.23, 138.10, 140.83,
    143.33, 145.83, 148.70, 151.23, 153.73, 156.03, 158.46, 160.83, 163.10,
    165.43, 167.90, 170.23, 172.43, 174.76, 176.76
]

# Load the video file
video = VideoFileClip("./assets/notes.mp4")

# Map the MIDI note values to the corresponding timestamps
note_to_timestamp = {}
for idx, midi_value in enumerate(range(62, 62 + len(timestamps))):  # MIDI note values for D3 to D#6
    note_to_timestamp[midi_value] = timestamps[idx]

# Track note start times and durations
note_start_times = {}
note_durations = {}

# Function to generate subclips for each note
def get_clip_for_midi_note(note):
    if note in note_to_timestamp and note in note_durations:
        start_time = note_to_timestamp[note]
        clip_duration = note_durations[note] *1000 # Use the actual note duration
        end_time = start_time + clip_duration
        return video.subclip(start_time, end_time)
    return None

# Read the MIDI file
midi_file = mido.MidiFile('./assets/fuchs.mid')

# List to hold the video clips
clips = []

# Iterate through the MIDI messages
for msg in midi_file.play():
    if not msg.is_meta:
        if msg.type == 'note_on' and msg.velocity > 0:
            note_start_times[msg.note] = video.reader.pos / video.reader.fps + msg.time / midi_file.ticks_per_beat * 60 / 120  # Convert ticks to seconds
        elif msg.type == 'note_off':
            if msg.note in note_start_times:
                start_time = note_start_times.pop(msg.note)
                duration = (video.reader.pos / video.reader.fps + msg.time / midi_file.ticks_per_beat * 60 / 120) - start_time
                note_durations[msg.note] = duration
                clip = get_clip_for_midi_note(msg.note)
                if clip:
                    clips.append(clip)

# Concatenate all the collected clips into one video
if clips:
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("./output/video.mp4")
