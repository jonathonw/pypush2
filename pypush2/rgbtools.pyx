import time

from cpython cimport array
import array

def rgb565ToBgr565(buffer):
  cdef int index
  cdef unsigned short value, redComponent, blueComponent, newValue
  cdef array.array originalArray = array.array('H', str(buffer))
  cdef unsigned short[:] cArray = originalArray

  cdef int length = len(originalArray)

  for index in range(length):
    redComponent = (cArray[index] >> 11) & 0b00011111
    greenComponent = (cArray[index]) & 0b0011111100000
    blueComponent = cArray[index] & 0b00011111

    newValue = (blueComponent << 11) | greenComponent | redComponent

    cArray[index] = newValue

  return originalArray

def shaping(bgrArray):
  cdef int SHAPING_PATTERN = 0xffe7f3e7
  cdef int index
  cdef array.array originalArray = array.array('I', bgrArray.tostring())
  cdef unsigned int[:] cArray = originalArray

  cdef int length = len(originalArray)

  for index in range(length):
    cArray[index] = cArray[index] ^ SHAPING_PATTERN

  return originalArray
