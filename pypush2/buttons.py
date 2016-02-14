import flufl.enum
import sets

BUTTON_PRESSED_VALUE = 127
BUTTON_RELEASED_VALUE = 0

class DisplayButtonGroups(flufl.enum.IntEnum):
  not_display_button = -1
  bottom = 0
  top = 1

def is_button(button):
  return button in Buttons

def is_display_button(button):
  """
  Returns true if the passedbutton is one of the buttons immediately
  above or below the Push 2's display.
  """
  return ((Buttons.top_display_0 <= button and button <= Buttons.top_display_7)
    or (Buttons.bottom_display_0 <= button and button <= Buttons.bottom_display_7))

def get_display_button_group(button):
  """
  Returns whether the passed button is above or below the display.
  Raises IndexError if the passed button is not a display button
  (i.e. is_display_button(button) returns false).
  """
  if Buttons.top_display_0 <= button and button <= Buttons.top_display_7:
    return DisplayButtonGroups.top
  elif Buttons.bottom_display_0 <= button and button <= Buttons.bottom_display_7:
    return DisplayButtonGroups.bottom
  else:
    raise IndexError("Button {} is not a display button".format(button))

def get_display_button_index(button):
  """
  Returns the index of the passed display button, with 0 referencing
  the leftmost button.  Raises IndexError if the passed button is not
  a display button (i.e. is_display_button(button) returns false).
  """
  if get_display_button_group(button) == DisplayButtonGroups.bottom:
    return button - Buttons.bottom_display_0
  elif get_display_button_group(button) == DisplayButtonGroups.top:
    return button - Buttons.top_display_0
  else:
    raise IndexError("Button {} is not a display button".format(button))

class Buttons(flufl.enum.IntEnum):
  # Left side
  tap_tempo = 3
  metronome = 9

  delete = 118
  undo = 119

  mute = 60
  solo = 61
  stop_clip = 29

  convert = 35
  double_loop = 117
  quantize = 116

  duplicate = 88
  new = 87

  fixed_length = 90
  automate = 89
  record = 86

  play = 85

  # Center (display buttons)
  # Above display
  top_display_0 = 102
  top_display_1 = 103
  top_display_2 = 104
  top_display_3 = 105
  top_display_4 = 106
  top_display_5 = 107
  top_display_6 = 108
  top_display_7 = 109

  # Below display
  bottom_display_0 = 20
  bottom_display_1 = 21
  bottom_display_2 = 22
  bottom_display_3 = 23
  bottom_display_4 = 24
  bottom_display_5 = 25
  bottom_display_6 = 26
  bottom_display_7 = 27

  # Right-side, sequence button column
  add_device = 52
  add_track = 53

  master = 28

  length_1_32t = 43
  length_1_32 = 42
  length_1_16t = 41
  length_1_16 = 40
  length_1_8t = 39
  length_1_8 = 38
  length_1_4t = 37
  length_1_4 = 36

  # Right-side control buttons
  setup = 30
  user = 59

  device = 110
  mix = 112
  browse = 111
  clip = 113

  up = 46
  left = 44
  right = 45
  down = 47

  repeat = 56
  accent = 57

  scale = 58
  layout = 31
  note = 50
  session = 51

  octave_up = 55
  page_left = 62
  page_right = 63
  octave_down = 54

  shift = 49
  select = 48

colored_buttons = sets.ImmutableSet([
  Buttons.mute,
  Buttons.solo,
  Buttons.stop_clip,
  Buttons.automate,
  Buttons.record,
  Buttons.play,
  Buttons.top_display_0,
  Buttons.top_display_1,
  Buttons.top_display_2,
  Buttons.top_display_3,
  Buttons.top_display_4,
  Buttons.top_display_5,
  Buttons.top_display_6,
  Buttons.top_display_7,
  Buttons.bottom_display_0,
  Buttons.bottom_display_1,
  Buttons.bottom_display_2,
  Buttons.bottom_display_3,
  Buttons.bottom_display_4,
  Buttons.bottom_display_5,
  Buttons.bottom_display_6,
  Buttons.bottom_display_7,
  Buttons.length_1_32t,
  Buttons.length_1_32,
  Buttons.length_1_16t,
  Buttons.length_1_16,
  Buttons.length_1_8t,
  Buttons.length_1_8,
  Buttons.length_1_4t,
  Buttons.length_1_4
])
'''
Set of buttons backed by RGB LEDs and capable of
displaying color.
'''
