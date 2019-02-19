"""
sine.py

Generates a sine wave and saves it n WAVE file format.

Author: Mahesh Venkitachalam
"""

import numpy as np
import wave

sRate = 44100
nSamples = sRate * 5
x = np.arange(nSamples)/float(sRate)
vals = np.sin(2.0*np.pi*146.83*x)
data = np.array(vals * 32767, 'int16').tostring()
with wave.open('sine146_83.wav', 'wb') as file:
    file.setparams((1, 2, sRate, nSamples, 'NONE', 'uncompressed'))
    file.writeframes(data)
