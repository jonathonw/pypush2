import pypush2.display, pypush2.colors, pypush2.device
import cairocffi
import mido

color = pypush2.colors.PUSH_COLORS_DICT["pink"]

class PushUi(object):
  def __init__(self, ui_spec):
    self._uiSpec = ui_spec

  def run(self):
    self._displayThread = _DisplayThread(self._uiSpec)
    self._displayThread.start()

    try:
      with pypush2.device.Device() as pushDevice:
        self._setup_button_leds(pushDevice)

        print "Listening to Push..."
        pushDevice.listen()
    finally:
      self._displayThread.cancel()
      self._displayThread.join()

  def _setup_button_leds(self, pushDevice):
    for i in range(0,128):
      pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=i, value=0))

    for i in range(36,100):
      pushDevice.send_midi_message(mido.Message('note_off', channel=0, note=i, velocity=0))

    for i in range(0, 8):
      pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=(pypush2.buttons.Buttons.top_display_0 + i), value=color.push_color_index))
      pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=(pypush2.buttons.Buttons.bottom_display_0 + i), value=color.push_color_index))
    pass


labels = ["Label", "ayayay", "Long label with really long name and stuff", "Hi There!", "Another label", "More labels!!!!!", "Moo", "Stuff"]


class _DisplayThread(pypush2.display.DisplayRenderer):
  def __init__(self, ui_spec, group=None, target=None, name=None, args=(), kwargs={}):
    pypush2.display.DisplayRenderer.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
    self._uiSpec = ui_spec

  def _get_ui_spec(self):
    return self._uiSpec

  def paint(self, context):
    with context:
      context.set_source_rgb(0, 0, 0)
      context.paint()

    # with context:
    #   context.set_source_rgba(0.5, 0.5, 0.5, 0.5)
    #   context.arc(pypush2.display.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.display.DisplayParameters.DISPLAY_HEIGHT - 20, 10, 0, 2 * pi)
    #   context.stroke()
      
    #   context.set_source_rgb(1, 1, 1)
    #   if self.iteration == 0:
    #     context.arc(pypush2.display.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.display.DisplayParameters.DISPLAY_HEIGHT - 20, 10, 0, (float(self.animationFrameNumber) / 30) * 2 * pi)
    #   else:
    #     context.arc(pypush2.display.DisplayParameters.DISPLAY_WIDTH - 20, pypush2.display.DisplayParameters.DISPLAY_HEIGHT - 20, 10, (float(self.animationFrameNumber) / 30) * 2 * pi, 2 * pi)
    #   context.stroke()
    #   self.animationFrameNumber = (self.animationFrameNumber + 1) % 30
    #   if self.animationFrameNumber == 0:
    #     self.iteration = (self.iteration + 1) % 2

    displayedString = "Test"
    with context:
      context.set_source_rgb(*color.rgb_color)
      context.move_to(20, 90)
      context.select_font_face(family="Avenir")
      context.set_font_size(32)
      context.text_path(displayedString)
      context.fill()

    for i in range(0, 8):
      self.drawLabel(context, labels[i], i % 2 == 0, (5 + 120*i, 3))

    for i in range(0, 8):
      self.drawLabel(context, labels[i], i % 2 == 1, (5 + 120*i, pypush2.display.DisplayParameters.DISPLAY_HEIGHT-27))

  def drawLabel(self, context, text, shouldFill, position):
    with context:
      context.rectangle(*position, width=110, height=24)
      context.clip()
      if shouldFill:
        context.set_source_rgb(*color.rgb_color)
        context.paint()
        context.set_source_rgb(0, 0, 0)
      else:
        context.set_source_rgb(*color.rgb_color)

      context.move_to(position[0] + 5, position[1] + 17)
      context.select_font_face(family="Avenir")
      context.set_font_size(14)
      context.text_path(text)
      context.fill()
