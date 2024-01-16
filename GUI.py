import sys
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)  # 设置窗口样式
        self.resize(800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 创建布局
        layout = QVBoxLayout(self)

        # 创建自定义标题栏
        titleBarLayout = QHBoxLayout()

        # 创建占位符
        titleBarLayout.addStretch()

        # 创建最小化按钮
        minimizeButton = QPushButton("-")
        minimizeButton.clicked.connect(self.showMinimized)
        titleBarLayout.addWidget(minimizeButton)

        # 创建关闭按钮
        closeButton = QPushButton("X")
        closeButton.clicked.connect(self.close)
        titleBarLayout.addWidget(closeButton)

        # 将标题栏添加到布局中
        layout.addLayout(titleBarLayout)

        # 创建浏览器组件
        self.webView = QWebEngineView()
        self.webView.load(QUrl("http://www.baidu.com"))

        # 将浏览器组件添加到布局中
        layout.addWidget(self.webView)

        # 设置鼠标跟踪，以便在没有按下鼠标按钮时捕获鼠标移动事件
        self.setMouseTracking(True)

        # 用于窗口拖动的变量
        self.draggable = False
        self.offset = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 250))  # 设置窗口边框颜色和透明度
        painter.drawRoundedRect(self.rect(), 10, 10)  # 绘制圆角矩形边框

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
