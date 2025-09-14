from PyQt5.QtWidgets import QPushButton, QFileDialog
import cv2 

class LoadImageButton(QPushButton):
    def __init__(self, main_window):
        super().__init__("Load Image", main_window)
        self.main_window = main_window
        self.clicked.connect(self.onClick)

    def onClick(self):
         
        file_name = self.openFileExplorer()
        if file_name:
            image = cv2.imread(file_name)
            self.main_window.set_image(image)
            
            # self.main_window.previewImage(image)

    def openFileExplorer(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg)", options=options)

        if file_name:
            return file_name
        else:
            return None
