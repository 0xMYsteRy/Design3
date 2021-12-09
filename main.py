from __future__ import print_function
import cv2 as cv
import numpy as np
import os
import time

EnterCounter = 0
ExitCounter = 0
cx_p = 0
cx = 0

def Check(a,  b):
    dist = ((a[0] - b[0]) ** 2 + 550 / ((a[1] + b[1]) / 2) * (a[1] - b[1]) ** 2) ** 0.5
    calibration = (a[1] + b[1]) / 2
    if 0 < dist < 0.25 * calibration:
        return True
    else:
        return False
def Setup(yolo):
    global net, ln, LABELS

    weights = os.path.sep.join([yolo, "yolov4-tiny.weights"])
    config = os.path.sep.join([yolo, "yolov4-tiny.cfg"])
    labelsPath = os.path.sep.join([yolo, "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")
    net = cv.dnn.readNetFromDarknet(config, weights)
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

def ImageProcess(image):
    global processedImg
    (H, W) = (None, None)
    frame = image.copy()
    if W is None or H is None:
        (H, W) = frame.shape[:2]
    # blob = cv.dnn.blobFromImage(frame, 1 / 255.0, (512, 512), swapRB=True, crop=False) tiny
    # blob = cv.dnn.blobFromImage(frame, 1 / 255.0, (320, 320), swapRB=True, crop=False) yolo4
    blob = cv.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    starttime = time.time()
    layerOutputs = net.forward(ln)
    stoptime = time.time()
    print("Video is Getting Processed at {:.4f} seconds per frame".format((stoptime-starttime)))
    confidences = []
    outline = []
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            maxi_class = np.argmax(scores)
            confidence = scores[maxi_class]
            if LABELS[maxi_class] == "person":
                if confidence > 0.5:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    outline.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
    box_line = cv.dnn.NMSBoxes(outline, confidences, 0.5, 0.3)

    if len(box_line) > 0:
        flat_box = box_line.flatten()
        pairs = []
        center = []
        status = []
        for i in flat_box:
            (x, y) = (outline[i][0], outline[i][1])
            (w, h) = (outline[i][2], outline[i][3])
            center.append([int(x + w / 2), int(y + h / 2)])
            status.append(False)
        for i in range(len(center)):
            for j in range(len(center)):
                close = Check(center[i], center[j])
                if close:
                    pairs.append([center[i], center[j]])
                    status[i] = True
                    status[j] = True
        index = 0
        for i in flat_box:
            (x, y) = (outline[i][0], outline[i][1])
            (w, h) = (outline[i][2], outline[i][3])

            global EnterCounter, ExitCounter, cx_p, cx

            x1 = w / 2
            y1 = h / 2
            cx_p = cx
            cx = x + x1
            cy = y + y1

            if 280 < cx < 320:
                if cx_p < 280:
                    EnterCounter = EnterCounter + 1
                if cx_p > 320:
                    ExitCounter = ExitCounter + 1


            print("EnterCounter:%s\n" % EnterCounter)
            print("ExitCounter:%s\n" % ExitCounter)

            cv.circle(frame,(int(cx),int(cy)),4,(0,255,0),-1)

            if status[index] == True:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 150), 2)
            elif status[index] == False:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            index += 1

        for h in pairs:
            cv.line(frame, tuple(h[0]), tuple(h[1]), (0, 0, 255), 2)
    processedImg = frame.copy()
create = None
frameno = 0
yolo = "yolo"
opname = "output.avi"
cap = cv.VideoCapture(1)
time1 = time.time()

while(True):
    ret, frame = cap.read()
    if not ret:
        break
    current_img = frame.copy()
    current_img = cv.resize(current_img, (current_img.shape[1],current_img.shape[0]), interpolation = cv.INTER_CUBIC)
    video = current_img.shape
    frameno += 1

    if(frameno%2 == 0 or frameno == 1):
        Setup(yolo)
        ImageProcess(current_img)
        Frame = processedImg

        cv.line(Frame, (300, 00), (300, 600), (0, 0, 255), 1)

        cv.putText(Frame, 'Entrances: %s'%EnterCounter, (10, 50),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
        cv.putText(Frame, 'Exits: %s'%ExitCounter, (10, 70),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv.putText(Frame, 'Current: %s' % (EnterCounter-ExitCounter), (10, 90),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv.imshow("Image", Frame)


    if cv.waitKey(1) & 0xFF == ord('s'):
        break
time2 = time.time()
print("Completed. Total Time Taken: {} minutes".format((time2-time1)/120))
cap.release()
cv.destroyAllWindows()
