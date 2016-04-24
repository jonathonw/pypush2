import time

import mido

import pypush2.buttons, pypush2.pads, pypush2.encoders, pypush2._utils.events


class Device(object):
  def __init__(self):
    self.on_button_press = pypush2._utils.events.EventHandler(self)
    '''
    Event raised when a button is pressed.  Handlers should be of the form:

    handler(sender, button)
    '''

    self.on_button_release = pypush2._utils.events.EventHandler(self)
    '''
    Event raised when a button is released.  Handlers should be of the form:

    handler(sender, button)
    '''

    self.on_pad_touch = pypush2._utils.events.EventHandler(self)
    '''
    Event raised when a pad is touched.  Handlers should be of the form:

    handler(sender, padNote, velocity)
    '''

    self.on_pad_release = pypush2._utils.events.EventHandler(self)
    '''
    Event raised when a pad is released.  Handlers should be of the form:

    handler(sender, padNote, velocity)
    '''

    # Encoders not yet implemented--  need further work on the encoder
    # abstraction before they can make sense
    self.on_encoder_touch = pypush2._utils.events.EventHandler(self)
    self.on_encoder_release = pypush2._utils.events.EventHandler(self)
    self.on_encoder_change = pypush2._utils.events.EventHandler(self)

    self.on_unhandled_midi_message = pypush2._utils.events.EventHandler(self)
    '''
    Event raised when a MIDI message is received but isn't handled by
    one of the other event types.  Handlers should be of the form:

    handler(sender, midiMessage)

    where midiMessage is a mido.Message.
    '''
    
    self._midi_input = mido.open_input('Ableton Push 2 Live Port')
    self._midi_output = mido.open_output('Ableton Push 2 Live Port')

  def __del__(self):
    self.close()

  def close(self):
    if not self._midi_input.closed:
      self._midi_input.close()
    if not self._midi_output.closed:
      self._midi_output.close()

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()

  def send_midi_message(self, message):
    '''
    Sends a raw MIDI message.  message should be a mido.Message.
    '''
    self._midi_output.send(message)

  def listen(self):
    '''
    Starts listening for MIDI messages.  This method blocks indefinitely,
    until KeyboardInterrupt is received (^C).
    '''
    # Clear out queued messages (Push sends a bunch of stuff on startup
    # that we don't care about, and will also queue up messages that
    # happen while nothing is running to receive them.)
    #for msg in self._midi_input.iter_pending():
    #  print msg
    #  pass
    time.sleep(0.1)
    while self._midi_input.receive(block = False) != None:
      pass

    try:
      self._midi_input.callback = self._on_midi_message_received

      # Setting callback spawns off a background thread within mido that
      # actually handles MIDI data--  we need to loop here so we don't
      # terminate prematurely.
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      pass

  def _on_midi_message_received(self, message):
    if message.type == "control_change":
      if pypush2.buttons.is_button(message.control):
        if message.value == pypush2.buttons.BUTTON_PRESSED_VALUE:
          self.on_button_press(pypush2.buttons.Buttons[message.control])
          return
        elif message.value == pypush2.buttons.BUTTON_RELEASED_VALUE:
          self.on_button_release(pypush2.buttons.Buttons[message.control])
          return
      elif pypush2.encoders.cc_is_display_encoder(message.control):
        encoderNumber = pypush2.encoders.get_encoder_number_from_cc(message.control)
        action = pypush2.encoders.convert_encoder_cc_value(message.value)
        self.on_encoder_change(encoderNumber, action)
    elif message.type == "note_on":
      if pypush2.pads.is_pad(message.note):
        self.on_pad_touch(message.note, message.velocity)
        return
      elif pypush2.encoders.note_is_display_encoder(message.note):
        if message.velocity == 127:
          self.on_encoder_touch(message.note - pypush2.encoders._DISPLAY_ENCODER_BASE_NOTE)
        elif message.velocity == 0:
          self.on_encoder_release(message.note - pypush2.encoders._DISPLAY_ENCODER_BASE_NOTE)
    elif message.type == "note_off":
      if pypush2.pads.is_pad(message.note):
        self.on_pad_release(message.note, message.velocity)
        return

    self.on_unhandled_midi_message(message)
