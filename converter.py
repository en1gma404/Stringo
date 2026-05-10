OPEN_STRINGS = {
    1: 64,
    2: 59,
    3: 55,
    4: 50,
    5: 45,
    6: 40
}

def midi_to_tab(midi_pitch):

    positions = []

    for string, open_note in OPEN_STRINGS.items():

        fret = midi_pitch - open_note

        if 0 <= fret <= 20:

            positions.append({
                "string": string,
                "fret": fret
            })

    return positions
