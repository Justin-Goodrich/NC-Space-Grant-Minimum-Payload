import cv2

class CameraController():
    def __init__(self, id=0):
        self.camera = cv2.VideoCapture(id)

    def capture_frame(self):
        retval, image = self.camera.read()
        self.camera.release()
        return retval, image
        

def ImageCamera(CameraController):
    def __init__(self):
        pass

def VideoCamera(CameraController):
    def __init__(self):
        pass

