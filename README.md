# Math to LaTeX Translator

This project is a GUI application that translates mathematical expressions from images into LaTeX code. It provides an intuitive interface for users to capture or load images, preview them, and extract LaTeX code seamlessly.

## Features

- **Screen Snipping**: Capture a portion of the screen to extract mathematical expressions.
- **Image Loading**: Load images from your file system for processing.
- **Image Preview**: Preview the loaded images before processing.
- **Processing Control**: Start and stop the image processing with a single button.
- **Code Display**: View the extracted mathematical code and copy it to the clipboard.
- **LaTeX Rendering**: Render the generated LaTeX code for easy viewing.

## Project Structure

```
math-to-latex-translator
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui                     # User interface components
│   │   ├── main_window.py     # Main window of the application
│   │   ├── snip_button.py     # Screen snipping functionality
│   │   ├── load_image_button.py# Load image functionality
│   │   ├── preview_image_button.py # Preview loaded images
│   │   ├── start_stop_button.py # Start/stop processing
│   │   ├── code_window.py      # Display extracted code
│   │   ├── latex_window.py     # Render LaTeX code
│   └── processing              # Image processing components
│       ├── image_processor.py  # Image processing logic
│       ├── usability_features.py # Usability enhancements
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Setup Instructions

**Python 3.12.7**

1. Clone the repository:
   ```
   git clone https://github.com/Beenben/HandMtoLat.git
   ```
2. Navigate to the project directory:
   ```
   cd HandMtoLat
   cd math-to-latex-translator
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application using the following command:
```
python src/main.py
```

Follow the on-screen instructions to capture or load images and extract LaTeX code. (only works for basic equations - see test_set1 directory) 

