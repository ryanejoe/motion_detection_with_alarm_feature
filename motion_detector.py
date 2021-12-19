
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
from playsound import playsound
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-x", "--alarm", type=str,help="do you wanna enable alarms, diabled by default")
args = vars(ap.parse_args())
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
firstFrame = None
while True:
	frame = vs.read()
	text = "Unoccupied"
	if frame is None:
		break
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	if firstFrame is None:
		firstFrame = gray
		continue
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	for c in cnts:
		if cv2.contourArea(c) < args["min_area"]:
			continue
		if args.get("alarm") == "yes" and text == "Occupied":
			playsound(r'C:\Users\glych\OneDrive\Desktop\main tool\MUSIC.wav')
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"
		x = "YES"
		print("yes")
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
