from VideoClipManager import VideoClipManager
from MidiProcessor import MidiProcessor

class MidiVideoGenerator:
    """Main class to coordinate the generation of a video from MIDI and video files."""
    def __init__(self, midi_path, video_path, timestamps, output_path):
        self.midi_path = midi_path
        self.video_path = video_path
        self.timestamps = timestamps
        self.output_path = output_path

    def generate_video(self):
        """Generates the final video from MIDI and video files."""
        video_manager = VideoClipManager(self.video_path)
        midi_processor = MidiProcessor(self.midi_path, self.timestamps, video_manager)
        midi_processor.process_midi()
        clips = midi_processor.get_clips()
        video_manager.concatenate_clips(clips, self.output_path)