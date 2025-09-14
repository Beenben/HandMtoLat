import cv2
import numpy as np
from functools import cmp_to_key
import sys

from keras.src.layers import BatchNormalization
from keras.src.ops import shape
from sklearn.model_selection import train_test_split
import tensorflow as tf
import keras
from keras import layers
from keras import ops   
import matplotlib.pyplot as plt

class ImageProcessor:
    __model_path = r'math-to-latex-translator\src\models\test_set_1_classification.keras'
    __model = keras.models.load_model(__model_path, compile=True)

    dic = {
        "-": r"-",
        "(": r"(",
        ")": r")",
        "+": r"+",
        "=": r"=",
        "times": r"\times",
        "0": r"0",
        "1": r"1",
        "2": r"2",
        "3": r"3",
        "4": r"4",
        "5": r"5",
        "6": r"6",
        "7": r"7",
        "8": r"8",
        "9": r"9",
        "div": r"\div", 
        "y": r"y", 
        "X": r"x", 
        "C": r"c", 
        "M": r"m"
    }

    dic_list = [v for k, v in dic.items()]
    __latexToNums = {k: v for v, k in enumerate(dic_list)}
    __numsToLatex = {v: k for v, k in enumerate(dic_list)}


    def process_image(self, image):
        bounding_boxes = self.bounding_box_detection(image)
        symbols = self.symbol_detection(bounding_boxes, image)
        latex_code = self.generate_latex(symbols)
        return latex_code
    
    def bounding_box_detection(self, image):
        # Implement bounding box detection logic here
        bboxes = []

        # store state of img after each stage
        img_stages = []
        
        #turn image into grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_stages.append(gray)
        
        #binarisation
        ret, binary_inv = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        img_stages.append(binary_inv)

        #dilation
        kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3, 8))
        imgDilate = cv2.dilate(binary_inv, kernel_dilate, iterations=3)
        img_stages.append(imgDilate)

        #finding contours
        contours, _ = cv2.findContours(imgDilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        #find bboxes    
        for contour in contours:
            bbox = cv2.boundingRect(contour)
            bboxes.append(bbox)
                
        #draw bbox on img
        bbox_img = image.copy()
        for bbox in bboxes:
            x, y, w, h = bbox
            start_point = (x, y)
            end_point = (x + w, y + h)
            cv2.rectangle(bbox_img, start_point, end_point, (0, 255, 0), 2)
        img_stages.append(bbox_img) 

        #order bboxes by x value
        bboxes = sorted(bboxes, key=lambda x: x[0])

        arrayLen = len(bboxes)
        noOverlapBBoxes = bboxes.copy()

        # iterate through all bounding box combinations 
        # improvement: use x coordinate and width and y coordinate and height 
        # to check for possible overlaps
        for i in range(arrayLen):
            for j in range(arrayLen):
                if j == i:
                    pass
                else:
                    IoA = self.IntersectionOverArea(bboxes[i], bboxes[j])
                    if IoA > 0.8:
                        try:
                            noOverlapBBoxes.remove(bboxes[i])
                        except:
                            pass

        return noOverlapBBoxes 

    def extract_math_code(self, image):
        # Implement math code extraction logic here
        pass

    def IntersectionOverArea(self, bbox1, bbox2):
        #finding top left and bottom right corner of first bbox
        x1, y1, w1, h1 = bbox1
        A1 = (x1, y1)
        B1 = (x1 + w1, y1 + h1)

        #finding top left and bottom right corner of the second bbox
        x2, y2, w2, h2 = bbox2
        A2 = (x2, y2)
        B2 = (x2 + w2, y2 + h2)

        # x determine the (x, y)-coordinates of the intersection rectangle
        xA = max(A1[0], A2[0])
        yA = max(A1[1], A2[1])
        xB = min(B1[0], B2[0])
        yB = min(B1[1], B2[1])

        # area of the intersection rectangle
        
        interArea = max(0, xB-xA+1) * max(0, yB-yA+1)

        # area of the first input box
        Area1 = (B1[0] - A1[0] +1)*(B1[1] - A1[1]+1)

        # area of intersection/area of box1
        IoA = interArea/float(Area1)
        return IoA

    def symbol_detection(self, bboxes, image):
        """
        Crops symbols from an image based on bounding boxes, preprocesses them,
        and returns the processed symbols ready for input into a model.

        Parameters:
        - image: The input image from which symbols will be cropped.
        - bboxes: A list of bounding boxes, where each box is represented as (x, y, w, h).

        Returns:
        - symbols: A list of processed symbol images with the shape (45, 45, 1).
        """

        symbols = []  # List to store the processed symbols
        threshold_value = 150  # Threshold value for binary thresholding
        max_value = 255  # Maximum value for thresholding

        for bbox in bboxes:
            # Unpack the bounding box coordinates
            x, y, w, h = bbox

            # Crop the symbol from the image using the bounding box
            symbol = image[y:y+h, x:x+w]

            # Convert the cropped symbol to grayscale
            symbol = cv2.cvtColor(symbol, cv2.COLOR_BGR2GRAY)

            # Calculate the padding to make the image square
            side_length = max(w, h)
            top_pad = (side_length - h) // 2
            bottom_pad = top_pad
            left_pad = (side_length - w) // 2
            right_pad = left_pad

            # Add padding to the image
            symbol = cv2.copyMakeBorder(symbol, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=255)

            # Resize the symbol to a fixed size of 45x45 pixels
            symbol = cv2.resize(symbol, (45, 45), interpolation=cv2.INTER_AREA)

            # Apply binary thresholding to the symbol
            _, symbol = cv2.threshold(symbol, threshold_value, max_value, cv2.THRESH_BINARY)

            # Reshape the symbol to add an extra dimension (45, 45, 1) to fit the model input shape
            symbol = symbol.reshape((45, 45, 1))

            # Append the processed symbol to the list
            symbols.append(symbol)

        return symbols  # Return the list of reshaped symbols
    
    def generate_latex(self, symbols):

        classified_symbols = []
        for i in range(len(symbols)):

            symbol = symbols[i]
            predicted_symbol_class = self.__model.predict(tf.expand_dims(symbol, axis=0))
            symbol_class = self.__numsToLatex[predicted_symbol_class.argmax(axis=-1)[0]]
            classified_symbols.append(symbol_class)
        
        latex_string = ''.join(classified_symbols)
        return latex_string
    
    def stopProcessing(self):
        print("terminating program")
        sys.exit()


    

    
