from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,
                             QHBoxLayout, QSpinBox, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QTimer
import sys


class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selección de Procesos a Ejecutar")
        self.setFixedSize(300, 200)
        self.createUI()

    def createUI(self):
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.hlyt_spin = QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.spn_label = QLabel("Seleccione el número procesos a ejecutar:")
        self.spn_nprocesos = QSpinBox()
        self.spn_nprocesos.setRange(1, 1000)
        self.spn_nprocesos.setValue(1)

        self.btn_crear = QPushButton("Crear Procesos")
        self.btn_crear.clicked.connect(self.createProcess)

        self.hlyt_spin.addWidget(self.spn_label)
        self.hlyt_spin.addWidget(self.spn_nprocesos)
        self.mainLayout.addLayout(self.hlyt_spin)
        self.mainLayout.addWidget(self.btn_crear)

    def createProcess(self):
        self.newWindow = CreateProcessWindow(self.spn_nprocesos.value())
        self.newWindow.show()
        self.hide()


class CreateProcessWindow(QWidget):
    def __init__(self, nprocesos):
        super().__init__()
        self.setWindowTitle("Creación de Procesos")
        self.setFixedSize(300, 400)
        self.nprocesos = nprocesos
        self.procesos = []
        self.process_ids = []
        self.createUI()

    def createUI(self):
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.lbl_nombre = QLabel("Nombre: ")
        self.txt_nombre = QLineEdit()

        self.lbl_operacion = QLabel("Operación a realizar ")
        self.txt_operacion = QComboBox()
        self.txt_operacion.addItems(["+", "-", "*", "/", "%", "^"])

        self.val_num1 = QLineEdit()
        self.val_num1.setValidator(QDoubleValidator())
        self.val_num2 = QLineEdit()
        self.val_num2.setValidator(QDoubleValidator())

        self.lbl_time = QLabel("Tiempo estimado (segundos): ")
        self.value_time = QSpinBox()
        self.value_time.setRange(1, 1000)
        self.value_time.setValue(1)

        self.lbl_id = QLabel("ID del proceso: ")
        self.value_id = QLineEdit()
        self.value_id.setValidator(QIntValidator())

        self.btn_agregar = QPushButton("Agregar proceso")
        self.btn_agregar.clicked.connect(self.addProcess)

        self.mainLayout.addWidget(self.lbl_nombre)
        self.mainLayout.addWidget(self.txt_nombre)
        self.mainLayout.addWidget(self.lbl_operacion)
        self.mainLayout.addWidget(self.val_num1)
        self.mainLayout.addWidget(self.txt_operacion)
        self.mainLayout.addWidget(self.val_num2)
        self.mainLayout.addWidget(self.lbl_time)
        self.mainLayout.addWidget(self.value_time)
        self.mainLayout.addWidget(self.lbl_id)
        self.mainLayout.addWidget(self.value_id)
        self.mainLayout.addWidget(self.btn_agregar)

    def addProcess(self):
        if self.nprocesos > 0 and self.value_id.text() != "" and self.txt_nombre.text() != "" and self.val_num1.text() != "" and self.val_num2.text() != "":
            if self.value_id.text() not in self.process_ids:
                self.procesos.append({
                    "nombre": self.txt_nombre.text(),
                    "operacion": self.val_num1.text() + self.txt_operacion.currentText() + self.val_num2.text(),
                    "tiempo": self.value_time.value(),
                    "id": self.value_id.text()
                })
                self.process_ids.append(self.value_id.text())
                self.nprocesos -= 1
                self.value_id.clear()
                self.value_time.setValue(1)
                self.val_num1.clear()
                self.val_num2.clear()
                self.txt_nombre.clear()
                self.txt_nombre.setFocus()
            else:
                QMessageBox.warning(self, "Error", "El ID del proceso debe ser único", QMessageBox.Ok)
        elif self.nprocesos == 0:
            respuesta = QMessageBox.question(self, "Confirmación", "Ya Registro todos los procesos, ¿Desea ejecutarlos?", QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                self.newWindow = ExecuteProcessWindow(self.procesos)
                self.newWindow.show()
                self.hide()
            else:
                pass
        else:
            QMessageBox.warning(self, "Error", "Verifique que no tenga campos vacios", QMessageBox.Ok)


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
    app = QApplication(sys.argv)
    window = FirstWindow()
    window.show()
    sys.exit(app.exec_())
