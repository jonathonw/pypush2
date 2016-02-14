_PAD_GRID_MIN = 0
_PAD_GRID_MAX = 99

def is_pad(note):
  return _PAD_GRID_MIN <= note and note <= _PAD_GRID_MAX
