from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import io

class LaTeXWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent

        self.setLayout(QVBoxLayout())
        self.label = QLabel(self)
        self.layout().addWidget(self.label)
        self.setPlaceholderText("Rendered LaTeX code will appear here")

    def setPlaceholderText(self, text: str) -> None:
        self.label.setText(text)

    def renderCode(self) -> None:
        latex_code = self.main_window.get_latex_code()

        if latex_code is None or latex_code == "":
            return None

        # Generate LaTeX using Matplotlib
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"${latex_code}$", fontsize=20, ha='center', va='center')
        ax.axis('off')

        # Save the figure to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        # Load the image from the BytesIO object
        image = QImage()
        image.loadFromData(buf.read(), 'PNG')

        # Convert the QImage to QPixmap and display it in the QLabel
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)