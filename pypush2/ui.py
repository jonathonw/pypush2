import pypush2.display, pypush2.colors, pypush2.device, pypush2.buttons, pypush2._utils.events
import cairocffi
import mido
import threading

from math import pi

from collections import deque

color = pypush2.colors.PUSH_COLORS_DICT["azure_radiance"]
dark_color = pypush2.colors.PUSH_COLORS_DICT["midnight"]
highlight_color = pypush2.colors.PUSH_COLORS_DICT["white"]

class PushUi(object):
  def __init__(self):
    self._displayThread = _DisplayThread()

  def run(self):
    self._displayThread.start()

    try:
      with pypush2.device.Device() as pushDevice:
        self._setup_button_leds(pushDevice)

        pushDevice.on_button_press += self._on_button_pressed
        pushDevice.on_encoder_touch += self._on_encoder_touched
        pushDevice.on_encoder_release += self._on_encoder_released

        self._displayThread.update_display_button_colors(pushDevice)

        print "Listening to Push..."
        pushDevice.listen()
    finally:
      self._displayThread.cancel()
      self._displayThread.join()

  def add_tab(self, new_tab):
    self._displayThread.add_tab(new_tab)

  def set_current_tab(self, tab_index):
    self._displayThread.set_current_tab(tab_index)

  def _setup_button_leds(self, pushDevice):
    for i in range(0,128):
      pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=i, value=0))

    for i in range(36,100):
      pushDevice.send_midi_message(mido.Message('note_off', channel=0, note=i, velocity=0))

  def _on_encoder_touched(self, sender, encoderNumber):
    self._displayThread.highlight_gauge(encoderNumber)

  def _on_encoder_released(self, sender, encoderNumber):
    self._displayThread.unhighlight_gauge(encoderNumber)

  def _on_button_pressed(self, sender, button):
    if(pypush2.buttons.is_display_button(button) and
      pypush2.buttons.get_display_button_group(button) == pypush2.buttons.DisplayButtonGroups.bottom):
      def fn():
        try:
          self.set_current_tab(pypush2.buttons.get_display_button_index(button))
          self._displayThread.update_display_button_colors(sender)
        except IndexError:
          pass

      self._displayThread.run_operation_in_ui_thread(fn)
      


class Tab(object):
  def __init__(self, title, active_color=color, inactive_color=dark_color, highlight_color=highlight_color):
    self.title = title
    self.active_color = active_color
    self.inactive_color = inactive_color
    self.highlight_color = highlight_color

    self.tab_selected = pypush2._utils.events.EventHandler(self)
    self.tab_deselected = pypush2._utils.events.EventHandler(self)

    self._actions = []
    self._dials = []

  def add_action(self, new_action):
    self._actions.append(new_action)

  def add_dial(self, new_dial):
    self._dials.append(new_dial)

  def _draw(self, context, index, highlighted):
    _drawLabel(context, self.title, highlighted, (5 + 120*index, pypush2.display.DisplayParameters.DISPLAY_HEIGHT-23), self.active_color)

class Action(object):
  def __init__(self, title, color=None):
    self.title = title
    self.color = color

    self.on_action = pypush2._utils.events.EventHandler(self)

  def _draw(self, context, index, inherited_color):
    color = self.color or inherited_color

    _drawLabel(context, self.title, False, (5 + 120*index, 3), color)

class Dial(object):
  def __init__(self, title, initial_value, min_value, max_value, active_color=None, inactive_color=None, highlight_color=None):
    self.title = title
    self.value = initial_value
    self.min_value = min_value
    self.max_value = max_value

    self.active_color = active_color
    self.inactive_color = inactive_color
    self.highlight_color = highlight_color

    self.on_change = pypush2._utils.events.EventHandler(self)

    self.value_format = None

  def _draw(self, context, index, highlighted, inherited_active_color, inherited_inactive_color, inherited_highlight_color):
    active_color = self.active_color or inherited_active_color
    inactive_color = self.inactive_color or inherited_inactive_color
    highlight_color = self.highlight_color or inherited_highlight_color

    _drawDial(context, self.title, self.value, self.min_value, self.max_value, highlighted, (5 + 120*index, 25), active_color, inactive_color, highlight_color)


labels = ["Label", "ayayay", "Long label with really long name and stuff", "Hi There!", "Another label", "More labels!!!!!", "Moo", "Stuff"]


