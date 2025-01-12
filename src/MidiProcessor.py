import mido

class MidiProcessor:
    """Processes MIDI files and maps notes to timestamps and durations."""
    def __init__(self, midi_path, timestamps, video_manager):
        self.midi_file = mido.MidiFile(midi_path)
        self.timestamps = timestamps
        self.video_manager = video_manager
        self.note_to_timestamp = self._map_notes_to_timestamps()
        self.note_start_times = {}
        self.note_durations = {}
        self.clips = []

    def _map_notes_to_timestamps(self):
        """Maps MIDI note values to timestamps based on input timestamps."""
        note_to_timestamp = {}
        for idx, midi_value in enumerate(range(62, 62 + len(self.timestamps))):
            note_to_timestamp[midi_value] = self.timestamps[idx]
        return note_to_timestamp

    def _get_clip_for_midi_note(self, note):
        """Generates a subclip for a given MIDI note."""
        if note in self.note_to_timestamp and note in self.note_durations:
            start_time = self.note_to_timestamp[note]
            clip_duration = self.note_durations[note] *1000
            return self.video_manager.get_clip(start_time, clip_duration)
        return None

    def process_midi(self):
        """Processes the MIDI file to extract note durations and generate video clips."""
        for msg in self.midi_file.play():
            if not msg.is_meta:
                if msg.type == 'note_on' and msg.velocity > 0:
                    self.note_start_times[msg.note] = (
                        self.video_manager.video.reader.pos / self.video_manager.video.reader.fps +
                        msg.time / self.midi_file.ticks_per_beat * 60 / 120
                    )
                elif msg.type == 'note_off' and msg.note in self.note_start_times:
                    start_time = self.note_start_times.pop(msg.note)
                    duration = (
                        self.video_manager.video.reader.pos / self.video_manager.video.reader.fps +
                        msg.time / self.midi_file.ticks_per_beat * 60 / 120
                    ) - start_time
                    self.note_durations[msg.note] = duration
                    clip = self._get_clip_for_midi_note(msg.note)
                    if clip:
                        self.clips.append(clip)

    def get_clips(self):
        """Returns the generated video clips."""
        return self.clips
