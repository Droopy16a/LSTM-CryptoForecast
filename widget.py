import numpy as np
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
from model import TensorModel
import matplotlib.dates as mdates

class PlotWidget(QMainWindow):
    def __init__(self, crypto_instance, timestamp=[0, 10, 100], data=[0, 1, 2], color="#81ff4f", currency="BTC", tt="d"):
        super().__init__()
        self.crypto = crypto_instance
        self.timestamp = timestamp
        self.data = data
        self.color = color
        self.currency = currency
        self.tt = tt
        self.initUI()
        self.tm = TensorModel()
        self.fetch_and_update()

    def initUI(self):
        self.setWindowTitle(f'{self.currency} Currency')
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        central_widget = QWidget()
        central_widget.setStyleSheet("""
            background-color: #1e1e1e;
            border: 1px solid #3c3c3c;
            border-radius: 8px;
        """)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #252525; border: none;")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 4, 0)
        top_bar_layout.addStretch()

        close_button = QPushButton("X")
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: #cccccc;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #d70000;
                color: #ffffff;
            }
        """)
        close_button.clicked.connect(self.close)
        top_bar_layout.addWidget(close_button)

        button_bar = QWidget()
        button_bar.setStyleSheet("background-color: #252525; border: none;")
        button_bar_layout = QHBoxLayout(button_bar)
        button_bar_layout.setContentsMargins(4, 4, 4, 4)
        button_bar_layout.setSpacing(4)

        timestamps = [("Hourly", "h"), ("Daily", "d"), ("Weekly", "w"), ("Monthly", "m"), ("Yearly", "y")]
        self.timestamp_buttons = {}
        for label, value in timestamps:
            btn = QPushButton(label)
            btn.setFixedSize(60, 24)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3c3c3c;
                    color: #cccccc;
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QPushButton:hover {
                    background-color: #007acc;
                    color: #ffffff;
                }
                QPushButton:checked {
                    background-color: #005f99;
                    color: #ffffff;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, v=value: self.change_timestamp(v))
            self.timestamp_buttons[value] = btn
            button_bar_layout.addWidget(btn)
        
        self.timestamp_buttons[self.tt].setChecked(True)
        button_bar_layout.addStretch()

        self.figure = Figure(facecolor='none')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: transparent;")
        
        main_layout.addWidget(top_bar)
        main_layout.addWidget(button_bar)
        main_layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111, facecolor='none')
        self.update_plot()

        self.old_pos = None
        self.canvas.setMouseTracking(True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_and_update)
        self.timer.start(10000)

    def change_timestamp(self, new_timestamp):
        for value, btn in self.timestamp_buttons.items():
            btn.setChecked(value == new_timestamp)
        
        self.tt = new_timestamp
        self.fetch_and_update()

    def fetch_and_update(self):
        print(f"fetch_and_update: self.tt={self.tt}")
        try:
            data = self.crypto.get_crypto(self.currency, timestamp=self.tt)
            print(f"fetch_and_update: crypto.timestamp={self.crypto.timestamp}")
            self.timestamp = [datetime.fromtimestamp(i[0]) for i in data['prices']]
            self.data = [i[1] for i in data['prices']]
            lst = self.tm.predict(data)
            self.color = "#81ff4f" if lst == 2 else "#ff4f4f" if lst == 0 else "#ffff4f"
            self.update_plot()
        except Exception as e:
            print(f"Error fetching data: {e}")

    def update_plot(self):
        self.ax.clear()

        self.ax.plot(self.timestamp, self.data, color=self.color, linewidth=2)

        if self.tt in ["h", "d"]:
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        else:
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))

        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        self.ax.grid(True, color='#3c3c3c', linestyle='--', alpha=0.5)
        self.ax.set_title(f'{self.currency} Currency : {self.data[-1]} USD',
                        color='#cccccc', fontfamily='Segoe UI')
        self.ax.spines['top'].set_color('#3c3c3c')
        self.ax.spines['right'].set_color('#3c3c3c')
        self.ax.spines['left'].set_color('#3c3c3c')
        self.ax.spines['bottom'].set_color('#3c3c3c')
        self.ax.tick_params(colors='#cccccc', labelsize=10)
        self.ax.tick_params(axis='x', rotation=45)

        self.figure.tight_layout()
        self.canvas.draw()


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None