import pytest
from PySide2 import QtCore, QtWidgets, QtGui
import Plotter

@pytest.fixture
def app(qtbot):
	test_plotter_app = Plotter.MainWindow()
	qtbot.addWidget(test_plotter_app)
	return test_plotter_app

def test_placeholder_label(app):
	assert app.canvas.axes.get_title() == "$f\\ (x)={{x}^{2}}$"

def test_label_after_wrong_input_and_no_parenthesis(app, qtbot):
	app.function_line_edit.setText("xx")
	qtbot.keyClick(app.function_line_edit, QtCore.Qt.Key_Return)
	assert app.canvas.axes.get_title() == "Unsupported syntax or invalid input"

def test_label_after_wrong_input_and_parenthesis(app, qtbot):
	app.function_line_edit.setText("x*(x)")
	qtbot.keyClick(app.function_line_edit, QtCore.Qt.Key_Return)
	assert app.canvas.axes.get_title() == "Unsupported syntax or invalid input,\n parenthesis aren't supported"

