import datetime
import socket
import numpy as np
import cv2
import select

class Receiver:
    def __init__(self, height, width, host, port, video=None):
        self.host = host
        self.port = port

        self.height = height
        self.width = width

        if(video == "" or video is None):
            self.video = None
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))

            self.socket.listen(1)

            self.inputs = [self.socket]
            self.timeout = 1.0

            self.unity_active = False
        else:
            self.video = cv2.VideoCapture(video)



    def applyImageCorrection(self, img):
        img = img[...,::-1]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img = cv2.rotate(img, cv2.ROTATE_180)
        return img

    def saveImage(self):
        print('Saving images')
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        cv2.imwrite("dump/images/" + now + '.png', self.image)

    def _getNetworkFrame(self):
        readable, _, _ = select.select(self.inputs , [], [], self.timeout)
        s = self.socket

        if s in readable:
            # New client connection
            self.conn, addr = s.accept()
            print('Connected by', addr)
            self.inputs.append(self.conn)
            self.unity_active = True

        elif self.unity_active:
            # Receive the byte array from Unity
            try:
                data = self.conn.recv(self.height * self.width * 4)
            except ConnectionResetError:
                # Unity has stopped sending data
                self.unity_active = False
                print('Unity stopped sending data')
                self.conn.close()
                self.inputs.remove(self.conn)

            if data:
                # Convert the byte array to a NumPy array
                try:
                    array = np.frombuffer(data, dtype=np.uint8)
                    self.image = np.reshape(array, (self.width, self.height, 4))
                    self.image = self.applyImageCorrection(self.image)

                    return self.image

                except:
                    print('Error converting data to NumPy array')
        else:
            print('Waiting for Unity to send data...')

    def _getVideoFrame(self):
        ret, frame = self.video.read()
        if ret:
            return frame
        else:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return self._getVideoFrame()

    def receive(self):
        if (self.video is None or self.video == ""):
            #print('Receiving from network')
            return self._getNetworkFrame()
        else:
            #print('Receiving from video')
            return self._getVideoFrame()