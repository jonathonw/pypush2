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
import pypush2

from math import pi

PAGE_LEFT_BUTTON=62
PAGE_RIGHT_BUTTON=63

class DisplayThread(pypush2.DisplayView):
  def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
    pypush2.DisplayView.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
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
      context.arc(pypush2.DisplayView.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.DisplayView.DisplayParameters.DISPLAY_HEIGHT - 20, 10, 0, 2 * pi)
      context.stroke()
      
      context.set_source_rgb(1, 0.1, 0.1)
      if self.iteration == 0:
        context.arc(pypush2.DisplayView.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.DisplayView.DisplayParameters.DISPLAY_HEIGHT - 20, 10, 0, (float(self.animationFrameNumber) / 30) * 2 * pi)
      else:
        context.arc(pypush2.DisplayView.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.DisplayView.DisplayParameters.DISPLAY_HEIGHT - 20, 10, (float(self.animationFrameNumber) / 30) * 2 * pi, 2 * pi)
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

def main():
  displayThread = DisplayThread()
  displayThread.start()

  def setString(message):
    #print message
    if(message.type == 'note_on'):
      displayThread.setStringToDisplay(u"{}/{} (Note: {})".format(message.note - 36, message.note - 36 + 64, message.note))
    else:
      if message.type == 'control_change' and message.control == PAGE_LEFT_BUTTON and message.value == 127:
        output.send(mido.Message('control_change', channel=0, control=PAGE_LEFT_BUTTON, value=0))
        output.send(mido.Message('control_change', channel=0, control=PAGE_RIGHT_BUTTON, value=127))

        for i in range(36,100):
          output.send(mido.Message('note_on', channel=0, note=i, velocity=i-36))
      elif message.type == 'control_change' and message.control == PAGE_RIGHT_BUTTON and message.value == 127:
        output.send(mido.Message('control_change', channel=0, control=PAGE_LEFT_BUTTON, value=127))
        output.send(mido.Message('control_change', channel=0, control=PAGE_RIGHT_BUTTON, value=0))

        for i in range(36,100):
          output.send(mido.Message('note_on', channel=0, note=i, velocity=i-36+64))
      else:
        print message

  try:
    with mido.open_output('Ableton Push 2 Live Port') as output, \
         mido.open_input('Ableton Push 2 Live Port') as input:
      #while True:
      for i in range(0,128):
        output.send(mido.Message('control_change', channel=0, control=i, value=0))

      output.send(mido.Message('control_change', channel=0, control=PAGE_RIGHT_BUTTON, value=127))

      for i in range(36,100):
        output.send(mido.Message('note_on', channel=0, note=i, velocity=i-36))

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
