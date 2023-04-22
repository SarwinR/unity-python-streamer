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
        
        # If video is not None, initialize the OpenCV video capture object
        if video is not None:
            self.video = cv2.VideoCapture(video)
            self.receiver = None
        # Otherwise, initialize the network receiver object
        else:
            self.receiver = receiver.Receiver(width, height, host, port)




    # Get a frame from the video capture object
    def _getVideoFrame(self):
        ret, frame = self.video.read()
        if ret:
            return frame
        else:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return self._getVideoFrame()

    # Get a frame from the network receiver object
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

    # Apply image correction to the given image
    def _applyImageCorrection(self, img):
        img = img[...,::-1]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img = cv2.rotate(img, cv2.ROTATE_180)
        return img




    # Save the current image to the given path with the given name
    def saveImage(self, name, path):
        cv2.imwrite(path + '/' + name, self.image)
        print('Image saved: ' + path + '/' + name)

    # Receive the raw data from the network receiver object
    def receive_raw_data(self):
        if(self.video is not None):
            return self._getVideoFrame()
        else:
            return self.receiver.receive_raw()

    # Receive a raw image from the network receiver object
    def receive_raw_image(self):
        if(self.video is not None):
            return self._getVideoFrame()
        else:
            return self._getFrame()

    # Receive a corrected image from the network receiver object
    def receive(self):
        if(self.video is not None):
            return self._getVideoFrame()
        else:
            frame = self._getFrame()
            if(frame is None):
                return None
            else:
                return self._applyImageCorrection(frame)