class _DisplayThread(pypush2.display.DisplayRenderer):
  def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
    pypush2.display.DisplayRenderer.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
    self._tabs = []
    self._highlightedGaugeLock = threading.Lock()
    self._highlightedGauges = set()
    self._current_tab = 0

    self._operation_queue = deque()

  def run_operation_in_ui_thread(self, operation):
    self._operation_queue.appendleft(operation) # no locking needed here; deque operations are guaranteed to be atomic

  def add_tab(self, new_tab):
    self._tabs.append(new_tab)

  def set_current_tab(self, tab_index):
    if tab_index < 0 or tab_index >= len(self._tabs):
      raise IndexError("Tab index out of bounds")
    else:
      self._current_tab = tab_index

  def update_display_button_colors(self, pushDevice):
    for i in range(8):
      # Bottom row: tab buttons
      if i < len(self._tabs):
        if i == self._current_tab:
          pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=(pypush2.buttons.Buttons.bottom_display_0 + i), value=self._tabs[i].active_color.push_color_index))
        else:
          pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=(pypush2.buttons.Buttons.bottom_display_0 + i), value=self._tabs[i].inactive_color.push_color_index))
      else:
        pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=(pypush2.buttons.Buttons.bottom_display_0 + i), value=pypush2.colors.PUSH_COLORS_DICT["black"].push_color_index))

      # Top row: action buttons
      if len(self._tabs) > 0 and i < len(self._tabs[self._current_tab]._actions):
        actionColor = self._tabs[self._current_tab]._actions[i].color or self._tabs[self._current_tab].active_color
        pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=(pypush2.buttons.Buttons.top_display_0 + i), value=actionColor.push_color_index))
      else:
        pushDevice.send_midi_message(mido.Message('control_change', channel=0, control=(pypush2.buttons.Buttons.top_display_0 + i), value=pypush2.colors.PUSH_COLORS_DICT["black"].push_color_index))

  def highlight_gauge(self, gauge):
    with self._highlightedGaugeLock:
      self._highlightedGauges.add(gauge)

  def unhighlight_gauge(self, gauge):
    with self._highlightedGaugeLock:
      self._highlightedGauges.discard(gauge)

  def shouldHighlightGauge(self, gauge):
    with self._highlightedGaugeLock:
      return gauge in self._highlightedGauges

  def paint(self, context):
    # Perform scheduled UI thread operations
    # Iterate across queue until it's out of elements
    try:
      while True:
        operation = self._operation_queue.pop()
        operation()
    except IndexError:
      pass

    with context:
      context.set_source_rgb(0, 0, 0)
      context.paint()

      for i, tab in enumerate(self._tabs):
        tab._draw(context, i, i == self._current_tab)

      if self._current_tab < len(self._tabs):
        currentTab = self._tabs[self._current_tab]
        for i, action in enumerate(currentTab._actions):
          action._draw(context, i, currentTab.active_color)

        for i, dial in enumerate(currentTab._dials):
          dial._draw(context, i, self.shouldHighlightGauge(i), currentTab.active_color, currentTab.inactive_color, currentTab.highlight_color)


    # for i in range(0, 8):
    #   _drawLabel(context, labels[i], i % 2 == 0, (5 + 120*i, 3))

    # for i in range(0, 8):
    #   _drawLabel(context, labels[i], i % 2 == 1, (5 + 120*i, pypush2.display.DisplayParameters.DISPLAY_HEIGHT-23))

    # for i in range(0, 8):
    #   _drawDial(context, labels[i], float(i) + 1.0, 0, 8, self.shouldHighlightGauge(i), (5 + 120*i, 25))

def _drawLabel(context, text, shouldFill, position, color):
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

def _drawDial(context, titleText, currentValue, minValue, maxValue, highlighted, position, primaryColor, secondaryColor, highlightColor):
  positionX = position[0]
  positionY = position[1]

  with context:
    dialColor = primaryColor.rgb_color
    if highlighted:
      dialColor = highlightColor.rgb_color

    context.rectangle(*position, width=110, height=110)
    context.clip()
    # with context:
    #   context.set_source_rgb(*pypush2.colors.PUSH_COLORS_DICT["eerie_black"].rgb_color)
    #   context.paint()

    context.set_source_rgb(*dialColor)
    context.select_font_face(family="Avenir")
    context.set_font_size(13)
    _drawCenteredText(context, titleText, (positionX + (110.0 / 2.0), positionY + 18))
    context.set_font_size(18)
    _drawCenteredText(context, str(currentValue), (positionX + (110.0/2.0), positionY + 73))

    valuePoint = (-5.0 * pi / 4.0) + ((currentValue - minValue) / (maxValue - minValue)) * (6.0 * pi / 4.0)

    context.set_line_width(6)
    context.set_line_cap(cairocffi.LINE_CAP_ROUND)

    context.set_source_rgb(*secondaryColor.rgb_color)
    context.arc(positionX + 55, positionY + 70, 35, valuePoint, pi / 4.0)
    context.stroke()

    context.set_source_rgb(*dialColor)
    context.arc(positionX + 55, positionY + 70, 35, (-5.0 * pi / 4.0), valuePoint)
    context.stroke()

def _drawCenteredText(context, text, bottomCenterPosition):
  with context:
    extents = context.text_extents(text)
    context.move_to(bottomCenterPosition[0] - (extents[2] / 2.0), bottomCenterPosition[1])
    context.text_path(text)
    context.fill()


