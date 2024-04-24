import socket
import numpy as np
import time
import cv2
import heapq

UDP_IP="127.0.0.1"
UDP_PORT = 9998
CHUNK_SIZE = 5760*8
NUM_CHUNKS = 20
print(CHUNK_SIZE*NUM_CHUNKS)
assert CHUNK_SIZE*NUM_CHUNKS == 921600


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,CHUNK_SIZE*NUM_CHUNKS*2)
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
  if i >= 5:
    i = 0
    frame2 = frame.reshape(480,640,3)
    cv2.imshow('receiver', frame2)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break



# # This is client code to receive video frames over UDP
# import cv2, socket
# import numpy as np
# import time
# import base64
#
# BUFF_SIZE = 65536
# client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
# host_name = socket.gethostname()
# host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
# print(host_ip)
# port = 9999
# message = b'Hello'
#
# client_socket.sendto(message,(host_ip,port))
# fps,st,frames_to_count,cnt = (0,0,20,0)
# while True:
# 	packet,_ = client_socket.recvfrom(BUFF_SIZE)
# 	data = base64.b64decode(packet,' /')
# 	npdata = np.fromstring(data,dtype=np.uint8)
# 	frame = cv2.imdecode(npdata,1)
# 	frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
# 	cv2.imshow("RECEIVING VIDEO",frame)
# 	key = cv2.waitKey(1) & 0xFF
# 	if key == ord('q'):
# 		client_socket.close()
# 		break
# 	if cnt == frames_to_count:
# 		try:
# 			fps = round(frames_to_count/(time.time()-st))
# 			st=time.time()
# 			cnt=0
# 		except:
# 			pass
# 	cnt+=1
#
