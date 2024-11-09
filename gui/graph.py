from typing import Any, Callable, Optional, TypeVar
from enum import StrEnum
from functools import wraps
from uuid import UUID, uuid4

from attrs import define, field, validators, setters
from networkx import Graph
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QStyle, QStyleOption
from PyQt6.QtGui import QMouseEvent, QPaintEvent, QPainter, QPen, QColor

from mc.blocs import BLOCS_ID

TMethod = TypeVar('TMethod', bound=Callable[..., Any])

COLOR_VALIDATOR = validators.instance_of(QColor)
WIDTH_VALIDATOR = validators.and_(validators.instance_of(int), validators.gt(0))
POSITION_VALIDATOR = validators.instance_of(QPoint)


class Mode(StrEnum):
	ADD = 'Ajouter'
	DELETE = 'Supprimer'
	MOVE = 'Déplacer'


@define(kw_only=True)
class Style:
	color: QColor = field(default=QColor('black'), validator=COLOR_VALIDATOR)
	width: int = field(default=1, validator=WIDTH_VALIDATOR)


@define(unsafe_hash=True)
class Node:
	_id: UUID = field(init=False, factory=uuid4, on_setattr=setters.frozen)

	position: QPoint = field(hash=False, validator=validators.instance_of(QPoint))
	style: Style = field(hash=False, validator=validators.instance_of(Style), kw_only=True)


def update(method: TMethod) -> TMethod:
	@wraps(method)
	def wrapper(self: 'QGraph', *args: Any, **kwargs: Any) -> Any:
		result = method(self, *args, **kwargs)
		self.update()
		return result
	return wrapper


