import os
import sys

# Asegurar que el directorio de cv_analyzer y subcarpetas estén en sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ui.streamlit_ui import main

if __name__ == "__main__":
    main()

