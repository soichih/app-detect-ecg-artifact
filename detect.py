#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import json
import os

import mne
from mne import io
from mne.datasets import sample

with open('config.json') as config_json:
        config = json.load(config_json)
        fname = config['fif']
        ch_name = config['ch_name']

raw = io.read_raw_fif(fname)

event_id = 999
ecg_events, _, _ = mne.preprocessing.find_ecg_events(raw, event_id, ch_name)

# Read epochs
picks = mne.pick_types(raw.info, meg=False, eeg=False, stim=False, eog=False, include=[ch_name], exclude='bads')
tmin, tmax = -0.1, 0.1
raw.del_proj()
epochs = mne.Epochs(raw, ecg_events, event_id, tmin, tmax, picks=picks)
data = epochs.get_data()

print("Number of detected ECG artifacts : %d" % len(data))

plt.plot(1e3 * epochs.times, np.squeeze(data).T)
plt.xlabel('Times (ms)')
plt.ylabel('ECG')
#plt.show()
plt.savefig("ecg_artifacts.png")
