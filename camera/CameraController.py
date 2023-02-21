import cv2
import threading
import os
import time

class CameraController():
    def __init__(self, id=0):
        self.id = id
        self.camera = cv2.VideoCapture(id,cv2.CAP_V4L)

    def turn_on(self):
        if self.camera.isOpened() == False:
            self.camera.open()

    def capture_frame(self):
        retval, image = self.camera.read()
        return image
        
class ImageCamera(CameraController):
    def image_collection(self, increment, n_photos, dir):

        """ 
        Takes a collection of images containg n photos
        @param increment: time increment in seconds for to take photos in
        @param n_photos: number of photos to take
        @param dir: sub directory to save images to 
        """

        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),dir)

        os.makedirs(dir_path, exist_ok=True)

        
        for i in range(n_photos):
            #files are to be save in a given directory, each file is to be named minimum_payload_image_(index).png            
            file_name = os.path.join(dir_path,'minimum_payload_image_{}.png'.format(i))
            image = self.capture_frame()

            # because of the limit computing power of the Raspberry Pi Zero a new thread is to start to write image to memory,
            # in order to save time and take advantage of our 15 second increment requirement
            
            t = threading.Thread(target = cv2.imwrite, args=(file_name,image))
            t.start()
            time.sleep(increment)
            t.join()


        
class VideoCamera(CameraController):
    def __init__(self):
        pass

print(os.listdir('./'))
