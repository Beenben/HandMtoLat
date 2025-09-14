from PyQt5.QtWidgets import QTextEdit, QApplication

class CodeWindow(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setReadOnly(True)
        self.setPlaceholderText("Extracted code will appear here")

    def displayCode(self, code: str):
        # Display the provided code in the text edit widget
        self.setPlainText(code)

    def updateCode(self):
        # Update the displayed code with the current latex_code from the main window
        latex_code = self.main_window.get_latex_code()
        print(latex_code)
        self.displayCode(latex_code)