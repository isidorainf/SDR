import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(project_root, 'scripts')
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

os.chdir(project_root)

from PySide6.QtWidgets import QApplication
from login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

