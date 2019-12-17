#!/usr/bin/env python

import matplotlib.pyplot as plt
import json

import mne
from mne import io

with open('config.json') as config_json:
    config = json.load(config_json)
    fname = config['fif']
    ch_type = config['ch_type']

raw = io.read_raw_fif(fname)

event_id = 999
ecg_events, _, _ = mne.preprocessing.find_ecg_events(raw, event_id)

# Read epochs
tmin, tmax = -0.1, 0.1
raw.del_proj()
epochs = mne.Epochs(raw, ecg_events, event_id, tmin, tmax, picks=(ch_type,))
evoked = epochs.get_data()

print("Number of detected ECG artifacts : %d" % len(epochs))

evoked.plot(show=False)
plt.savefig("ecg_artifacts.png")