@define(slots=False)
class QGraph(QWidget):
	graph: Graph = field(init=False, factory=Graph, on_setattr=setters.frozen)
	mode: Mode = field(init=False, default=Mode.ADD, validator=validators.instance_of(Mode))

	selected_node: Optional[Node] = field(
		init=False,
		default=None,
		validator=validators.optional(validators.instance_of(Node))
	)
	node_color: QColor = field(default=QColor('#CFD5D6'), validator=COLOR_VALIDATOR)
	node_width: int = field(init=False, default=5, validator=WIDTH_VALIDATOR)

	edge_bloc: str = field(default='yellow_concrete', validator=validators.in_(BLOCS_ID))
	edge_color: QColor = field(default=QColor('#F0AF15'), validator=COLOR_VALIDATOR)
	edge_width: int = field(init=False, default=2, validator=WIDTH_VALIDATOR)

	def __attrs_pre_init__(self) -> None:
		super().__init__()

	@update
	def mousePressEvent(self, event: QMouseEvent) -> None:
		if event.button() == Qt.MouseButton.LeftButton:
			position = event.pos()
			closest_node = self._find_closest_node(position)
			self._handle_mode_event(position, closest_node)

	@update
	def mouseMoveEvent(self, event: QMouseEvent) -> None:
		if (self.mode == Mode.MOVE) and self.selected_node:
			self.selected_node.position = event.pos()

	@update
	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		if (self.mode == Mode.MOVE) and (event.button() == Qt.MouseButton.LeftButton):
			self.selected_node = None

	def paintEvent(self, event: QPaintEvent) -> None:
		style_option = QStyleOption() # Why the fuck
		style_option.initFrom(self) # do I have to do this
		painter = QPainter(self) # to get the setStyleSheet method
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, style_option, painter, self) # to finally works ?
		self._draw_edges(painter)
		self._draw_nodes(painter)
		self._highlight_selected_node(painter)

	@update
	def set_mode(self, mode: Mode) -> None:
		if mode != self.mode:
			self.mode = mode
			self.selected_node = None

	@update
	def reset(self) -> None:
		self.mode = Mode.ADD
		self.graph.clear()
		self.selected_node = None

	def _handle_mode_event(self, position: QPoint, closest_node: Optional[Node]) -> None:
		match self.mode:
			case Mode.ADD:
				self._handle_add_mode(position, closest_node)
			case Mode.DELETE:
				self._handle_delete_mode(position, closest_node)
			case Mode.MOVE:
				self._handle_move_mode(closest_node)

	def _handle_add_mode(self, position: QPoint, closest_node: Optional[Node]) -> None:
		if self.selected_node is None:
			if closest_node is None:
				self._add_node(position)
			else:
				self.selected_node = closest_node
		else:
			if closest_node is None:
				new_node = self._add_node(position)
				self._add_edge(self.selected_node, new_node)
			elif closest_node != self.selected_node:
				self._add_edge(self.selected_node, closest_node)
			self.selected_node = None

	def _handle_delete_mode(self, position: QPoint, closest_node: Optional[Node]) -> None:
		if closest_node:
			self._remove_node(closest_node)
		else:
			closest_edge = self._find_closest_edge(position)
			if closest_edge:
				self._remove_edge(closest_edge)

	def _handle_move_mode(self, closest_node: Optional[Node]) -> None:
		self.selected_node = closest_node

	def _add_node(self, position: QPoint) -> Node:
		node = Node(position, style=Style(color=self.node_color, width=self.node_width))
		self.graph.add_node(node)
		return node

	def _remove_node(self, node: Node) -> None:
		self.graph.remove_node(node)

	def _find_closest_node(self, position: QPoint) -> Node | None:
		return min(
			(
				(node, distance)
				for node in self.graph.nodes
				if ((distance := self._distance_to_node(position, node)) < 10)
			),
			default=(None, float('inf')),
			key=lambda item: item[1]
		)[0]

	@staticmethod
	def _distance_to_node(position: QPoint, node: Node) -> int:
		return (position - node.position).manhattanLength()

	def _add_edge(self, node1: Node, node2: Node) -> tuple[Node, Node]:
		self.graph.add_edge(
			node1,
			node2,
			bloc=self.edge_bloc,
			style=Style(color=self.edge_color, width=self.edge_width)
		)
		return node1, node2

	def _remove_edge(self, edge: tuple[Node, Node]) -> None:
		self.graph.remove_edge(*edge)

	def _find_closest_edge(self, position: QPoint) -> tuple[Node, Node] | None:
		return min(
			(
				(edge, distance)
				for edge in self.graph.edges
				if ((distance := self._distance_to_edge(position, edge)) < 10)
			),
			default=(None, float('inf')),
			key=lambda item: item[1]
		)[0]

	@staticmethod
	def _distance_to_edge(position: QPoint, edge: tuple[Node, Node]) -> float:
		p1, p2 = edge[0].position, edge[1].position
		vector_diff = p1 - p2
		twice_area = abs(
			vector_diff.y() * position.x() - vector_diff.x() * position.y() + p1.x() * p2.y() - p1.y() * p2.x()
		)
		edge_length = vector_diff.manhattanLength()
		return twice_area / edge_length if (edge_length > 0) else float('inf')

	def _draw_nodes(self, painter: QPainter) -> None:
		pen = QPen()
		for node in self.graph.nodes:
			node_style = node.style
			pen.setColor(node_style.color)
			pen.setWidth(node_style.width)
			painter.setPen(pen)
			painter.drawPoint(node.position)

	def _draw_edges(self, painter: QPainter) -> None:
		pen = QPen()
		for node1, node2 in self.graph.edges:
			edge_style = self.graph[node1][node2]['style']
			pen.setColor(edge_style.color)
			pen.setWidth(edge_style.width)
			painter.setPen(pen)
			painter.drawLine(node1.position, node2.position)

	def _highlight_selected_node(self, painter: QPainter) -> None:
		pen = QPen()
		if self.selected_node:
			pen.setColor(QColor('#F1AF15'))
			pen.setWidth(5)
			painter.setPen(pen)
			painter.drawEllipse(self.selected_node.position, 10, 10)
