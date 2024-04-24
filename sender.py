import socket
import numpy as np
import cv2
import time


# Specify IP information
UDP_IP = '127.0.0.1'                  
UDP_PORT = 9999
CHUNK_SIZE = 576
NUM_CHUNKS = 1600
assert CHUNK_SIZE*NUM_CHUNKS == 921600

cap = cv2.VideoCapture(0) # Capture video element
i = -1
while(True):
  i += 1
  i %= NUM_CHUNKS
  if not i:
    ret, frame = cap.read()
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  d = frame.flatten()
  s = d.tobytes()
  sequence_number = i.to_bytes(2, "big")
  start_idx = i * CHUNK_SIZE
  end_idx = (i + 1) * CHUNK_SIZE
  chunk = s[start_idx:end_idx]
  sock.sendto(sequence_number + chunk, (UDP_IP, UDP_PORT))

  # time.sleep(0.0002)


cap.release()
cv2.destroyAllWindows()
