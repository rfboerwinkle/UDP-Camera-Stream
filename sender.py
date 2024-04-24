import socket
import numpy as np
import cv2
import time


# Specify IP information
UDP_IP = '127.0.0.1'
UDP_PORT = 9998
CHUNK_SIZE = 5760*8
NUM_CHUNKS = 20
assert CHUNK_SIZE*NUM_CHUNKS == 921600

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,CHUNK_SIZE*NUM_CHUNKS*2)

cap = cv2.VideoCapture(0) # Capture video element
i = -1
while(True):
  i += 1
  i %= NUM_CHUNKS
  if not i:
    ret, frame = cap.read()
  d = frame.flatten()
  s = d.tobytes()
  sequence_number = i.to_bytes(2, "big")
  start_idx = i * CHUNK_SIZE
  end_idx = (i + 1) * CHUNK_SIZE
  chunk = s[start_idx:end_idx]
  sock.sendto(sequence_number + chunk, (UDP_IP, UDP_PORT))

  time.sleep(0.0002)


cap.release()
cv2.destroyAllWindows()




# # This is server code to send video frames over UDP
# import cv2, socket
# import numpy as np
# import time
# import base64
#
# BUFF_SIZE = 65536
# server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
# host_name = socket.gethostname()
# host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
# print(host_ip)
# port = 9999
# socket_address = (host_ip,port)
# server_socket.bind(socket_address)
# print('Listening at:',socket_address)
#
# vid = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam
# fps,st,frames_to_count,cnt = (0,0,20,0)
#
# while True:
# 	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
# 	print('GOT connection from ',client_addr)
# 	WIDTH=400
# 	while(vid.isOpened()):
# 		_,frame = vid.read()
# 		# frame = imutils.resize(frame,width=WIDTH)
# 		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
# 		message = base64.b64encode(buffer)
# 		print(len(message))
# 		server_socket.sendto(message,client_addr)
# 		frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
# 		cv2.imshow('TRANSMITTING VIDEO',frame)
# 		key = cv2.waitKey(1) & 0xFF
# 		if key == ord('q'):
# 			server_socket.close()
# 			break
# 		if cnt == frames_to_count:
# 			try:
# 				fps = round(frames_to_count/(time.time()-st))
# 				st=time.time()
# 				cnt=0
# 			except:
# 				pass
# 		cnt+=1
#
