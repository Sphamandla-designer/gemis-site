"""Re-voice single sentences inside a narration: python3 splice.py
Each (film, slot start, slot end, patch start, patch end) replaces that slot of the
film's voiceover with the patch sentence, tempo-fitted (within 0.87–1.15) and centred."""
import subprocess, wave, numpy as np, os
SR = 44100
def load(p):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', p, '-ar', str(SR), '-ac', '1', '_t.wav'], check=True)
    w = wave.open('_t.wav'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; w.close(); return a
def save(p, a):
    w = wave.open(p, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
def tempo(a, k):
    save('_a.wav', a); subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '_a.wav', '-af', f'atempo={k:.4f}', '_b.wav'], check=True); return load('_b.wav')
def rms(a): return float(np.sqrt(np.mean(a * a)) + 1e-9)
patch = load('a/gemis-patch.mp3')
P = [(0, 2.03), (2.58, 3.89), (4.33, 7.73), (8.25, 13.43), (13.88, 16.46), (17.00, 22.04), (22.47, 24.83), (25.20, 29.59), (29.99, 33.24), (33.72, 37.91), (38.29, 42.31), (42.73, 44.27)]
JOBS = {'managem': [(10.86, 13.71, 0), (54.57, 55.85, 1)], 'wastemart': [(14.44, 18.09, 2)],
        'sbs': [(4.70, 9.57, 3), (17.66, 19.81, 4), (57.52, 63.71, 5)], 'homeassist': [(11.75, 14.10, 6), (57.26, 61.61, 7)],
        'transhex': [(5.80, 9.35, 8), (25.46, 29.59, 9), (40.54, 45.19, 10), (72.96, 74.90, 11)]}
for film, jobs in JOBS.items():
    v = load(f'orig-vo/{film}-vo.mp3'); out = v.copy()
    for a, b, i in jobs:
        a0, b0 = int((a - .06) * SR), min(len(v), int((b + .10) * SR))          # the slot, with a little of the pauses around it
        seg = patch[int((P[i][0] - .03) * SR if P[i][0] else 0):int((P[i][1] + .08) * SR)]
        slot = b0 - a0; k = min(1.15, max(0.87, len(seg) / slot)); seg = tempo(seg, k) if abs(k - 1) > .02 else seg
        seg = seg * (rms(v[a0:b0]) / rms(seg))                                   # the same level as the line it replaces
        f = int(.012 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        room = slot + (int(.28 * SR) if b0 < len(v) else int(1.5 * SR))           # it may run into the pause that follows
        seg = seg[:room]; out[a0:b0] = 0
        start = a0 + max(0, (slot - len(seg)) // 3)
        end = start + len(seg)
        if end > len(out): out = np.concatenate([out, np.zeros(end - len(out), np.float32)])
        out[start:end] = seg
        print(f'{film}: slot {a:.2f}–{b:.2f} ({b - a:.2f}s) ← patch {i + 1} ({(P[i][1] - P[i][0]):.2f}s) tempo {k:.2f} placed {start / SR:.2f}–{end / SR:.2f}')
    save(f'{film}-vo.wav', out)
for t in ('_t.wav', '_a.wav', '_b.wav'):
    if os.path.exists(t): os.remove(t)
