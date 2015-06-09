import _pyfreenect2

class PyFreenect2Error(Exception):
	def __init__(self, message):
		super(PyFreenect2Error, self).__init__(message)
class DeveloperIsALazyBastardError(Exception):
	def __init__(self, message):
		super(DeveloperIsALazyBastardError, self).__init__(message)

################################################################################
#                               GLOBAL FUNCTIONS                               #
################################################################################

def numberOfDevices():
	return _pyfreenect2.numberOfDevices()
def getDefaultDeviceSerialNumber():
	if numberOfDevices() == 0:
		raise PyFreenect2Error("Could not find a Kinect v2")
	else:
		return _pyfreenect2.getDefaultDeviceSerialNumber()

################################################################################
#                                Freenect2Device                               #
################################################################################

class Freenect2Device:
	def __init__(self, serialNumber, pipeline=None):
		if pipeline is not None:
			raise DeveloperIsALazyBastardError("pyfreenect2.PacketPipeline is not yet implemented")
		self._capsule = _pyfreenect2.Freenect2Device_new(serialNumber)
	def start(self):
		_pyfreenect2.Freenect2Device_start(self._capsule)
	def stop(self):
		_pyfreenect2.Freenect2Device_stop(self._capsule)
	def setColorFrameListener(self, listener):
		if not isinstance(listener, SyncMultiFrameListener):
			raise TypeError("Argument to Freenect2Device.setColorFrameListener must be of type Freenect2Device.SyncMultiFrameListener")
		else:
			_pyfreenect2.Freenect2Device_setColorFrameListener(self._capsule, listener._capsule)
	def setIrAndDepthFrameListener(self, listener):
		if not isinstance(listener, SyncMultiFrameListener):
			raise TypeError("Argument to Freenect2Device.setIrAndDepthFrameListener must be of type Freenect2Device.SyncMultiFrameListener")
		else:
			_pyfreenect2.Freenect2Device_setIrAndDepthFrameListener(self._capsule, listener._capsule)
	@property
	def serial_number(self):
		return _pyfreenect2.Freenect2Device_getSerialNumber(self._capsule)
	@property
	def firmware_version(self):
		return _pyfreenect2.Freenect2Device_getFirmwareVersion(self._capsule)
	@property
	def color_camera_params(self):
		return _pyfreenect2.Freenect2Device_getColorCameraParams(self._capsule)
	@property
	def ir_camera_params(self):
		return _pyfreenect2.Freenect2Device_getIRCameraParams(self._capsule)

################################################################################
#                            SyncMultiFrameListener                            #
################################################################################

class SyncMultiFrameListener:
	def __init__(self, *args):
		types = 0
		for arg in args:
			types |= int(arg)
		self._capsule = _pyfreenect2.SyncMultiFrameListener_new(types)
	def waitForNewFrame(self):
		return FrameMap(_pyfreenect2.SyncMultiFrameListener_waitForNewFrame(self._capsule))


################################################################################
#                                   FrameMap                                   #
################################################################################

class FrameMap:
	def __init__(self, capsule):
		print "DEBUG: FrameMap capsule type = %s" % type(capsule)
		self._capsule = capsule
	def getFrame(self, frame_type):
		if not frame_type in (1, 2, 4):
			raise ValueError("frame_type must be one of Frame.COLOR, Frame.IR, or Frame.DEPTH")
		else:
			return Frame(_pyfreenect2.FrameMap_getFrame(self._capsule, frame_type))

################################################################################
#                                     Frame                                    #
################################################################################

class Frame:
	COLOR = 1
	IR = 2
	DEPTH = 4
	def __init__(self, capsule):
		print "DEBUG: Frame capsule type = %s" % type(capsule)
		self._capsule = capsule
	def getHeight(self):
		return _pyfreenect2.Frame_getHeight(self._capsule)
	def getWidth(self):
		return _pyfreenect2.Frame_getWidth(self._capsule)
	def getData(self):
		return _pyfreenect2.Frame_getData(self._capsule)

################################################################################
#                                 Registration                                 #
################################################################################

class Registration:
	def __init__(self, ir_camera_params, color_camera_params):
		self._capsule = _pyfreenect2.Registration_new(ir_camera_params, color_camera_params)
	def apply(self, rgbFrame, depthFrame):
		return _pyfreenect2.Registration_apply(self._capsule, rgbFrame, depthFrame)
