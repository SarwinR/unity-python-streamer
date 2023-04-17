import receiver
import cv2

host = '127.0.0.1'
ports = 1234
r = receiver.Receiver(720, 480, host, ports)


while True:
    image = r.receive()
    if image is not None:
        cv2.imshow(str(r.port), image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        