import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QTime, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Duración total del temporizador (por ejemplo, 1 hora)
        self.totalDuration = QTime(1, 0)

        self.initUI()

    def initUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)

        # Tiempo transcurrido, empieza en 0
        self.elapsedTime = QTime(0, 0)

        # Configura el temporizador para actualizar cada segundo
        self.timer.start(1000)

        # Etiquetas para mostrar los tiempos
        self.elapsedLabel = QLabel(self)
        self.remainingLabel = QLabel(self)
        self.elapsedLabel.setAlignment(Qt.AlignCenter)
        self.remainingLabel.setAlignment(Qt.AlignCenter)
        self.updateTimer()

        # Diseño vertical para el widget central
        layout = QVBoxLayout()
        layout.addWidget(self.elapsedLabel)
        layout.addWidget(self.remainingLabel)

        # Establece el widget central y su diseño
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.setWindowTitle('Temporizador PyQt')
        self.setGeometry(300, 300, 250, 150)
        self.show()

    def updateTimer(self):
        self.elapsedTime = self.elapsedTime.addSecs(1)
        remainingTime = QTime(0, 0).addSecs(self.totalDuration.secsTo(self.elapsedTime) * -1)

        self.elapsedLabel.setText(f"Tiempo Transcurrido: {self.elapsedTime.toString('hh:mm:ss')}")
        self.remainingLabel.setText(f"Tiempo Restante: {remainingTime.toString('hh:mm:ss')}")

        if self.elapsedTime >= self.totalDuration:
            self.timer.stop()
            self.remainingLabel.setText("Tiempo Restante: 00:00:00")

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
