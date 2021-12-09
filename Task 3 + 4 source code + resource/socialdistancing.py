import cv2 as cv
import numpy as np
import os
import time

def Check(a,  b):
    dist = ((a[0] - b[0]) ** 2 + 550 / ((a[1] + b[1]) / 2) * (a[1] - b[1]) ** 2) ** 0.5
    calibration = (a[1] + b[1]) / 2
    if 0 < dist < 0.25 * calibration:
        return True
    else:
        return False
def Setup(yolo):
    global net, ln, LABELS
    weights = os.path.sep.join([yolo, "yolov3.weights"])
    config = os.path.sep.join([yolo, "yolov3.cfg"])
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
filename = "testVideo.mp4"
yolo = "yolo"
opname = "output.avi"
cap = cv.VideoCapture(filename)
time1 = time.time()
while(True):
    ret, frame = cap.read()
    if not ret:
        break
    current_img = frame.copy()
    current_img = cv.resize(current_img, (current_img.shape[1]//2,current_img.shape[0]//2), interpolation = cv.INTER_CUBIC)
    video = current_img.shape
    frameno += 1
    if(frameno%2 == 0 or frameno == 1):
        Setup(yolo)
        ImageProcess(current_img)
        Frame = processedImg
        cv.imshow("Image", Frame)
        if create is None:
            fourcc = cv.VideoWriter_fourcc(*'XVID')
            create = cv.VideoWriter(opname, fourcc, 30, (Frame.shape[1], Frame.shape[0]), True)
    create.write(Frame)
    if cv.waitKey(1) & 0xFF == ord('s'):
        break
time2 = time.time()
print("Completed. Total Time Taken: {} minutes".format((time2-time1)/60))
cap.release()
cv.destroyAllWindows()
