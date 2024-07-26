"""This code is licensed under the GPL-3.0 license
Written by masajinobe-ef
"""


def bpm_to_ms(bpm):
    one_beat_ms = 60000 / bpm
    note_durations = {
        '1/4': one_beat_ms,
        '1/8': one_beat_ms / 2,
        '1/16': one_beat_ms / 4,
        '1/32': one_beat_ms / 8,
        '1/64': one_beat_ms / 16,
    }
    return note_durations
