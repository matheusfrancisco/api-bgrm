
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2
import sys
import os

def identify_text(img):
    try:
        image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        orig = image.copy()
        (H, W) = image.shape[:2]

        (newW, newH) = (320, 320)
        rW = W / float(newW)
        rH = H / float(newH)

        image = cv2.resize(image, (newW, newH))
        (H, W) = image.shape[:2]

        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"]

        net = cv2.dnn.readNet('app/api/miope/frozen_east_text_detection.pb')
        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                    (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)

        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        for y in range(0, numRows):
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            for x in range(0, numCols):

                if scoresData[x] < 0.6:
                    continue

                (offsetX, offsetY) = (x * 4.0, y * 4.0)
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        boxes = non_max_suppression(np.array(rects), probs=confidences)
        kernel_w = (W // 7) | 1
        kernel_h = (H // 7) | 1

        for (startX, startY, endX, endY) in boxes:
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)
            to_blur = orig[startY: endY, startX: endX]
            to_blur = cv2.GaussianBlur(to_blur, (kernel_w, kernel_h), 0)
            orig[startY: endY, startX: endX] = to_blur
        
        _, img_enconded = cv2.imencode(".png", orig)
        
        return img_enconded

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {"status": str(e)}
