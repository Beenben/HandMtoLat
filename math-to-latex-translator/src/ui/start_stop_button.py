
from PyQt5.QtWidgets import QPushButton, QApplication
import time 

class StartStopButton(QPushButton):
    def __init__(self, main_window):
        super().__init__("Start", main_window)
        self.main_window = main_window
        self.is_running = False
        self.clicked.connect(self.onClick)

    def onClick(self):
        # when running -> stopProcessing()
        # when not running -> startProcessing()
        if self.is_running:
            self.stopProcessing()
        else:
            self.startProcessing()

    def startProcessing(self):
        self.is_running = True
        self.setText("Stop")
        QApplication.processEvents()

        start_time = time.time()
      
        image = self.main_window.get_image()
        latex_code = self.main_window.imageProcessor.process_image(image)

        self.main_window.set_latex_code(latex_code)
        self.is_running = False

        end_time = time.time()
        processing_time = end_time - start_time
        print(f"processing time: {processing_time:.2f} seconds")

        self.main_window.codeWindow.updateCode()
        self.main_window.latexWindow.renderCode()
        self.setText("Start")


    def stopProcessing(self):
        self.is_running = False
        self.setText("Start")
        self.main_window.imageProcessor.stopProcessing()

