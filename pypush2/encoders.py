_TEMPO_ENCODER_NOTE = 10
_TEMPO_ENCODER_CC = 14

_SWING_ENCODER_NOTE = 9
_SWING_ENCODER_CC = 15

_DISPLAY_ENCODER_BASE_NOTE = 0
_DISPLAY_ENCODER_BASE_CC = 71
_DISPLAY_ENCODER_COUNT = 8

_MASTER_ENCODER_NOTE = 8
_MASTER_ENCODER_CC = 79

def note_is_encoder(note):
  """
  Returns true if the given note number corresponds to an encoder touched message.
  """
  return (note == _TEMPO_ENCODER_NOTE or
    note == _SWING_ENCODER_NOTE or
    (_DISPLAY_ENCODER_BASE_NOTE <= note and note < (_DISPLAY_ENCODER_BASE_NOTE + _DISPLAY_ENCODER_COUNT)) or
    note == _MASTER_ENCODER_NOTE
  )
