from camera.CameraController import CameraController, ImageCamera
import numpy as np 
import os


class TestCameraController:
    def test_is_working(self):
        cam = CameraController(0)
        success = cam.camera.grab()
        assert success == True

    def test_capture_frame(self):
        cam = CameraController(0)
        image = cam.capture_frame()
        assert isinstance(image, np.ndarray)

class TestImageCamera:
    def test_take_photos(self,tmp_path):
        cam = ImageCamera(0)
        n_photos = 5
        increment = 1
        d = tmp_path / "sub"
        cam.image_collection(increment,n_photos,d)
        assert len(os.listdir(d)) == n_photos

