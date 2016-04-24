import flufl.enum

_TEMPO_ENCODER_NOTE = 10
_TEMPO_ENCODER_CC = 14

_SWING_ENCODER_NOTE = 9
_SWING_ENCODER_CC = 15

_DISPLAY_ENCODER_BASE_NOTE = 0
_DISPLAY_ENCODER_BASE_CC = 71
_DISPLAY_ENCODER_COUNT = 8

_MASTER_ENCODER_NOTE = 8
_MASTER_ENCODER_CC = 79

class EncoderAction(flufl.enum.IntEnum):
  down_fast = -2
  down = -1
  no_change = 0
  up = 1
  up_fast = 2

def convert_encoder_cc_value(value):
  if value > 64:
    return value - 128
  else:
    return value

def note_is_encoder(note):
  """
  Returns true if the given note number corresponds to an encoder touched message.
  """
  return (note == _TEMPO_ENCODER_NOTE or
    note == _SWING_ENCODER_NOTE or
    (_DISPLAY_ENCODER_BASE_NOTE <= note and note < (_DISPLAY_ENCODER_BASE_NOTE + _DISPLAY_ENCODER_COUNT)) or
    note == _MASTER_ENCODER_NOTE
  )

def note_is_display_encoder(note):
  """
  Returns true if the given note number corresponds to an encoder touched message for
  one of the encoders above the display
  """
  return (_DISPLAY_ENCODER_BASE_NOTE <= note and note < (_DISPLAY_ENCODER_BASE_NOTE + _DISPLAY_ENCODER_COUNT))

def cc_is_display_encoder(cc):
  """
  Returns true if the given note number corresponds to an encoder touched message for
  one of the encoders above the display
  """
  return (_DISPLAY_ENCODER_BASE_CC <= cc and cc < (_DISPLAY_ENCODER_BASE_CC + _DISPLAY_ENCODER_COUNT))

def get_encoder_number_from_cc(cc):
  return cc - _DISPLAY_ENCODER_BASE_CC
