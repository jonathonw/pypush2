_PAD_GRID_MIN =36
_PAD_GRID_MAX = 99
_PAD_GRID_SIZE = 8 # Push 2 pad grid is square

def is_pad(note):
  """
  Returns True if note corresponds to one of the grid pads.
  """
  return _PAD_GRID_MIN <= note and note <= _PAD_GRID_MAX

def get_pad_xy_from_note(note):
  """
  Gets the (x, y) coordinate of the specified pad (referred to
  by note number).  (0,0) is the bottom left pad; (7,7) is the
  upper right.
  """
  if is_pad(note):
    padNumber = note - _PAD_GRID_MIN
    return (padNumber % _PAD_GRID_SIZE, padNumber / _PAD_GRID_SIZE)
  else:
    raise IndexError("Note {} does not correspond to a pad".format(note))

def get_pad_note_from_xy(coordinate):
  """
  Gets the pad number from the given (x, y) coordinate (passed as a tuple).
  """
  if (0 <= coordinate[0] and coordinate[0] < _PAD_GRID_SIZE and
      0 <= coordinate[1] and coordinate[1] < _PAD_GRID_SIZE):
    return coordinate[0] + coordinate[1] * _PAD_GRID_SIZE + _PAD_GRID_MIN
  else:
    raise IndexError("Location {} is not a valid location within the grid".format(coordinate))
