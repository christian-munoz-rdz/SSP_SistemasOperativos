from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,
                             QHBoxLayout, QSpinBox, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QTimer
import sys


class ExecuteProcessWindow(QMainWindow):
    def __init__(self, procesos):
        super().__init__()
        self.setWindowTitle(' Procesamiento por Lotes')
        self.procesos = procesos
        self.setFixedSize(700, 600)
        self.divideInBatches()
        self.initUI()

    def initUI(self):

        # Contenedor central y layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        currentProcesVlayout = QVBoxLayout()
        self.currentBatchVlayout = QVBoxLayout()
        globalHlayout = QHBoxLayout(centralWidget)

        # Etiquetas para mostrar información
        self.batchLabel = QLabel("Lote Actual:  | Lotes Pendientes: ", self)
        self.currentProcessLabel = QLabel("Proceso actual:", self)
        self.currentProcessNameLabel = QLabel("Nombre: Proceso: ", self)
        self.currentProcessIdLabel = QLabel("ID: ", self)
        self.currentProcessOperationLabel = QLabel("Operación: ", self)
        self.currentProcessTimeLabel = QLabel("Tiempo estimado: ", self)
        self.elapsedTimeLabel = QLabel("Tiempo Transcurrido de Proceso: ", self)
        self.remainingTimeLabel = QLabel("Tiempo Restante de Proceso: ", self)
        self.globalTimeLabel = QLabel("Reloj Global: 0", self)

        # Tabla para mostrar los procesos terminados
        self.finishedProcessTable = QTableWidget(0, 4, self)
        self.finishedProcessTable.setHorizontalHeaderLabels(["ID", "Operación", "Resultado", ""]) #La ultima columna es para marcar el inicio de un nuevo lote
        self.finishedProcessTable.verticalHeader().setVisible(False)
        self.finishedProcessTable.setRowCount(0)

        #Boton para finalizar el programa al terminar los procesos
        self.finishedButton = QPushButton("Finalizar", self)
        self.finishedButton.clicked.connect(self.close)

        # Añadir widgets al layout
        currentProcesVlayout.addWidget(self.batchLabel)
        currentProcesVlayout.addWidget(self.currentProcessLabel)
        currentProcesVlayout.addWidget(self.currentProcessNameLabel)
        currentProcesVlayout.addWidget(self.currentProcessIdLabel)
        currentProcesVlayout.addWidget(self.currentProcessOperationLabel)
        currentProcesVlayout.addWidget(self.currentProcessTimeLabel)
        currentProcesVlayout.addWidget(self.elapsedTimeLabel)
        currentProcesVlayout.addWidget(self.remainingTimeLabel)
        currentProcesVlayout.addWidget(self.globalTimeLabel)
        currentProcesVlayout.addWidget(self.finishedProcessTable)
        currentProcesVlayout.addWidget(self.finishedButton)

        #Datos de Lote en Ejecución
        self.currentBatchList = QLabel("Procesos pendientes en el lote Actual: ", self)

        self.currentBatchVlayout.addWidget(self.currentBatchList)

        # Añadir layout al contenedor central
        globalHlayout.addLayout(currentProcesVlayout)
        globalHlayout.addLayout(self.currentBatchVlayout)
        centralWidget.setLayout(globalHlayout)

        #ocultamos el boton de finalizar
        self.finishedButton.hide()

        # Timer para simular el paso del tiempo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProcess)
        self.timer.start(1000)  # Actualiza cada segundo

        # Lógica de procesamiento por lotes (se debe implementar)
        self.currentBatch = 0
        self.currentProcessIndex = 0
        self.remainingBatches = len(self.lotes) - 1
        self.current_process = self.lotes[self.currentBatch][self.currentProcessIndex]
        self.endedProcesses = []
        self.globalTime = 0
        self.elapsedTime = 0
        self.remainingTime = self.current_process['tiempo']

        for proceso in self.lotes[self.currentBatch][self.currentProcessIndex:]:
            self.currentBatchList.setText(self.currentBatchList.text() + "\n" + f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}")
    def updateProcess(self):
        self.globalTime += 1
        self.elapsedTime += 1
        self.remainingTime -= 1
        self.globalTimeLabel.setText(f"Reloj Global: {self.globalTime}")
        self.elapsedTimeLabel.setText(f"Tiempo Transcurrido de Proceso: {self.elapsedTime}")
        self.remainingTimeLabel.setText(f"Tiempo Restante de Proceso: {self.remainingTime}")
        self.batchLabel.setText(f"Lote Actual: {self.currentBatch+1} | Lotes Pendientes: {self.remainingBatches}")
        self.currentProcessNameLabel.setText(f"Nombre: {self.current_process['nombre']}")
        self.currentProcessIdLabel.setText(f"ID: {self.current_process['id']}")
        self.currentProcessOperationLabel.setText(f"Operación: {self.current_process['operacion']}")
        self.currentProcessTimeLabel.setText(f"Tiempo estimado: {self.current_process['tiempo']}")

        if self.remainingTime == 0:
            self.currentBatchList.setText("Procesos pendientes en el lote Actual: ")
            rowPosition = self.finishedProcessTable.rowCount()
            self.finishedProcessTable.insertRow(rowPosition)
            self.finishedProcessTable.setItem(rowPosition, 0, QTableWidgetItem(str(self.current_process['id'])))
            self.finishedProcessTable.setItem(rowPosition, 1, QTableWidgetItem(self.current_process['operacion']))
            self.finishedProcessTable.setItem(rowPosition, 2, QTableWidgetItem(str(eval(self.current_process['operacion']))))
            if self.currentProcessIndex == 0:
                self.finishedProcessTable.setItem(rowPosition, 3, QTableWidgetItem("Inicio de Lote"))
            elif self.currentProcessIndex == len(self.lotes[self.currentBatch]) - 1:
                self.finishedProcessTable.setItem(rowPosition, 3, QTableWidgetItem("Fin de Lote"))

            if self.currentProcessIndex < len(self.lotes[self.currentBatch]) - 1:
                self.currentProcessIndex += 1
                self.current_process = self.lotes[self.currentBatch][self.currentProcessIndex]
                for proceso in self.lotes[self.currentBatch][self.currentProcessIndex:]:
                    self.currentBatchList.setText(self.currentBatchList.text() + "\n" + f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}")
                self.elapsedTime = 0
                self.remainingTime = self.current_process['tiempo']
            else:
                self.currentBatch += 1
                self.remainingBatches -= 1
                if self.currentBatch < len(self.lotes):
                    self.currentProcessIndex = 0
                    self.current_process = self.lotes[self.currentBatch][self.currentProcessIndex]
                    for proceso in self.lotes[self.currentBatch][self.currentProcessIndex:]:
                        self.currentBatchList.setText(self.currentBatchList.text() + "\n" + f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}")
                    self.elapsedTime = 0
                    self.remainingTime = self.current_process['tiempo']
                else:
                    self.timer.stop()
                    self.finishedButton.show()

    def divideInBatches(self):
        self.lotes = []
        lote = []
        for proceso in self.procesos:
            lote.append(proceso)
            if len(lote) == 4:
                self.lotes.append(lote)
                lote = []
        if lote:
            self.lotes.append(lote)


