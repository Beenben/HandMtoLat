from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

import sys
import os

sys.path.append(r'math-to-latex-translator/src')

from ui.snip_button import SnipButton
from ui.load_image_button import LoadImageButton
from ui.preview_image_button import PreviewImageButton
from ui.start_stop_button import StartStopButton
from ui.code_window import CodeWindow
from ui.latex_window import LaTeXWindow
from processing.image_processor import ImageProcessor

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Math to LaTeX Translator")
        self.setGeometry(100, 100, 800, 400)

        self.__image = None
        self.__latex_code = None
        
        self.snipButton = SnipButton(self)
        self.loadImageButton = LoadImageButton(self)
        self.previewImageButton = PreviewImageButton(self)
        self.startStopButton = StartStopButton(self)
        self.codeWindow = CodeWindow(self)
        self.latexWindow = LaTeXWindow(self)
        self.imageProcessor = ImageProcessor()
        # self.usabilityFeatures = UsabilityFeatures()

        layout = QVBoxLayout()
        layout.addWidget(self.snipButton)
        layout.addWidget(self.loadImageButton)
        layout.addWidget(self.previewImageButton)
        layout.addWidget(self.startStopButton)
        layout.addWidget(self.codeWindow)
        layout.addWidget(self.latexWindow)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def minimize(self):
        self.showMinimized()

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image  

    def get_latex_code(self):
        return self.__latex_code

    def set_latex_code(self, latex_code):
        self.__latex_code = latex_code



        

    # def previewImage(self, image):
    #     height, width, channel = image.shape
    #     bytes_per_line = 3 * width
    #     qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    #     pixmap = QPixmap.fromImage(qimage)
    #     self.latexWindow.setPixmap(pixmap)
    #     self.latexWindow.setAlignment(Qt.AlignCenter)