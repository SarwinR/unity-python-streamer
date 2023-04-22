import socket
import select

class Receiver:
    def __init__(self, width, height, host, port):
        # Initialize the properties
        self.host = host
        self.port = port
        self.height = height
        self.width = width
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.inputs = [self.socket]
        self.timeout = 1.0
        self.unity_active = False

    def _getNetworkFrame(self):
        # Check for any new data from Unity
        readable, _, _ = select.select(self.inputs , [], [], self.timeout)
        s = self.socket

        if s in readable:
            # New client connection
            self.conn, addr = s.accept()
            print('Connected to Unity at', addr)
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
            # Waiting for Unity to send data
            print('Waiting for Unity to send data...')

    def receive_raw(self):
        # Get the latest data from Unity
        data = self._getNetworkFrame()
        return data