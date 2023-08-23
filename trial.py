import multiprocessing
import cv2
import time
import numpy as np
import json
import assign_green


def get_output_layers(net):

    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1]
                     for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, classes, COLORS, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

    cv2.putText(img, label, (x-4, y-4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def get_count(image, pid, count):

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    # load model and send as param
    with open('yolo.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet('yolov3.weights',
                          'yolov3.cfg')

    blob = cv2.dnn.blobFromImage(
        image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.4
    nms_threshold = 0.3

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.4:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, conf_threshold, nms_threshold)
    vehicle_count = len(indices)

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, classes, COLORS, class_ids[i], confidences[i], round(
            x), round(y), round(x+w), round(y+h))
    cv2.imwrite(
        "traffic_web/main_page/static/images/%d_capture_side_%d.jpg" % (count, pid), image)
    return vehicle_count


# ******************************************************************************

# ******************************************************************************

# ******************************************************************************

# ******************************************************************************

# ******************************************************************************

# ******************************************************************************

# ******************************************************************************

# ******************************************************************************


def FrameCaptureHelper(args):
    return FrameCapture(*args)

# Function to extract frames


def FrameCapture(path, pid, seconds, count):
    # print("Started", pid)
    success = 0
    cnt = 0
    vidObj = cv2.VideoCapture(path)
    cnt += (30*seconds)  # 30fps
    vidObj.set(1, cnt)
    # vidObj object calls read
    # function extract frames
    success, image = vidObj.read()
    # Saves the frames with pid
    #cv2.imwrite("frame-side%d.jpg" % (pid), image)
    # Resize code
    # print('Original Dimensions : ', image.shape)

    # # resize image
    # resized = cv2.resize(image, (416, 416), interpolation=cv2.INTER_AREA)

    vehicle_cnt = get_count(image, pid, count)

    f = open("buffer.json", "r")
    json_object = json.load(f)
    json_object[str(pid)] = vehicle_cnt
    f = open("buffer.json", "w")
    json.dump(json_object, f)
    f.close()

    # Saves the frames with frame-count

    # print('Resized Dimensions : ', resized.shape)

    return "{count}frame-side{piid}.jpg".format(count=count, piid=pid)


# Driver Code
def run_main(seconds, cnt):
    # Calling the function
    seconds = seconds % 7
    # print(seconds)
    pool = multiprocessing.Pool(4)
    videos = [["inputVideos/sample.mp4", 0, seconds, cnt], ["inputVideos/sample2.mp4", 1, seconds, cnt],
              ["inputVideos/sample3.mp4", 2, seconds, cnt], ["inputVideos/sample4.mp4", 3, seconds, cnt]]
    vals = pool.map(FrameCaptureHelper, videos)
    # print(s)
    # vals.wait()
    # print(vals)  # signifies usage with object count
