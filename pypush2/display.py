import time
import threading
import usb.core
import usb.util
import array
import cairocffi
import rgbtools
import cProfile

_FRAMES_PER_SECOND = 60.0

class DisplayParameters:
  DISPLAY_WIDTH = 960
  DISPLAY_HEIGHT = 160

  BUFFER_WIDTH = 1024
  BUFFER_HEIGHT = 160

class DisplayRenderer(threading.Thread):
  '''
  DisplayRenderer is an abstract superclass implementing logic to
  push frames (rendered with Cairo) to the Push 2's display.  To use,
  override the paint(context) method, instantiate an instance, and call
  start().

  Since this spawns a background thread to do the actual work of
  interacting with the Push, subclasses will want to make sure to use
  the appropriate synchronization mechanisms when working with data
  inside paint that may be used from other threads.
  '''

  _MAGIC_HEADER = array.array('B', [ 0xFF, 0xCC, 0xAA, 0x88, 
                                     0x00, 0x00, 0x00, 0x00, 
                                     0x00, 0x00, 0x00, 0x00, 
                                     0x00, 0x00, 0x00, 0x00 ]);

  _PUSH_VID = 0x2982
  _PUSH_PID = 0x1967

  def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
    threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
    self.cancelled = threading.Event()

  def paint(self, context):
    raise NotImplementedError("Subclasses must implement paint")

  def cancel(self):
    self.cancelled.set()

  def is_cancelled(self):
    return self.cancelled.is_set()

  def run(self):
    dev = usb.core.find(idVendor=DisplayRenderer._PUSH_VID, idProduct=DisplayRenderer._PUSH_PID)

    if dev is None:
      raise ValueError("Device not found")

    dev.set_configuration()

    surface = cairocffi.ImageSurface(cairocffi.FORMAT_RGB16_565, DisplayParameters.BUFFER_WIDTH, DisplayParameters.BUFFER_HEIGHT)
    context = cairocffi.Context(surface)
    while not self.is_cancelled():
      start = time.clock()
      
      with context:
        self.paint(context)

      surface.flush()

      data = surface.get_data()
      convertedBgr = rgbtools.rgb565ToBgr565(data)
      shapedBgr = rgbtools.shaping(convertedBgr)

      end = time.clock()

      dev.write(1, DisplayRenderer._MAGIC_HEADER)
      dev.write(1, shapedBgr)

      frameTime = end - start

      if(frameTime < (1.0 / _FRAMES_PER_SECOND)):
        time.sleep((1.0 / _FRAMES_PER_SECOND) - frameTime)
      else:
        time.sleep(1.0 / _FRAMES_PER_SECOND)

class ProfiledDisplayRenderer(DisplayRenderer):
    # Overrides threading.Thread.run()
    def run(self):
        profiler = cProfile.Profile()
        try:
            return profiler.runcall(DisplayRenderer.run, self)
        finally:
            profiler.dump_stats('myprofile-%d.profile' % (self.ident,))
