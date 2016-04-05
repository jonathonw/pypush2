import collections
import flufl.enum

ColorInfo = collections.namedtuple("ColorInfo", ["push_color_index", "rgb_color"])
'''
Describes a color in the Push default palette.  push_color_index is
the numeric value used to display the color on a Push pad or RGB button;
rgb_color is a three-element tuple containing an RGB equivalent to that color.
'''

PUSH_COLORS_DICT = {
  "bright_red": ColorInfo(127, (1.0, 0.0, 0.0)),
  "bright_green": ColorInfo(126, (0.0, 1.0, 0.0)),
  "bright_blue": ColorInfo(125, (0.0, 0.0, 1.0)),
  "white": ColorInfo(120, (1.0, 1.0, 1.0)),
  "black": ColorInfo(0, (0.0, 0.0, 0.0)),
  "dark_grey": ColorInfo(124, (0.25, 0.25, 0.25)),
  "grey": ColorInfo(123, (0.6, 0.6, 0.6)),
  "pink": ColorInfo(21, (1.0, 0.5, 0.5))
}
'''
Dict of colors names to ColorInfo tuples describing that color.
'''

PushColors = flufl.enum.IntEnum("PushColors", [(key, value.push_color_index) for (key, value) in PUSH_COLORS_DICT.iteritems()])
'''
Enumeration of colors--  same content as PUSH_COLORS_DICT, but allows lookup
of color by Push color index.
'''

def get_color_info_by_push_color_index(colorIndex):
  if colorIndex in PushColors:
    return PUSH_COLORS_DICT[PushColors[colorIndex].name]
  else:
    raise IndexError("Color {} is not a known color", colorIndex)
