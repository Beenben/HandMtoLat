from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QDialog
from PyQt5.QtGui import QImage, QPixmap

class PreviewImageButton(QPushButton):
    def __init__(self, main_window):
        super().__init__("Preview Image", main_window)
        self.main_window = main_window
        self.clicked.connect(self.onClick)

    def onClick(self):
        image = self.main_window.get_image()

        # validation
        if image is None:
            return None

        self.showPreview(image)

    def showPreview(self, image):
        # Create a dialog to display the image
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("Image Preview")
        dialog.setGeometry(100, 100, image.shape[1], image.shape[0])

        # Convert the image to QImage
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # Create a label to display the image
        label = QLabel(dialog)
        label.setPixmap(pixmap)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()