#!/usr/bin/env python

import pypush2.ui

import pypush2.colors as colors
from pypush2.encoders import EncoderAction

def dialChanged(sender, action):
  if action == EncoderAction.down:
    newValue = sender.value - 0.1
    if newValue >= sender.min_value:
      sender.value = newValue
    else:
      sender.value = sender.min_value
  elif action == EncoderAction.down_fast:
    newValue = sender.value - 0.2
    if newValue >= sender.min_value:
      sender.value = newValue
    else:
      sender.value = sender.min_value
  elif action == EncoderAction.up:
    newValue = sender.value + 0.1
    if newValue <= sender.max_value:
      sender.value = newValue
    else:
      sender.value = sender.max_value
  elif action == EncoderAction.up_fast:
    newValue = sender.value + 0.2
    if newValue <= sender.max_value:
      sender.value = newValue
    else:
      sender.value = sender.max_value

def main():
  pushUi = pypush2.ui.PushUi()

  tab1 = pypush2.ui.Tab("First Tab")
  tab1.add_action(pypush2.ui.Action("Action 1"))
  tab1.add_action(pypush2.ui.Action("Action 2"))
  tab1.add_action(pypush2.ui.Action("Action 3", colors.PUSH_COLORS_DICT["dup_green"]))
  tab1.add_action(pypush2.ui.Action("Action 4"))

  dial1 = pypush2.ui.Dial("Dial 1", 3.4, 0.0, 10.0)
  dial1.on_change += dialChanged
  tab1.add_dial(dial1)

  dial2 = pypush2.ui.Dial("Dial 2", 10.0, 0.0, 10.0)
  dial2.on_change += dialChanged
  tab1.add_dial(dial2)

  dial3 = pypush2.ui.Dial("Dial 3", 0.0, 0.0, 10.0)
  dial3.on_change += dialChanged
  tab1.add_dial(dial3)

  dial4 = pypush2.ui.Dial("Dial 4", 0.001, 0.0, 10.0, colors.PUSH_COLORS_DICT["red"], colors.PUSH_COLORS_DICT["cedar_wood_finish"], colors.PUSH_COLORS_DICT["white"])
  dial4.on_change += dialChanged
  tab1.add_dial(dial4)

  dial5 = pypush2.ui.Dial("Dial 5", 9.999, 0.0, 10.0)
  dial5.on_change += dialChanged
  tab1.add_dial(dial5)

  pushUi.add_tab(tab1)

  tab2 = pypush2.ui.Tab("Second Tab")
  pushUi.add_tab(tab2)

  tab3 = pypush2.ui.Tab("Third Tab", colors.PUSH_COLORS_DICT["hollywood_cerise"], colors.PUSH_COLORS_DICT["purple"], colors.PUSH_COLORS_DICT["lavender_magenta"])
  
  dial31 = pypush2.ui.Dial("Some Dial", 5.9, 0.0, 10.0)
  dial31.on_change += dialChanged
  tab3.add_dial(dial31)

  dial32 = pypush2.ui.Dial("Yet Another Dial", 2.1, 0.0, 10.0)
  dial32.on_change += dialChanged
  tab3.add_dial(dial32)

  dial33 = pypush2.ui.Dial("This dial has a long name", 6.6, 0.0, 10.0)
  dial33.on_change += dialChanged
  tab3.add_dial(dial33)

  dial34 = pypush2.ui.Dial("This dial is a different color", 5.0, 0.0, 10.0, colors.PUSH_COLORS_DICT["red"], colors.PUSH_COLORS_DICT["cedar_wood_finish"], colors.PUSH_COLORS_DICT["white"])
  dial34.on_change += dialChanged
  tab3.add_dial(dial34)

  dial35 = pypush2.ui.Dial("Moo", 2.2, 0.0, 10.0)
  dial35.on_change += dialChanged
  tab3.add_dial(dial35)

  pushUi.add_tab(tab3)
  pushUi.run()

if __name__ == "__main__":
  main()
