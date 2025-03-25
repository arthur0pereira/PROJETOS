import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 400, 200)

        # Tema Escuro
        self.set_dark_theme()

        # Layout e Widgets
        layout = QVBoxLayout()
        label = QLabel("Insira o URL do vídeo:")
        self.url_input = QLineEdit()
        self.download_button = QPushButton("Baixar")
        self.download_button.clicked.connect(self.baixar_video)

        layout.addWidget(label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.download_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

    def baixar_video(self):
        url = self.url_input.text()
        if url:
            # Lógica de download do vídeo (adicione aqui)
            print(f"Baixando vídeo de: {url}")
        else:
            print("Por favor, insira um URL válido!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())