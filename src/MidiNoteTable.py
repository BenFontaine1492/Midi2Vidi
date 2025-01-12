class MidiNoteTable:
    """Generates and manages the mapping of MIDI values to scientific pitch notation."""
    def __init__(self):
        self.note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.table = self._generate_table()

    def _generate_table(self):
        table = {}
        for midi_value in range(21, 109):  # Standard range for piano
            octave = (midi_value // 12) - 1
            note_name = self.note_names[midi_value % 12]
            table[f"{note_name}{octave}"] = midi_value
        return table