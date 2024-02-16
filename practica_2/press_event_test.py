import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer, Qt

class Cronometro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializarUI()

    def inicializarUI(self):
        self.setWindowTitle('Cronómetro PyQt')
        self.setGeometry(100, 100, 200, 100)
        self.mostrarTiempo = QLabel('00:00:00', self)
        self.mostrarTiempo.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.mostrarTiempo)

        self.tiempo = 0  # Tiempo en segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizarTiempo)
        self.timer.start(1000)  # Actualizar cada segundo

        self.pausado = False

    def actualizarTiempo(self):
        if not self.pausado:
            self.tiempo += 1
            horas = self.tiempo // 3600
            minutos = (self.tiempo % 3600) // 60
            segundos = self.tiempo % 60
            self.mostrarTiempo.setText(f'{horas:02d}:{minutos:02d}:{segundos:02d}')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_P:
            self.pausarCronometro()
        elif e.key() == Qt.Key_C:
            self.continuarCronometro()

    def pausarCronometro(self):
        if not self.pausado:
            self.pausado = True
            self.timer.stop()

    def continuarCronometro(self):
        if self.pausado:
            self.pausado = False
            self.timer.start(1000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Cronometro()
    ventana.show()
    sys.exit(app.exec_())

