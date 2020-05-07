#! /usr/bin/python

# 2017/2/15
# Takahiro Shinozaki
# Tokyo Institute of Technology
# voicechanger.py (python 3.5)

import sys
import re
import wave
import numpy as np
import numpy.matlib
import math as mt
from scipy.fftpack import fft
import matplotlib.pyplot as plt

# check wav file specification
def wavInfoChk(wave, name):
    print(name + " # channels : " + str(wave.getnchannels()))
    print(name + " sampling   : " + str(wave.getframerate()) + " Hz")
    print(name + " samp width : " + str(wave.getsampwidth()) + " byte")
    print(name + " length     : " + str(wave.getnframes()))
    if wave.getnchannels() != 1 or wave.getframerate() != 16000 or wave.getsampwidth() != 2:
        print("ERROR: Input wav files must be Monaural/16kHz/16bit PCM", file=sys.stderr)
        sys.exit(1)
        

# form speech vectors
def splitwave(wav, wlen, shft):
  T   = mt.floor( (np.size(wav)-wlen)/shft + 1 );       # No. of output vectors
  wframes = np.zeros([T, wlen]);
  for t in range(0, T):
    wframes[t,:] = wav[t*shft : t*shft+wlen]*np.hanning(wlen) # hanning window
  return wframes

# form wave signal
def concatwframes(wframes, shft):
  [T, wlen] = np.shape(wframes)
  wavout = np.zeros([(T-1)*shft+wlen])
  for t in range(0, T):
    wavout[shft*t:shft*t+wlen] = wavout[shft*t:shft*t+wlen] + wframes[t, :]
  return wavout


# main function
if __name__ == "__main__":

    window = 256
    shift = 128
    N = 15

    if len(sys.argv) < 4:
        print("Usage: voicechanger soundS.wav soundF.wav out.wav", file=sys.stderr)
        print("Input wav files must be Monaural/16kHz/16bit PCM", file=sys.stderr)
        sys.exit(1)

    wavSFile = sys.argv[1] # wave file used as source
    wavFFile = sys.argv[2] # wave file used as filter
    wavOFile = sys.argv[3] # output file

    # get input wave data
    try:
        wave_s = wave.open(wavSFile, "r")
    except:
        print("ERROR: failed to open source wave file: " + wavSFile, file=sys.stderr)
        sys.exit(1)
    try:
        wave_f = wave.open(wavFFile, "r")
    except:
        print("ERROR: failed to open filter wave file: " + wavFFile, file=sys.stderr)
        sys.exit(1)
    wavInfoChk(wave_s, wavSFile + "(Source)")
    wavInfoChk(wave_f, wavFFile + "(Filter)")
    s = wave_s.readframes(wave_s.getnframes())
    s = np.frombuffer(s, dtype="int16")
    f = wave_f.readframes(wave_f.getnframes())
    f = np.frombuffer(f, dtype="int16")

    # truncate to the shorter one
    minlen = min(np.size(s), np.size(f))
    s = s[0:minlen]
    f = f[0:minlen]

    # form speech vectors
    wSframes = splitwave(s, window, shift)
    wFframes = splitwave(f, window, shift)

    # spectrum
    specS = np.fft.fft(wSframes)
    specF = np.fft.fft(wFframes)

    # amplitude spectrum and angle
    specSamp = np.abs(specS)
    specSang = np.angle(specS)
    specFamp = np.abs(specF)
    specFang = np.angle(specF)

    # cepstrum
    cepS = np.fft.ifft(np.log(specSamp))
    cepF = np.fft.ifft(np.log(specFamp))

    # get low cefrency elements from cepF, and hight from cepS
    cepY = np.zeros(np.shape(cepS), dtype="complex")
    cepY[:, (N+1):(window-N)] = cepS[:, (N+1):(window-N)]
    cepY[:, 0:N+1] = cepF[:, 0:N+1]
    cepY[:, window-N:window] = cepF[:, window-N:window]

#    cepF[:, (N+1):(window-N)] = 0
#    cepS[:, 0:(N+1)] = 0
#    cepS[:, window-N:window] = 0

    # convert back to magnitude spectrum
    specYamp = np.exp(np.real(np.fft.fft(cepY)))
#    specFamp2 = np.exp(np.real(np.fft.fft(cepF)))
#    specSamp2 = np.exp(np.real(np.fft.fft(cepS)))

#    plt.plot(specFamp2[10, :])
#    plt.show()
#    plt.plot(specSamp2[10, :])
#    plt.show()
#    plt.plot(specYamp[10, :])
#    plt.show()

    # convert back to wave
    specY = specYamp * np.exp(specSang*1j)
    wYframes = np.real(np.fft.ifft(specY))
    wavout = concatwframes(wYframes, shift).astype(dtype="int16")

    # write output wav file
    write_wave = wave.Wave_write(wavOFile)
    write_wave.setnchannels(1)
    write_wave.setsampwidth(2)
    write_wave.setframerate(16000)
    write_wave.setnframes(np.size(wavout))
    write_wave.writeframes(wavout)
    write_wave.close()

