import socket
import numpy as np
import time
import cv2
import heapq

UDP_IP="127.0.0.1"
UDP_PORT = 9999
CHUNK_SIZE = 576
NUM_CHUNKS = 1600
assert CHUNK_SIZE*NUM_CHUNKS == 921600


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

i = 0
frame = np.zeros(NUM_CHUNKS*CHUNK_SIZE, dtype=np.uint8)
print(frame)
while True:
    data, addr = sock.recvfrom(CHUNK_SIZE+2)
    sequence_number = int.from_bytes(data[0:2], "big")
    frame_data = data[2:]

    a = sequence_number*CHUNK_SIZE
    b = (sequence_number+1)*CHUNK_SIZE
    frame[a:b] = np.frombuffer(frame_data, dtype=np.uint8)
    i += 1
    if not i%NUM_CHUNKS:
      frame2 = frame.reshape(480,640,3)
      cv2.imshow('receiver', frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
