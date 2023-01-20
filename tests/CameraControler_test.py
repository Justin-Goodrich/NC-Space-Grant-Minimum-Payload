import pytest
from CameraController import CameraController
import numpy as np 



class TestCameraController:
    camera = CameraController(0)

    def test_is_working(self):
        success = self.camera.camera.grab()
        assert success == True

    def test_capture_frame(self):
        retvalue, image = self.camera.capture_frame()
        assert isinstance(image, np.ndarray)
