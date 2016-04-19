import pypush2.display, pypush2.colors, pypush2.device
import cairocffi
import mido
import threading

from math import pi

color = pypush2.colors.PUSH_COLORS_DICT["azure_radiance"]
dark_color = pypush2.colors.PUSH_COLORS_DICT["midnight"]
highlight_color = pypush2.colors.PUSH_COLORS_DICT["cyan_aqua"]

class PushUi(object):
  def __init__(self, ui_spec):
    self._uiSpec = ui_spec

  def run(self):
    self._displayThread = _DisplayThread(self._uiSpec)
    self._displayThread.start()

    try:
      with pypush2.device.Device() as pushDevice:
        self._setup_button_leds(pushDevice)

        pushDevice.on_encoder_touch += self._on_encoder_touched
        pushDevice.on_encoder_release += self._on_encoder_released

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

  def _on_encoder_touched(self, sender, encoderNumber):
    self._displayThread.set_highlighted_gauge(encoderNumber)

  def _on_encoder_released(self, sender, encoderNumber):
    self._displayThread.set_highlighted_gauge(-1)


labels = ["Label", "ayayay", "Long label with really long name and stuff", "Hi There!", "Another label", "More labels!!!!!", "Moo", "Stuff"]


class _DisplayThread(pypush2.display.DisplayRenderer):
  def __init__(self, ui_spec, group=None, target=None, name=None, args=(), kwargs={}):
    pypush2.display.DisplayRenderer.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
    self._uiSpec = ui_spec
    self._highlightedGaugeLock = threading.Lock()
    self._highlightedGauge = -1

  def _get_ui_spec(self):
    return self._uiSpec

  def set_highlighted_gauge(self, highlighted_gauge):
    with self._highlightedGaugeLock:
      self._highlightedGauge = highlighted_gauge

  def get_highlighted_gauge(self):
    with self._highlightedGaugeLock:
      return self._highlightedGauge

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

    # displayedString = "Test"
    # with context:
    #   context.set_source_rgb(*color.rgb_color)
    #   context.move_to(20, 90)
    #   context.select_font_face(family="Avenir")
    #   context.set_font_size(32)
    #   context.text_path(displayedString)
    #   context.fill()

    for i in range(0, 8):
      self.drawLabel(context, labels[i], i % 2 == 0, (5 + 120*i, 3))

    for i in range(0, 8):
      self.drawLabel(context, labels[i], i % 2 == 1, (5 + 120*i, pypush2.display.DisplayParameters.DISPLAY_HEIGHT-23))

    for i in range(0, 8):
      self.drawGauge(context, labels[i], float(i) + 1.0, 0, 8, i == self.get_highlighted_gauge(), (5 + 120*i, 25))

  def drawLabel(self, context, text, shouldFill, position):
    with context:
      context.rectangle(*position, width=110, height=20)
      context.clip()
      if shouldFill:
        context.set_source_rgb(*color.rgb_color)
        context.paint()
        context.set_source_rgb(0, 0, 0)
      else:
        context.set_source_rgb(*color.rgb_color)

      context.move_to(position[0] + 5, position[1] + 15)
      context.select_font_face(family="Avenir")
      context.set_font_size(13)
      context.text_path(text)
      context.fill()

  def drawGauge(self, context, titleText, currentValue, minValue, maxValue, highlighted, position):
    positionX = position[0]
    positionY = position[1]

    with context:
      primaryColor = color.rgb_color
      if highlighted:
        primaryColor = highlight_color.rgb_color

      context.rectangle(*position, width=110, height=110)
      context.clip()
      # with context:
      #   context.set_source_rgb(*pypush2.colors.PUSH_COLORS_DICT["eerie_black"].rgb_color)
      #   context.paint()

      context.set_source_rgb(*primaryColor)
      context.select_font_face(family="Avenir")
      context.set_font_size(13)
      self.drawCenteredText(context, titleText, (positionX + (110.0 / 2.0), positionY + 18))
      context.set_font_size(18)
      self.drawCenteredText(context, str(currentValue), (positionX + (110.0/2.0), positionY + 73))

      valuePoint = (-5.0 * pi / 4.0) + ((currentValue - minValue) / (maxValue - minValue)) * (6.0 * pi / 4.0)

      context.set_line_width(6)
      context.set_line_cap(cairocffi.LINE_CAP_ROUND)

      context.set_source_rgb(*dark_color.rgb_color)
      context.arc(positionX + 55, positionY + 70, 35, valuePoint, pi / 4.0)
      context.stroke()

      context.set_source_rgb(*primaryColor)
      context.arc(positionX + 55, positionY + 70, 35, (-5.0 * pi / 4.0), valuePoint)
      context.stroke()

  def drawCenteredText(self, context, text, bottomCenterPosition):
    with context:
      extents = context.text_extents(text)
      context.move_to(bottomCenterPosition[0] - (extents[2] / 2.0), bottomCenterPosition[1])
      context.text_path(text)
      context.fill()


