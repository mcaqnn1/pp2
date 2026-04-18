"""
generate_tracks.py — creates short demo WAV tones in ./music/
Run once before launching the player:  python generate_tracks.py
"""

import os
import struct
import math

MUSIC_DIR = "music"

TRACKS = [
    ("track1_blues_riff.wav",   440.0,  3.0),   # A4
    ("track2_jazz_theme.wav",   523.25, 3.0),   # C5
    ("track3_rock_beat.wav",    349.23, 3.0),   # F4
    ("track4_classical.wav",    392.0,  3.0),   # G4
    ("track5_lofi_chill.wav",   293.66, 3.0),   # D4
]

SAMPLE_RATE = 44100


def make_wav(path: str, freq: float, duration: float):
    n_samples  = int(SAMPLE_RATE * duration)
    amplitude  = 16000
    channels   = 1
    bit_depth  = 16
    byte_rate  = SAMPLE_RATE * channels * bit_depth // 8
    block_align = channels * bit_depth // 8
    data_size  = n_samples * block_align

    with open(path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<IHHIIHH",
                            16,           
                            1,             
                            channels,
                            SAMPLE_RATE,
                            byte_rate,
                            block_align,
                            bit_depth))
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        for i in range(n_samples):
            t      = i / SAMPLE_RATE
            env    = min(t / 0.05, 1.0) * min((duration - t) / 0.1, 1.0)
            sample = int(amplitude * env * math.sin(2 * math.pi * freq * t))
            f.write(struct.pack("<h", sample))


if __name__ == "__main__":
    os.makedirs(MUSIC_DIR, exist_ok=True)
    for filename, freq, dur in TRACKS:
        path = os.path.join(MUSIC_DIR, filename)
        make_wav(path, freq, dur)
        print(f"  ✓  {filename}  ({freq:.2f} Hz, {dur}s)")
    print(f"\nDone — {len(TRACKS)} tracks saved to ./{MUSIC_DIR}/")
    print("Now run:  python main.py")