import collections
import flufl.enum

ColorInfo = collections.namedtuple("ColorInfo", ["push_color_index", "rgb_color"])
'''
Describes a color in the Push default palette.  push_color_index is
the numeric value used to display the color on a Push pad or RGB button;
rgb_color is a three-element tuple containing an RGB equivalent to that color.
'''

PUSH_COLORS_DICT = {
  "black": ColorInfo(0, (0.0, 0.0, 0.0)), # #000000
  "scarlet": ColorInfo(1, (0.949019607843, 0.113725490196, 0.0)), # #f21d00
  "coral": ColorInfo(2, (0.980392156863, 0.470588235294, 0.321568627451)), # #fa7852
  "tangerine": ColorInfo(3, (0.901960784314, 0.541176470588, 0.0)), # #e68a00
  "muesli": ColorInfo(4, (0.650980392157, 0.537254901961, 0.337254901961)), # #a68956
  "canary": ColorInfo(5, (0.929411764706, 0.976470588235, 0.352941176471)), # #edf95a
  "supernova": ColorInfo(6, (1.0, 0.811764705882, 0.043137254902)), # #ffcf0b
  "electric_lime": ColorInfo(7, (0.776470588235, 1.0, 0.0)), # #c6ff00
  "limeade": ColorInfo(8, (0.290196078431, 0.749019607843, 0.0)), # #4abf00
  "lima": ColorInfo(9, (0.337254901961, 0.749019607843, 0.0745098039216)), # #56bf13
  "camarone": ColorInfo(10, (0.0, 0.419607843137, 0.0)), # #006b00
  "dup_green": ColorInfo(11, (0.0980392156863, 1.0, 0.188235294118)), # #19ff30
  "emerald": ColorInfo(12, (0.0901960784314, 0.650980392157, 0.501960784314)), # #17a680
  "deep_sea": ColorInfo(13, (0.0, 0.549019607843, 0.372549019608)), # #008c5f
  "cyan_/_aqua": ColorInfo(14, (0.152941176471, 1.0, 1.0)), # #27ffff
  "azure_radiance": ColorInfo(15, (0.0, 0.454901960784, 0.988235294118)), # #0074fc
  "absolute_zero": ColorInfo(16, (0.0, 0.309803921569, 0.8)), # #004fcc
  "congress_blue": ColorInfo(17, (0.0, 0.290196078431, 0.6)), # #004a99
  "purple_heart": ColorInfo(18, (0.392156862745, 0.290196078431, 0.850980392157)), # #644ad9
  "blueberry": ColorInfo(19, (0.36862745098, 0.270588235294, 1.0)), # #5e45ff
  "electric_violet": ColorInfo(20, (0.529411764706, 0.0, 1.0)), # #8700ff
  "lavender_magenta": ColorInfo(21, (0.901960784314, 0.341176470588, 0.890196078431)), # #e657e3
  "purple": ColorInfo(22, (0.4, 0.0, 0.6)), # #660099
  "hollywood_cerise": ColorInfo(23, (1.0, 0.0, 0.6)), # #ff0099
  "cadillac": ColorInfo(24, (0.63137254902, 0.298039215686, 0.372549019608)), # #a14c5f
  "razzle_dazzle_rose": ColorInfo(25, (1.0, 0.301960784314, 0.76862745098)), # #ff4dc4
  "dup_lavender_magenta": ColorInfo(26, (0.921568627451, 0.545098039216, 0.882352941176)), # #eb8be1
  "roof_terracotta": ColorInfo(27, (0.650980392157, 0.203921568627, 0.129411764706)), # #a63421
  "paarl": ColorInfo(28, (0.6, 0.337254901961, 0.156862745098)), # #995628
  "olive": ColorInfo(29, (0.529411764706, 0.403921568627, 0.0)), # #876700
  "hacienda": ColorInfo(30, (0.564705882353, 0.509803921569, 0.121568627451)), # #90821f
  "dup_limeade": ColorInfo(31, (0.290196078431, 0.529411764706, 0.0)), # #4a8700
  "dup_camarone": ColorInfo(32, (0.0, 0.498039215686, 0.0705882352941)), # #007f12
  "tory_blue": ColorInfo(33, (0.0941176470588, 0.325490196078, 0.698039215686)), # #1853b2
  "studio": ColorInfo(34, (0.38431372549, 0.294117647059, 0.678431372549)), # #624bad
  "cosmic": ColorInfo(35, (0.450980392157, 0.227450980392, 0.403921568627)), # #733a67
  "rose_bud": ColorInfo(36, (0.972549019608, 0.737254901961, 0.686274509804)), # #f8bcaf
  "atomic_tangerine": ColorInfo(37, (1.0, 0.607843137255, 0.462745098039)), # #ff9b76
  "koromiko": ColorInfo(38, (1.0, 0.749019607843, 0.372549019608)), # #ffbf5f
  "harvest_gold": ColorInfo(39, (0.850980392157, 0.686274509804, 0.443137254902)), # #d9af71
  "dolly": ColorInfo(40, (1.0, 0.956862745098, 0.501960784314)), # #fff480
  "olive_green": ColorInfo(41, (0.749019607843, 0.729411764706, 0.411764705882)), # #bfba69
  "pine_glade": ColorInfo(42, (0.737254901961, 0.8, 0.533333333333)), # #bccc88
  "mint_green": ColorInfo(43, (0.682352941176, 1.0, 0.6)), # #aeff99
  "caribbean_green_pearl": ColorInfo(44, (0.486274509804, 0.866666666667, 0.623529411765)), # #7cdd9f
  "asparagus": ColorInfo(45, (0.537254901961, 0.705882352941, 0.490196078431)), # #89b47d
  "anakiwa": ColorInfo(46, (0.501960784314, 0.952941176471, 1.0)), # #80f3ff
  "malibu": ColorInfo(47, (0.478431372549, 0.807843137255, 0.988235294118)), # #7acefc
  "danube": ColorInfo(48, (0.407843137255, 0.63137254902, 0.827450980392)), # #68a1d3
  "ship_cove": ColorInfo(49, (0.521568627451, 0.560784313725, 0.760784313725)), # #858fc2
  "biloba_flower": ColorInfo(50, (0.733333333333, 0.666666666667, 0.949019607843)), # #bbaaf2
  "prelude": ColorInfo(51, (0.803921568627, 0.733333333333, 0.894117647059)), # #cdbbe4
  "mauvelous": ColorInfo(52, (0.937254901961, 0.545098039216, 0.690196078431)), # #ef8bb0
  "mantle": ColorInfo(53, (0.521568627451, 0.61568627451, 0.549019607843)), # #859d8c
  "smoke": ColorInfo(54, (0.419607843137, 0.458823529412, 0.43137254902)), # #6b756e
  "regent_gray": ColorInfo(55, (0.517647058824, 0.564705882353, 0.607843137255)), # #84909b
  "nevada": ColorInfo(56, (0.41568627451, 0.439215686275, 0.458823529412)), # #6a7075
  "manatee": ColorInfo(57, (0.533333333333, 0.521568627451, 0.61568627451)), # #88859d
  "dolphin": ColorInfo(58, (0.423529411765, 0.41568627451, 0.458823529412)), # #6c6a75
  "venus": ColorInfo(59, (0.61568627451, 0.521568627451, 0.611764705882)), # #9d859c
  "fedora": ColorInfo(60, (0.454901960784, 0.41568627451, 0.454901960784)), # #746a74
  "lemon_grass": ColorInfo(61, (0.611764705882, 0.61568627451, 0.521568627451)), # #9c9d85
  "limed_ash": ColorInfo(62, (0.454901960784, 0.458823529412, 0.41568627451)), # #74756a
  "bazaar": ColorInfo(63, (0.61568627451, 0.517647058824, 0.517647058824)), # #9d8484
  "dove_gray": ColorInfo(64, (0.458823529412, 0.41568627451, 0.41568627451)), # #756a6a
  "cedar_wood_finish": ColorInfo(65, (0.450980392157, 0.0549019607843, 0.0)), # #730e00
  "aubergine": ColorInfo(66, (0.2, 0.0313725490196, 0.0313725490196)), # #330808
  "nutmeg": ColorInfo(67, (0.450980392157, 0.21568627451, 0.149019607843)), # #733726
  "coffee_bean": ColorInfo(68, (0.2, 0.0941176470588, 0.0666666666667)), # #331811
  "cinnamon": ColorInfo(69, (0.450980392157, 0.270588235294, 0.0)), # #734500
  "nero": ColorInfo(70, (0.149019607843, 0.0862745098039, 0.0)), # #261600
  "lisbon_brown": ColorInfo(71, (0.301960784314, 0.247058823529, 0.156862745098)), # #4d3f28
  "oil": ColorInfo(72, (0.101960784314, 0.0823529411765, 0.0509803921569)), # #1a150d
  "pesto": ColorInfo(73, (0.450980392157, 0.423529411765, 0.180392156863)), # #736c2e
  "eternity": ColorInfo(74, (0.101960784314, 0.0941176470588, 0.0392156862745)), # #1a180a
  "yukon_gold": ColorInfo(75, (0.450980392157, 0.364705882353, 0.0196078431373)), # #735d05
  "madras": ColorInfo(76, (0.149019607843, 0.121568627451, 0.00392156862745)), # #261f01
  "dup_olive": ColorInfo(77, (0.388235294118, 0.501960784314, 0.0)), # #638000
  "dup_madras": ColorInfo(78, (0.152941176471, 0.2, 0.0)), # #273300
  "verdun_green": ColorInfo(79, (0.137254901961, 0.349019607843, 0.0)), # #235900
  "deep_fir": ColorInfo(80, (0.0588235294118, 0.149019607843, 0.0)), # #0f2600
  "green_leaf": ColorInfo(81, (0.156862745098, 0.349019607843, 0.0352941176471)), # #285909
  "pine_tree": ColorInfo(82, (0.0666666666667, 0.149019607843, 0.0156862745098)), # #112604
  "dup_deep_fir": ColorInfo(83, (0.0, 0.250980392157, 0.0)), # #004000
  "dup_deep_fir": ColorInfo(84, (0.0, 0.101960784314, 0.0)), # #001a00
  "san_felix": ColorInfo(85, (0.043137254902, 0.450980392157, 0.0862745098039)), # #0b7316
  "english_holly": ColorInfo(86, (0.0156862745098, 0.149019607843, 0.0274509803922)), # #042607
  "eden": ColorInfo(87, (0.0470588235294, 0.349019607843, 0.266666666667)), # #0c5944
  "bottle_green": ColorInfo(88, (0.0196078431373, 0.149019607843, 0.113725490196)), # #05261d
  "aqua_deep": ColorInfo(89, (0.0, 0.301960784314, 0.203921568627)), # #004d34
  "burnham": ColorInfo(90, (0.0, 0.149019607843, 0.0980392156863)), # #002619
  "pine_green": ColorInfo(91, (0.0, 0.450980392157, 0.450980392157)), # #007373
  "swamp": ColorInfo(92, (0.0, 0.149019607843, 0.149019607843)), # #002626
  "midnight_blue": ColorInfo(93, (0.0, 0.207843137255, 0.450980392157)), # #003573
  "midnight": ColorInfo(94, (0.0, 0.0705882352941, 0.149019607843)), # #001226
  "dup_midnight_blue": ColorInfo(95, (0.0, 0.172549019608, 0.450980392157)), # #002c73
  "dup_midnight": ColorInfo(96, (0.0, 0.078431372549, 0.2)), # #001433
  "prussian_blue": ColorInfo(97, (0.0, 0.145098039216, 0.301960784314)), # #00254d
  "dup_midnight": ColorInfo(98, (0.0, 0.0745098039216, 0.149019607843)), # #001326
  "jacarta": ColorInfo(99, (0.18431372549, 0.137254901961, 0.4)), # #2f2366
  "ebony": ColorInfo(100, (0.0705882352941, 0.0509803921569, 0.149019607843)), # #120d26
  "meteorite": ColorInfo(101, (0.164705882353, 0.121568627451, 0.450980392157)), # #2a1f73
  "haiti": ColorInfo(102, (0.0549019607843, 0.0392156862745, 0.149019607843)), # #0e0a26
  "christalle": ColorInfo(103, (0.211764705882, 0.0, 0.4)), # #360066
  "black_russian": ColorInfo(104, (0.078431372549, 0.0, 0.149019607843)), # #140026
  "wine_berry": ColorInfo(105, (0.301960784314, 0.113725490196, 0.298039215686)), # #4d1d4c
  "tamarind": ColorInfo(106, (0.101960784314, 0.0392156862745, 0.0980392156863)), # #1a0a19
  "ripe_plum": ColorInfo(107, (0.2, 0.0, 0.301960784314)), # #33004d
  "dup_black_russian": ColorInfo(108, (0.0666666666667, 0.0, 0.101960784314)), # #11001a
  "pompadour": ColorInfo(109, (0.450980392157, 0.0, 0.270588235294)), # #730045
  "toledo": ColorInfo(110, (0.149019607843, 0.0, 0.0901960784314)), # #260017
  "livid_brown": ColorInfo(111, (0.301960784314, 0.141176470588, 0.176470588235)), # #4d242d
  "night_rider": ColorInfo(112, (0.101960784314, 0.0470588235294, 0.0588235294118)), # #1a0c0f
  "dup_wine_berry": ColorInfo(113, (0.301960784314, 0.0901960784314, 0.23137254902)), # #4d173b
  "dup_coffee_bean": ColorInfo(114, (0.101960784314, 0.0313725490196, 0.078431372549)), # #1a0814
  "tawny_port": ColorInfo(115, (0.450980392157, 0.137254901961, 0.345098039216)), # #732358
  "dup_coffee_bean": ColorInfo(116, (0.149019607843, 0.0470588235294, 0.113725490196)), # #260c1d
  "dup_black": ColorInfo(117, (0.0, 0.0, 0.0)), # #000000
  "granite_gray": ColorInfo(118, (0.349019607843, 0.349019607843, 0.349019607843)), # #595959
  "eerie_black": ColorInfo(119, (0.101960784314, 0.101960784314, 0.101960784314)), # #1a1a1a
  "white": ColorInfo(120, (1.0, 1.0, 1.0)), # #ffffff
  "dup_granite_gray": ColorInfo(121, (0.349019607843, 0.349019607843, 0.349019607843)), # #595959
  "silver": ColorInfo(122, (0.8, 0.8, 0.8)), # #cccccc
  "light_gray": ColorInfo(123, (0.250980392157, 0.250980392157, 0.250980392157)), # #404040
  "dark_gray": ColorInfo(124, (0.078431372549, 0.078431372549, 0.078431372549)), # #141414
  "blue": ColorInfo(125, (0.0, 0.0, 1.0)), # #0000ff
  "green": ColorInfo(126, (0.0, 1.0, 0.0)), # #00ff00
  "red": ColorInfo(127, (1.0, 0.0, 0.0)) # #ff0000
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
