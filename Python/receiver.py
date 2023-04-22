import socket
import cv2
import select

class Receiver:
    def __init__(self, width, height, host, port, video=None):
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


    def _getNetworkFrame(self):
        readable, _, _ = select.select(self.inputs , [], [], self.timeout)
        s = self.socket

        if s in readable:
            # New client connection
            self.conn, addr = s.accept()
            print('Connected to', addr)
            self.inputs.append(self.conn)
            self.unity_active = True

        elif self.unity_active:
            # Receive the byte array from Unity
            try:
                data = self.conn.recv(self.width * self.height * 4)
            except ConnectionResetError:
                # Unity has stopped sending data
                self.unity_active = False
                print('Unity stopped sending data')
                self.conn.close()
                self.inputs.remove(self.conn)

            return data
        
        else:
            print('Waiting for Unity to send data...')

    def _getVideoFrame(self):
        ret, frame = self.video.read()
        if ret:
            return frame
        else:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return self._getVideoFrame()

    def receive_raw(self):
        if (self.video is None or self.video == ""):
            return self._getNetworkFrame()
        else:
            return self._getVideoFrame()