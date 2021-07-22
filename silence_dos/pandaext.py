import usb1
import sys
from panda import Panda

class PandaExtended(Panda):
  def __init__(self, serial=None, claim=True):
    Panda.__init__(self, serial=serial, claim=claim)

  def connect(self, claim=True, wait=False):
    if self._handle is not None:
      self.close()
    context = usb1.USBContext()
    self._handle = None
    self.wifi = False
    while 1:
      try:
        for device in context.getDeviceList(skip_on_error=True):
          if device.getVendorID() == 0xbbaa and device.getProductID() in [0xddcc, 0xddee, 0xddff]:
            try:
              this_serial = device.getSerialNumber()
            except Exception:
              continue
            if self._serial is None or this_serial == self._serial:
              self._serial = this_serial
              print("opening device", self._serial, hex(device.getProductID()))
              self.bootstub = device.getProductID() == 0xddee
              self._handle = device.open()
              if sys.platform not in ["win32", "cygwin", "msys", "darwin"]:
                self._handle.setAutoDetachKernelDriver(True)
              if claim:
                self._handle.claimInterface(0)
              break
      except Exception as e:
        print("exception", e)
        traceback.print_exc()
      if not wait or self._handle is not None:
        break
      context = usb1.USBContext()  # New context needed so new devices show up
    assert(self._handle is not None)
    print("connected")

  @staticmethod
  def list():
    context = usb1.USBContext()
    ret = []
    try:
      for device in context.getDeviceList(skip_on_error=True):
        if device.getVendorID() == 0xbbaa and device.getProductID() in [0xddcc, 0xddee, 0xddff]:
          try:
            ret.append(device.getSerialNumber())
          except Exception:
            continue
    except Exception:
      pass
    return ret
