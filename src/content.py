import customtkinter as ctk
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QVBoxLayout
import sys

from PyQt5 import QtWidgets
from tkinter import Toplevel, Frame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication
from PyQt5 import QtCore
from NodeGraphQt import NodeGraph, Node

class EmbeddedQtWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        
        # Create a NodeGraph widget
        self.node_graph = NodeGraph()
        
        # Create a QMainWindow to hold the NodeGraph widget
        self.main_window = QMainWindow()
        self.main_window.setCentralWidget(self.node_graph.widget)
        
        # Add QMainWindow to the layout
        self.layout().addWidget(self.main_window)

    def sizeHint(self):
        return QtCore.QSize(800, 600)

# Function to create a Qt application if one doesn't already exist
def get_qt_app():
    if not QApplication.instance():
        return QApplication([])
    return QApplication.instance()

class ContentPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Main Content Area", font=('Roboto', 14)).pack(pady=20)

        # Create an embedded Qt widget
        self.embed_qt_widget()

    def embed_qt_widget(self):
        qt_app = get_qt_app()

        # Create a new toplevel window to host the Qt widget
        self.top = Toplevel(self)
        self.top.geometry("800x600")

        # Create a frame to hold the Qt widget
        self.qt_container = Frame(self.top)
        self.qt_container.pack(fill="both", expand=True)

        # Create the Qt widget and embed it into the Tkinter frame
        self.qt_widget = EmbeddedQtWidget()
        window_container = self.qt_widget.winId()
        container_ptr = int(window_container)
        self.qt_container.tk.call('tk', 'create', 'window', self.qt_container, '-use', container_ptr)

        # Periodically process the Qt events to keep the interface responsive
        self.process_qt_events()

    def process_qt_events(self):
        QApplication.processEvents()
        self.after(10, self.process_qt_events)
