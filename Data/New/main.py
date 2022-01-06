import cv2 as cv
import numpy as np
from scipy.spatial import distance
from Detector import detect
MIN_DISTANCE = 50

def measure():
    violate = set()
    # ensure there are *at least* two people detections (required in
    # order to compute our pairwise distance maps)
    if len(results) >= 2:
        # extract all centroids from the results and compute the
        # Euclidean distances between all pairs of the centroids
        centroids = np.array([r[2] for r in results])
        D = distance.cdist(centroids, centroids, metric="euclidean")
        # loop over the upper triangular of the distance matrix
        for i in range(0, D.shape[0]):
            for j in range(i + 1, D.shape[1]):
                # check to see if the distance between any two
                # centroid pairs is less than the configured number
                # of pixels
                if D[i, j] < MIN_DISTANCE:
                    # update our violation set with the indexes of
                    # the centroid pairs
                    violate.add(i)
                    violate.add(j)
    return violate

def draw():
    #result = np.array(results)
    for i in range(0, len(results)-1):
        # extract the bounding box and centroid coordinates, then
        # initialize the color of the annotation
        startX, startY, endX, endY = results[i][1]
        cX, cY = results[i][2]
        color = (0, 255, 0)
        # if the index pair exists within the violation set, then
        # update the color
        if i in violate:
            color = (0, 0, 255)
        # draw (1) a bounding box around the person and (2) the
        # centroid coordinates of the person,
        cv.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        cv.circle(frame, (cX, cY), 5, color, 1)
        # draw the total number of social distancing violations on the
        # output frame
    text = "Social Distancing Violations: {}".format(len(violate))
    cv.putText(frame, text, (10, frame.shape[0] - 25),
                cv.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)


############## MAIN #################
# Load YOLOv4 model and enable GPU
print("[Detector] Loading YOLO...")
yolo = cv.dnn.readNetFromDarknet(".\yolo\yolov4-tiny.cfg", ".\yolo\yolov4-tiny.weights")
# yolo.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
# yolo.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

# Load objects names. Later when we have our own trained model we do not need this
classes = []
with open("./yolo/coco.names", 'r') as f:
    classes = f.read().splitlines()
# print(classes)

print("[Detector] Capturing video stream...")
cap = cv.VideoCapture('./testVideo.mp4')  # change to 0 for live webcam
print("[MAIN] Program is running...")
while True:
    isTrue, frame = cap.read()
    results = detect(frame, yolo, index=classes.index("person"))
    # initialize the set of indexes that violate the minimum social
    # distance
    violate = measure()
    draw()


    # show video:
    resized = cv.resize(frame, (int(frame.shape[1]*0.7), int(frame.shape[0]*0.7)),
                        interpolation=cv.INTER_CUBIC)
    cv.imshow('Video', resized)
    if cv.waitKey(16) & 0xFF == ord('s'):
        print("[MAIN] Exiting program...")
        break
cap.release()
cv.destroyAllWindows()