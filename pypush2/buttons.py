from flufl.enum import Enum

class Buttons(Enum):
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

  1_32t = 43
  1_32 = 42
  1_16t = 41
  1_16 = 40
  1_8t = 39
  1_8 = 38
  1_4t = 37
  1_4 = 36

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
