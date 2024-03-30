import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Renk Tespiti ve Maskeleme")
        self.setGeometry(100, 100, 1000, 600)

        self.original_image_label = QLabel()
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setFixedSize(800, 500)

        self.result_image_label = QLabel()
        self.result_image_label.setAlignment(Qt.AlignCenter)
        self.result_image_label.setFixedSize(800, 500)

        self.load_button = QPushButton("Resim Yükle  /  Upload a picture")
        self.load_button.clicked.connect(self.load_image)

        self.refresh_button = QPushButton("Yenile   /   Refresh")
        self.refresh_button.clicked.connect(self.refresh_image)

        # HSV değerlerini girebileceğimiz textbox'lar
        self.h_min_edit = QLineEdit()
        self.h_max_edit = QLineEdit()
        self.s_min_edit = QLineEdit()
        self.s_max_edit = QLineEdit()
        self.v_min_edit = QLineEdit()
        self.v_max_edit = QLineEdit()

        # Layout oluştur
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("H Min:"))
        hbox1.addWidget(self.h_min_edit)
        hbox1.addWidget(QLabel("H Max:"))
        hbox1.addWidget(self.h_max_edit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("S Min:"))
        hbox2.addWidget(self.s_min_edit)
        hbox2.addWidget(QLabel("S Max:"))
        hbox2.addWidget(self.s_max_edit)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel("V Min:"))
        hbox3.addWidget(self.v_min_edit)
        hbox3.addWidget(QLabel("V Max:"))
        hbox3.addWidget(self.v_max_edit)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.load_button)
        hbox4.addWidget(self.refresh_button)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.original_image_label)
        image_layout.addWidget(self.result_image_label)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addLayout(hbox3)
        layout.addLayout(hbox4)
        layout.addLayout(image_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def load_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            self.filename = filename
            self.refresh_image()

    def refresh_image(self):
        try:
            image = cv2.imread(self.filename)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except  Exception as e:
            print("Lütfen resim seçip tekrar deneyin.")
        try:
            # HSV değerlerini al
            h_min = int(self.h_min_edit.text())
            h_max = int(self.h_max_edit.text())
            s_min = int(self.s_min_edit.text())
            s_max = int(self.s_max_edit.text())
            v_min = int(self.v_min_edit.text())
            v_max = int(self.v_max_edit.text())

            lower_color = np.array([h_min, s_min, v_min])
            upper_color = np.array([h_max, s_max, v_max])

            # Renk maskeleme işlemi
            hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsv_image, lower_color, upper_color)
            result = cv2.bitwise_and(rgb_image, rgb_image, mask=mask)

            # Resimleri yeniden boyutlandırma
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_image_original = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888).scaled(800, 500, Qt.KeepAspectRatio)
            q_image_result = QImage(result.data, w, h, bytes_per_line, QImage.Format_RGB888).scaled(800, 500, Qt.KeepAspectRatio)

            # QPixmap'e dönüşüm ve QLabel'e gösterim
            pixmap_original = QPixmap.fromImage(q_image_original)
            pixmap_result = QPixmap.fromImage(q_image_result)
            self.original_image_label.setPixmap(pixmap_original)
            self.result_image_label.setPixmap(pixmap_result)
        except  Exception as e:
            print("Lütfen sadece sayısal bir değer girin.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
