from PyQt5.QtWidgets import QMainWindow, QApplication
from Program_files.menu_window import MenuWindow
from questions import all_questions, category_names
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window1 = MenuWindow(all_questions, category_names)
    app.exec_()
