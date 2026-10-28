import csv
import queue
import wave
from pathlib import Path

import sounddevice as sd

SAMPLE_RATE = 16000  # Azure ට ඕනේ 16kHz, mono, 16-bit WAV
ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "sentences.csv"
AUDIO_DIR = ROOT / "data" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def record_clip():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=SAMPLE_RATE, channels=1,
                           dtype="int16", callback=callback):
        input("   >>> පටිගත වෙමින්... කියලා ඉවර වුණාම Enter ඔබන්න ")

    chunks = []
    while not q.empty():
        chunks.append(q.get())
    return b"".join(chunks)


def save_wav(path, audio_bytes):
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)  # 16-bit
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio_bytes)


def main():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        out = AUDIO_DIR / f"{row['id']}.wav"
        print(f"\n[{row['id']}] ({row['language']}) {row['reference_text']}")
        if out.exists():
            ans = input("   මේක දැනටමත් පටිගත කරලා. නැවත කරන්න 'r', මඟ හරින්න Enter: ")
            if ans.strip().lower() != "r":
                continue
        cmd = input("   පටිගත කිරීම පටන් ගන්න Enter (මඟ හරින්න 's'): ")
        if cmd.strip().lower() == "s":
            continue
        save_wav(out, record_clip())
        print(f"   සුරැකුණා: {out.name}")

    print("\nඉවරයි.")


if __name__ == "__main__":
    main()