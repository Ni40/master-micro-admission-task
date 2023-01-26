from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide2.QtWidgets import (
    QMainWindow, QApplication, QLineEdit, QDoubleSpinBox, QVBoxLayout, QHBoxLayout, QWidget, QLabel
)
import sys
import matplotlib
from FunctionReader import FunctionReader
import math
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_box_aspect(1)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Window configuration, main layout is a VBox
        self.setWindowTitle('Plotter App')
        placeholder_function = 'x^2'
        placeholder_bounds = (-1, 1)
        main_layout = QVBoxLayout()
        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Configure canvas
        self.canvas = MplCanvas(parent=widget,
                                width=5, height=4, dpi=100)
        main_layout.addWidget(self.canvas)

        # Configure controls section
        controls_layout = QHBoxLayout()
        controls_widget = QWidget(widget)
        font = controls_widget.font()
        font.setPixelSize(14)
        font.setFamily('calibri')
        controls_widget.setFont(font)
        controls_widget.setLayout(controls_layout)
        controls_widget.setMaximumHeight(50)
        main_layout.addWidget(controls_widget)

        # Configure function line edit
        function_line_edit_label = QLabel('f(x)=')
        controls_layout.addWidget(function_line_edit_label)
        self.function_line_edit = QLineEdit(controls_widget)
        self.function_line_edit.setText(placeholder_function)
        self.function_line_edit.returnPressed.connect(self.function_changed)
        controls_layout.addWidget(self.function_line_edit)

        # Configure x lower bound spinner
        lower_x_spinner_label = QLabel('Xmin')
        controls_layout.addWidget(lower_x_spinner_label)
        self.lower_x_spinner = QDoubleSpinBox(controls_widget)
        self.lower_x_spinner.setMinimumWidth(80)
        self.lower_x_spinner.setRange(-math.inf, math.inf)
        self.lower_x_spinner.setValue(placeholder_bounds[0])
        self.lower_x_spinner.valueChanged.connect(self.bounds_changed)
        controls_layout.addWidget(self.lower_x_spinner)

        # Configure x upper bound spinner
        upper_x_spinner_label = QLabel('Xmax')
        controls_layout.addWidget(upper_x_spinner_label)
        self.upper_x_spinner = QDoubleSpinBox(controls_widget)
        self.upper_x_spinner.setMinimumWidth(80)
        self.upper_x_spinner.setRange(-math.inf, math.inf)
        self.upper_x_spinner.setValue(placeholder_bounds[1])
        self.upper_x_spinner.valueChanged.connect(self.bounds_changed)
        controls_layout.addWidget(self.upper_x_spinner)

        # Configure intial function plotted
        self.n_data = 200
        self.x_range = placeholder_bounds
        self.function_reader = FunctionReader(placeholder_function)
        self._plot_ref = None
        self.update_plot()
        self.show()

    def draw_plot(self):
        """
        Draws self.ydata vs self.xdata if valid\n
        otherwise prints error message
        """
        self.canvas.axes.cla()
        self.canvas.axes.grid()
        if self.function_reader.get_function():
            self.canvas.axes.set_title(f"$f\ (x)={self.function_reader.get_string()}$", math_fontfamily='stixsans', size=16)
            self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        else:
            self.canvas.axes.set_title(self.function_reader.get_error(), math_fontfamily='stixsans', size=16)
        self.canvas.draw()

    def update_plot(self):
        """
        Computes new y and x data and refreshes the plot accordingly\n
        ignores the imaginary component of y if exists
        """
        if self.function_reader.get_function():
            self.xdata = [((self.n_data - i) * self.x_range[0] + i * self.x_range[1])
                          / self.n_data for i in range(self.n_data + 1)]
            self.ydata = [self.function_reader.get_function()(x).real
                          for x in self.xdata]
        self.draw_plot()

    def function_changed(self):
        """
        Function to be triggered on pressing enter in the f(x) line edit
        """
        self.function_reader = FunctionReader(self.function_line_edit.text())
        self.update_plot()

    def bounds_changed(self):
        """
        Function to be triggered if one of the spinners' values changes
        """
        # Are the spinners appropriately ordered?
        if self.lower_x_spinner.value() >= self.upper_x_spinner.value():
            # force into order if not in order
            if self.lower_x_spinner.value() != self.x_range[0]:
                self.upper_x_spinner.setValue(self.lower_x_spinner.value() + 1)
            else:
                self.lower_x_spinner.setValue(self.upper_x_spinner.value() - 1)
        self.x_range = (self.lower_x_spinner.value(),
                        self.upper_x_spinner.value())
        self.update_plot()


app = QApplication(sys.argv)
w = MainWindow()
app.exec_()
