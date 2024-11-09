'''
import sys

from PyQt6.QtWidgets import QApplication

from gui.window_old import MainWindow



if __name__ == "__main__":
	try:
		app = QApplication(sys.argv)
		window = MainWindow()
		window.resize(800, 600)
		window.show()
		sys.exit(app.exec())
	except Exception as e:
		print(f"An error occurred: {e}")
'''
