#!/usr/bin/env python

import mido

import json
import urllib2

def flush_all_pending(midi_in_port):
  for message in midi_in_port.iter_pending():
    pass

def build_push_sysex_data(command_id, command_data):
  result = [0x00, 0x21, 0x1d, 0x01, 0x01]
  result.append(command_id)
  result.extend(command_data)
  return result

def wait_for_sysex_reply(midi_in_port):
  for message in midi_in_port:
    if message.type == "sysex":
      return message.data

def send_command_and_wait_for_reply(midi_in_port, midi_out_port, command_id, command_data):
  message = mido.Message("sysex", data=build_push_sysex_data(command_id, command_data))
  midi_out_port.send(message)
  return wait_for_sysex_reply(midi_in_port)

def get_color_palette_entry(midi_in_port, midi_out_port, color_index):
  messageData = send_command_and_wait_for_reply(midi_in_port, midi_out_port, 0x04, [color_index])
  returnedColorIndex = messageData[6]
  redLsb = messageData[7]
  redMsb = messageData[8]
  red = redLsb + (redMsb << 7)
  greenLsb = messageData[9]
  greenMsb = messageData[10]
  green = greenLsb + (greenMsb << 7)
  blueLsb = messageData[11]
  blueMsb = messageData[12]
  blue = blueLsb + (blueMsb << 7)
  whiteLsb = messageData[13]
  whiteMsb = messageData[14]
  white = whiteLsb + (whiteMsb << 7)

  return (returnedColorIndex, (red, green, blue), white)

def rgb_to_hex(rgb):
  return '#%02x%02x%02x' % rgb

def getColorName(rgb):
  hexColor = '%02x%02x%02x' % rgb
  try:
    resultJson = json.load(urllib2.urlopen("http://www.thecolorapi.com/id?hex=" + hexColor))
    colorName = resultJson[u"name"][u"value"]
    colorName = colorName.lower().replace(" ", "_")
  except Exception as e:
    colorName = "unknown"

  return colorName

def main():
  seenColorNames = set()
  with mido.open_input('Ableton Push 2 Live Port') as inPort,\
      mido.open_output('Ableton Push 2 Live Port') as outPort:
    flush_all_pending(inPort)

    for colorIndex in range(0, 128):
      colorEntry = get_color_palette_entry(inPort, outPort, colorIndex)

      colorName = getColorName(colorEntry[1])
      if colorName in seenColorNames:
        colorName = "dup_" + colorName

      seenColorNames.add(colorName)

      # print rgb_to_hex(colorEntry[1]), colorEntry
      print u'"{}": ColorInfo({}, ({}, {}, {})), # {}'.format(
        colorName,
        colorEntry[0],
        colorEntry[1][0] / 255.0,
        colorEntry[1][1] / 255.0,
        colorEntry[1][2] / 255.0,
        rgb_to_hex(colorEntry[1]))

if __name__ == "__main__":
  main()