if __name__ == "__main__":
    app = QApplication([])
    procesos = [
        {'id': 1, 'nombre': 'Proceso 1', 'operacion': '2+2', 'tiempo': 5},
        {'id': 2, 'nombre': 'Proceso 2', 'operacion': '3+3', 'tiempo': 3},
        {'id': 3, 'nombre': 'Proceso 3', 'operacion': '4+4', 'tiempo': 4},
        {'id': 4, 'nombre': 'Proceso 4', 'operacion': '5+5', 'tiempo': 6},
        {'id': 5, 'nombre': 'Proceso 5', 'operacion': '6+6', 'tiempo': 2},
        {'id': 6, 'nombre': 'Proceso 6', 'operacion': '7+7', 'tiempo': 3},
        {'id': 7, 'nombre': 'Proceso 7', 'operacion': '8+8', 'tiempo': 5},
        {'id': 8, 'nombre': 'Proceso 8', 'operacion': '9+9', 'tiempo': 4},
        {'id': 9, 'nombre': 'Proceso 9', 'operacion': '10+10', 'tiempo': 3},
        {'id': 10, 'nombre': 'Proceso 10', 'operacion': '11+11', 'tiempo': 4},
        {'id': 11, 'nombre': 'Proceso 11', 'operacion': '12+12', 'tiempo': 5},
        {'id': 12, 'nombre': 'Proceso 12', 'operacion': '13+13', 'tiempo': 3},
        {'id': 13, 'nombre': 'Proceso 13', 'operacion': '14+14', 'tiempo': 4},
        {'id': 14, 'nombre': 'Proceso 14', 'operacion': '15+15', 'tiempo': 6},
        {'id': 15, 'nombre': 'Proceso 15', 'operacion': '16+16', 'tiempo': 2}]
    window = ExecuteProcessWindow(procesos)
    window.show()
    sys.exit(app.exec_())