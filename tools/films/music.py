"""The music bed for a case-study film, synthesised (numpy + scipy): no samples, no licence.
python3 music.py <managem|wastemart> <seconds> <out.wav>"""
import sys, wave, numpy as np
from scipy.signal import butter, sosfilt
film, DUR, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
sr = 44100; N = int(sr * DUR); L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(7)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def add(sig, t, amp=1.0, pan=0.0):
    i = int(t * sr); n = min(len(sig), N - i)
    if n > 0 and i >= 0: L[i:i+n] += sig[:n] * amp * np.sqrt((1 - pan) / 2); R[i:i+n] += sig[:n] * amp * np.sqrt((1 + pan) / 2)
def filt(x, lo=None, hi=None):
    sos = butter(2, [lo, hi], 'bandpass', fs=sr, output='sos') if lo and hi else butter(2, hi, 'lowpass', fs=sr, output='sos') if hi else butter(2, lo, 'highpass', fs=sr, output='sos')
    return sosfilt(sos, x)
def pluck(f, d=.6, bright=.4):
    t = np.arange(int(d * sr)) / sr
    return (np.sin(2*np.pi*f*t) * np.exp(-t*6) + bright * np.sin(2*np.pi*3*f*t) * np.exp(-t*16) + .15 * np.sin(2*np.pi*5*f*t) * np.exp(-t*30)) * np.minimum(1, t / .004)
def mute(f, d=.22):                      # a palm-muted string
    t = np.arange(int(d * sr)) / sr
    return filt(np.sign(np.sin(2*np.pi*f*t)) * np.exp(-t*22), None, 1400) * np.minimum(1, t / .003)
def pad(fs, d):
    t = np.arange(int(d * sr)) / sr; env = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.2)
    return filt(sum(np.sin(2*np.pi*f*t + k) + .5 * np.sin(2*np.pi*f*1.005*t) for k, f in enumerate(fs)), None, 1800) * env
def kick():
    t = np.arange(int(.28 * sr)) / sr; return np.sin(2*np.pi*(48 + 70*np.exp(-t*30))*t) * np.exp(-t*13)
def hat(d=.05):
    t = np.arange(int(d * sr)) / sr; return filt(rng.standard_normal(len(t)), 6500, None) * np.exp(-t*70)
def bell(f, d=2.2):
    t = np.arange(int(d * sr)) / sr; return sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*dd) for r, a, dd in ((1,1,2.4),(2,.4,4),(3.01,.2,6))) * np.minimum(1, t/.002)

if film == 'managem':                    # D major, 100 bpm: warm marimba arpeggios; the beat arrives with the product
    bpm, prog, lift, close = 100, [(62,66,69,73),(59,62,66,69),(55,59,62,66),(57,61,64,69)], 18.6, 52.2
else:                                    # A minor to C, 92 bpm: muted strings and a shaker, a working rhythm
    bpm, prog, lift, close = 92, [(57,60,64,67),(53,57,60,64),(48,52,55,60),(55,59,62,67)], 15.0, 51.4
b = 60 / bpm; bar = 4 * b; t = 0.0; i = 0
while t < DUR - 3.5:
    ch = prog[(i // 8) % 4]; step = i % 8; on = t >= lift; end = t >= close
    if step == 0: add(pad([hz(c - 12) for c in ch], bar + .4), t, .05 if not on else .035)
    if film == 'managem':
        note = ch[[0, 2, 1, 3, 2, 1, 3, 2][step]] + (12 if step in (3, 6) else 0)
        add(pluck(hz(note), .7), t, .16 if on else .10, (step % 3 - 1) * .4)
        if on and step in (0, 5): add(pluck(hz(ch[0] - 24), .9, .1), t, .22)
    else:
        note = ch[[0, 0, 2, 0, 1, 0, 3, 2][step]]
        add(mute(hz(note - 12)), t, .12 if on else .08, -.3); 
        if step in (2, 6): add(pluck(hz(ch[2] + 12), .5, .25), t, .09 if on else .05, .4)
        if on and step in (0, 3, 6): add(pluck(hz(ch[0] - 24), .7, .1), t, .22)
        add(hat(.03), t + b / 4, .035 if on else .02, .5)
    if on and not end:
        if step in (0, 4): add(kick(), t, .30)
        if step % 2 == 1: add(hat(), t, .05, .3)
    t += b / 2; i += 1
# the lift, and the close
tt = np.arange(int(1.4 * sr)) / sr; add(filt(rng.standard_normal(len(tt)), 400, 5000) * (tt / 1.4) ** 2, lift - 1.4, .09)
last = prog[0]; [add(bell(hz(c + 12)), DUR - 4.4 + k * .09, .10, (k - 1.5) * .3) for k, c in enumerate(last)]
mx = max(np.abs(L).max(), np.abs(R).max()); s = np.stack([L, R], 1) / mx * .8
f = int(.5 * sr); s[:f] *= np.linspace(0, 1, f)[:, None]; g = int(2.2 * sr); s[-g:] *= np.linspace(1, 0, g)[:, None]
w = wave.open(out, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((s * 32767).astype(np.int16).tobytes()); w.close()
