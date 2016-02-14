#!/usr/bin/env python
"""
pypush2 LED Colors example
==========================

This is an example script using pypush2 to:

1. Display the default Push 2 LED color palette on the Push 2 pad grid
2. Handle paging between the two pages of colors (since Push has a 
   128-color palette, and only has 64 pads)
3. When a pad is touched, use the Push display to show the index of the
   touched color in the palette and the pad number.

This script is being migrated to use pypush2 abstractions as they become
available; currently, it only uses pypush2 to implement display handling.
For now, button handling is still implemented directly using mido for MIDI.
"""

import threading
import time

import mido
import pypush2.display
import pypush2.buttons

from math import pi

PAGE_LEFT_BUTTON=62
PAGE_RIGHT_BUTTON=63

class DisplayThread(pypush2.display.DisplayRenderer):
  def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
    pypush2.display.DisplayRenderer.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
    self.stringToDisplay = u"Touch a pad to see the color value it\u2019s showing"
    self.stringToDisplayLock = threading.Lock()
    self.animationFrameNumber = 0
    self.iteration = 0

  def setStringToDisplay(self, newString):
    with self.stringToDisplayLock:
      self.stringToDisplay = newString

  def getStringToDisplay(self):
    with self.stringToDisplayLock:
      val = self.stringToDisplay
    return val

  def paint(self, context):
    with context:
      context.set_source_rgb(0, 0, 0)
      context.paint()

    with context:
      context.set_source_rgb(0.1, 0.1, 0.1)
      context.arc(pypush2.display.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.display.DisplayParameters.DISPLAY_HEIGHT - 20, 10, 0, 2 * pi)
      context.stroke()
      
      context.set_source_rgb(1, 0.1, 0.1)
      if self.iteration == 0:
        context.arc(pypush2.display.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.display.DisplayParameters.DISPLAY_HEIGHT - 20, 10, 0, (float(self.animationFrameNumber) / 30) * 2 * pi)
      else:
        context.arc(pypush2.display.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.display.DisplayParameters.DISPLAY_HEIGHT - 20, 10, (float(self.animationFrameNumber) / 30) * 2 * pi, 2 * pi)
      context.stroke()
      self.animationFrameNumber = (self.animationFrameNumber + 1) % 30
      if self.animationFrameNumber == 0:
        self.iteration = (self.iteration + 1) % 2

    with context:
      context.set_source_rgb(1, 1, 1)
      context.move_to(20, 90)
      context.select_font_face(family="Segoe UI")
      context.set_font_size(32)
      context.text_path(self.getStringToDisplay())
      context.fill()

def printMessage(message):
  print message

def setupLeds(output, allLedsOn, colorGridPage):
  if allLedsOn:
    dimLevel = 3
    for i in range(0,128):
      if i in pypush2.buttons.colored_buttons:
        output.send(mido.Message('control_change', channel=0, control=i, value=94))
      else:
        output.send(mido.Message('control_change', channel=0, control=i, value=dimLevel))
    output.send(mido.Message('control_change', channel=0, control=pypush2.buttons.Buttons.play, value=95))
  else:
    dimLevel = 0
    for i in range(0,128):
      output.send(mido.Message('control_change', channel=0, control=i, value=dimLevel))
    output.send(mido.Message('control_change', channel=0, control=pypush2.buttons.Buttons.play, value=94))

  if colorGridPage == 0:
    for i in range(36,100):
      output.send(mido.Message('note_on', channel=0, note=i, velocity=i-36))
    output.send(mido.Message('control_change', channel=0, control=pypush2.buttons.Buttons.page_left, value=dimLevel))
    output.send(mido.Message('control_change', channel=0, control=pypush2.buttons.Buttons.page_right, value=127))
  else:
    for i in range(36,100):
      output.send(mido.Message('note_on', channel=0, note=i, velocity=i-36+64))
    output.send(mido.Message('control_change', channel=0, control=pypush2.buttons.Buttons.page_left, value=127))
    output.send(mido.Message('control_change', channel=0, control=pypush2.buttons.Buttons.page_right, value=dimLevel))


def main():
  displayThread = DisplayThread()
  displayThread.start()

  ledState = {
    "ledPage": 0,
    "allLedsOn": False
  }

  def setString(message):
    # Display handling
    if(message.type == 'note_on'):
      displayThread.setStringToDisplay(u"{}/{} (Note: {})".format(message.note - 36, message.note - 36 + 64, message.note))
    elif(message.type == 'control_change'):
      if pypush2.buttons.is_button(message.control):
        button = pypush2.buttons.Buttons[message.control]
        displayThread.setStringToDisplay(u"CC: {} ({})".format(message.control, button.name))
      else:
        displayThread.setStringToDisplay(u"CC: {}".format(message.control))
      print "Control:", message.control
    else:
      print message

    # Button event handling
    if message.type == 'control_change' and message.control == pypush2.buttons.Buttons.page_left and message.value == 127:
      ledState["ledPage"] = 0
      setupLeds(output, ledState["allLedsOn"], ledState["ledPage"])
    elif message.type == 'control_change' and message.control == pypush2.buttons.Buttons.page_right and message.value == 127:
      ledState["ledPage"] = 1
      setupLeds(output, ledState["allLedsOn"], ledState["ledPage"])
    elif message.type == 'control_change' and message.control == pypush2.buttons.Buttons.play and message.value == 127:
      ledState["allLedsOn"] = not ledState["allLedsOn"]
      setupLeds(output, ledState["allLedsOn"], ledState["ledPage"])

  try:
    with mido.open_output('Ableton Push 2 Live Port') as output, \
         mido.open_input('Ableton Push 2 Live Port') as input:
      setupLeds(output, ledState["allLedsOn"], ledState["ledPage"])

      input.callback = setString
      while True:
        time.sleep(1)

    time.sleep(1)
  except KeyboardInterrupt:
    pass
  finally:
    displayThread.cancel()
    displayThread.join()

if __name__ == "__main__":
  main()
