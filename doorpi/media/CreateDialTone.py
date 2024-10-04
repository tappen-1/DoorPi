#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Stolen from this source - thx to FB36:
# http://code.activestate.com/recipes/578168-sound-generator-using-wav-file/

def generate_dial_tone(filename='dialtone.wav', volume=50):
    # generate wav file containing sine waves
    # FB36 - 20120617
    import math, wave, array
    duration = 3  # seconds
    freq = 440  # frequency of the sine waves in Hz
    data = array.array('h')  # signed short integer (-32768 to 32767) data
    sample_rate = 44100  # of samples per second (standard)
    num_channels = 1  # of channels (1: mono, 2: stereo)
    data_size = 2  # 2 bytes because of using signed short integers => bit depth = 16
    num_samples_per_cycle = int(sample_rate / freq)
    num_samples = sample_rate * duration

    for i in range(num_samples // 2):
        sample = 32767 * float(volume) / 100
        sample *= math.sin(math.pi * 2 * (i % num_samples_per_cycle) / num_samples_per_cycle)
        data.append(int(sample))

    for i in range(num_samples // 2):
        sample = 0
        data.append(int(sample))

    with wave.open(filename, 'w') as f:
        f.setparams((num_channels, data_size, sample_rate, num_samples, "NONE", "Uncompressed"))
        f.writeframes(data.tobytes())

    return filename
