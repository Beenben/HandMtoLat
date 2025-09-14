from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QCursor
from PyQt5.QtCore import Qt, QPoint, QRect
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2

#https://github.com/harupy/snipping-tool

class SnippingTool(QWidget):
    def __init__(self, main_window):
        super().__init__()
        root = tk.Tk()

        # defining main window
        self.main_window = main_window

        # finding screen width and height in terms of pixels
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # creating snipping mode
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')

        # finding start and end point
        self.begin = QPoint()
        self.end = QPoint()

        # darken screen
        self.setWindowOpacity(0.3)


        # change cursor to cross for snipping tool
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))

        # makes window borderless
        self.setWindowFlags(Qt.FramelessWindowHint)
        print('Snipping')
        self.show()
        
    
    def paintEvent(self, event):
        # define rectangle colour and border
        brush_color = (128, 128, 255, 100)
        qp = QPainter(self)
        qp.setPen(QPen(QColor('black'), 3))
        qp.setBrush(QColor(*brush_color))

        # draw rectangle
        rect = QRect(self.begin, self.end)
        qp.drawRect(rect)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        # Validate that the cropped image is not dimensionless
        if x1 == x2 or y1 == y2:
            error_message = QMessageBox(self)
            error_message.setWindowTitle("Invalid Selection")
            error_message.setText("The cropped image is empty. Please make a valid selection.")
            error_message.exec_()
            return


        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('capture.png')
        # img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        img = np.array(img)

        # store image in main_window
        self.main_window.set_image(img)

class SnipButton(QPushButton):
    def __init__(self, main_window):
        super().__init__("Snip", main_window)
        self.main_window = main_window
        
        # onclick call function
        self.clicked.connect(self.onClick)

    # activating snipping mode
    def onClick(self):
        self.snipping_tool = SnippingTool(self.main_window)