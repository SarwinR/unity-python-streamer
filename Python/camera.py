import receiver
import cv2
import numpy as np

class Camera:
    def __init__(self, width, height, host, port, video=None):
        self.width = width
        self.height = height
        self.host = host
        self.port = port
        self.video = video
        self.receiver = receiver.Receiver(width, height, host, port, video)
        
    def _getFrame(self):
        data = self.receiver.receive_raw()
        if data:
            # Convert the byte array to a NumPy array
            try:
                array = np.frombuffer(data, dtype=np.uint8)
                self.image = np.reshape(array, (self.height, self.width, 4))

                return self.image
            except:
                print('Error converting data to NumPy array')
    
    def _applyImageCorrection(self, img):
        img = img[...,::-1]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img = cv2.rotate(img, cv2.ROTATE_180)
        return img
    
    

    
    def saveImage(self, name, path):
        cv2.imwrite(path + '/' + name, self.image)
        print('Image saved: ' + path + '/' + name)

    def receive_raw_data(self):
        return self.receiver.receive_raw()

    def receive_raw_image(self):
        return self._getFrame()

    def receive(self):
        return self._applyImageCorrection(self._getFrame())