import receiver
import cv2

host = '127.0.0.1'
ports = [1110, 1111, 1112,1113,1114, 1115]
receivers = [receiver.Receiver(720, 480, host, port) for port in ports]

while True:
    for r in receivers:
        image = r.receive()
        if image is not None:
            cv2.imshow(str(r.port), image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        