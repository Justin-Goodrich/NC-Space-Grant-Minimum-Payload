from CameraController import CameraController, ImageCamera
import numpy as np 
import os


class TestCameraController:
    camera = CameraController(0)

    def test_is_working(self):
        success = self.camera.camera.grab()
        assert success == True

    def test_capture_frame(self):
        image = self.camera.capture_frame()
        assert isinstance(image, np.ndarray)

class TestImageCamera:
    image_camera = ImageCamera(0)

    def test_take_photos(self,tmp_path):
        n_photos = 5
        increment = 1
        d = tmp_path / "sub"
        self.image_camera.image_collection(increment,n_photos,d)
        assert len(os.listdir(d)) == n_photos

