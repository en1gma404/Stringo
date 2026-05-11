from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from basic_pitch.inference import predict
import tempfile, os, glob, subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

OPEN_STRINGS = {
    1: 64,  # e
    2: 59,  # B
    3: 55,  # G
    4: 50,  # D
    5: 45,  # A
    6: 40,  # E
}

def midi_to_tab_positions(midi_pitch):
    positions = []
    for string_num, open_note in OPEN_STRINGS.items():
        fret = midi_pitch - open_note
        if 0 <= fret <= 12:
            positions.append({"string": string_num, "fret": fret})
    return positions

def best_position(midi_pitch, prev_string=None):
    positions = midi_to_tab_positions(midi_pitch)
    if not positions:
        return None
    if prev_string is None:
        return positions[0]
    return min(positions, key=lambda p: abs(p["string"] - prev_string))

def notes_to_tabs(note_events):
    tabs = []
    prev_string = None
    for note in note_events:
        start_time, end_time, midi_pitch, confidence, _ = note
        if confidence < 0.3:
            continue
        if end_time - start_time < 0.05:
            continue
        if midi_pitch < 40 or midi_pitch > 88:
            continue
        pos = best_position(int(midi_pitch), prev_string)
        if pos:
            tabs.append({
                "time": round(float(start_time), 2),
                "string": int(pos["string"]),
                "fret": int(pos["fret"])
            })
            prev_string = pos["string"]
    return tabs

@app.get("/")
def index():
    return FileResponse("index.html")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    print(f"Получен файл: {file.filename}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    analyze_path = tmp_path  # по умолчанию — оригинал

    try:
        print("Разделяю дорожки через demucs...")
        subprocess.run([
            "python", "-m", "demucs",
            "--two-stems=guitar",
            "-o", "separated",
            tmp_path
        ], check=True)

        guitar_files = glob.glob("separated/**/*guitar*.wav", recursive=True)
        if guitar_files:
            analyze_path = guitar_files[0]
            print(f"Гитарная дорожка: {analyze_path}")
        else:
            print("Гитара не найдена, анализирую оригинал")

    except Exception as e:
        print(f"demucs недоступен, анализирую оригинал: {e}")

    print("Запускаю basic-pitch...")
    _, _, note_events = predict(analyze_path)

    os.unlink(tmp_path)

    print(f"basic-pitch нашёл нот: {len(note_events)}")
    tabs = notes_to_tabs(note_events)
    print(f"После фильтрации: {len(tabs)}")

    return {"tabs": tabs, "total_notes": len(tabs)}