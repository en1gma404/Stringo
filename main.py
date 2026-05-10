from basic_pitch.inference import predict
from converter import midi_to_tab

audio_path = "christy-moore-ride-on-official-live-video-christymoorevevo_w1IapaU8.mp3"

model_output, midi_data, note_events = predict(audio_path)

for note in note_events[:20]:

    midi_pitch = note[2]
    confidence = note[3]

    if confidence < 0.5:
        continue

    positions = midi_to_tab(midi_pitch)

    print(f"MIDI: {midi_pitch}")
    print(positions)
    print("------")
