import sys

import PyQt6

from Model import MainWindow

if __name__ == '__main__':
	app = PyQt6.QtWidgets.QApplication(sys.argv)
	ex = MainWindow()
	ex.show()
	sys.exit(app.exec())