import sys
from pathlib import Path
from typing import Callable, Optional

from attrs import define, field, validators, setters
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QStatusBar, QLabel
from PyQt6.QtGui import QMouseEvent, QCursor, QActionGroup, QAction, QIcon

from gui.graph import Mode, QGraph

MIN_WIDTH = 960
MIN_HEIGHT = 493
ICONS_PATH: Path = Path('icons')


@define
class MainWindow(QMainWindow):
	canvas: QGraph = field(init=False, factory=QGraph, on_setattr=setters.frozen)

	tool_bar: QToolBar = field(init=False, validator=validators.instance_of(QToolBar))

	status_bar: QStatusBar = field(init=False, validator=validators.instance_of(QStatusBar))
	def __attrs_pre_init__(self) -> None:
		super().__init__()

	def __attrs_post_init__(self) -> None:
		self._setup_ui()
		self._setup_canvas()
		self.tool_bar = self._create_toolbar()
		self.addToolBar(self.tool_bar)
		self.status_bar = self._create_statusbar()
		self.setStatusBar(self.status_bar)

	def _setup_ui(self) -> None:
		self.setWindowTitle('HB - GraphDisplay')
		self.setWindowIcon(QIcon(str((ICONS_PATH / 'app.ico').absolute())))
		self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)
		self.setCentralWidget(self.canvas)

	def _setup_canvas(self) -> None:
		self.canvas.setStyleSheet("background-color: #080A0F;")

	def _create_toolbar(self) -> QToolBar:
		toolbar = QToolBar()
		toolbar.toggleViewAction().setEnabled(False)
		toolbar.setIconSize(QSize(16, 16))
		action_group = QActionGroup(self)
		action_group.setExclusive(True)
		self._add_toolbar_actions(action_group, toolbar)
		return toolbar

	def _add_toolbar_actions(self, action_group: QActionGroup, toolbar: QToolBar) -> None:
		for mode in Mode:
			action = self._create_toolbar_action(mode)
			action_group.addAction(action)
			toolbar.addAction(action)

	def _create_toolbar_action(self, mode: Mode) -> QAction:
		return self._configure_action(
			mode.value,
			icon=f'{mode.name.lower()}.svg',
			command=lambda: self.canvas.set_mode(mode)
		)

	def _configure_action(self, text: str, *, icon: str, command: Optional[Callable] = None) -> QAction:
		action = QAction(QIcon(str((ICONS_PATH / icon).absolute())), text, self)
		action.setStatusTip(text)
		action.setCheckable(True)
		if command:
			action.triggered.connect(command)
		return action

	def _create_statusbar(self) -> QStatusBar:
		statusbar = QStatusBar(self)
		return statusbar



app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.show()
app.exec()
