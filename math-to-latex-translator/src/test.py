import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import tensorflow as tf

def main():
    # Check for GPU availability
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print("GPUs detected:")
        for gpu in gpus:
            print(f"  - {gpu}")
    else:
        print("No GPUs detected. Using CPU.")

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()