from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget,QHBoxLayout, QSpinBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer, Qt
import random
import sys


class FirstWindow(QMainWindow):
    def __init__(self): # Constructor de la clase
        super().__init__()
        self.setWindowTitle("Numero de Procesos") # Título de la ventana
        self.setFixedSize(300, 200) # Tamaño de la ventana
        self.createUI()  # Llamada al método para crear la interfaz
        self.procesos = [] #Lista para guardar los procesos

    def createUI(self): #crea la interfaz para seleccionar el número de procesos a ejecutar
        # Contenedor principal y layout
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.hlyt_spin = QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        # Widgets para seleccionar el número de procesos
        #Etiqueta
        self.spn_label = QLabel("Seleccione el número procesos a ejecutar:")
        #Spinbox
        self.spn_nprocesos = QSpinBox()
        self.spn_nprocesos.setRange(1, 1000)
        self.spn_nprocesos.setValue(1)
        #Boton para crear procesos
        self.btn_crear = QPushButton("Crear Procesos")
        self.btn_crear.clicked.connect(self.generateProcess)

        # Añadir widgets al layout
        self.hlyt_spin.addWidget(self.spn_label)
        self.hlyt_spin.addWidget(self.spn_nprocesos)
        self.mainLayout.addLayout(self.hlyt_spin)
        self.mainLayout.addWidget(self.btn_crear)

    def generateProcess(self): #genera n procesos aleatorios
        operaciones = ["+", "-", "*", "/", "%", "**"] #Lista de operaciones
        # Ciclo para generar n procesos
        for i in range(1, self.spn_nprocesos.value()+1):
            self.procesos.append({
                "id": i,
                "tiempo": random.randint(7, 18),
                "operacion": f"{random.randint(1, 100)} {random.choice(operaciones)} {random.randint(1, 100)}"
            })

        # Crear la nueva ventana donde se ejecutarán los procesos
        self.newWindow = ExecuteProcessWindow(self.procesos)
        self.newWindow.show()
        self.close() # Cerrar la ventana actual


class ExecuteProcessWindow(QMainWindow):
    def __init__(self, procesos): # Constructor de la clase
        super().__init__()
        self.setWindowTitle(' Procesamiento por Lotes') # Título de la ventana
        self.procesos = procesos #Lista de procesos
        self.setFixedSize(800, 600) # Tamaño de la ventana
        self.divideInBatches() #Divide los procesos en lotes
        self.initUI() # Llamada al método para crear la interfaz

    def initUI(self):
        # Contenedor central y layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        currentProcesVlayout = QVBoxLayout()
        self.currentBatchVlayout = QVBoxLayout()
        globalHlayout = QHBoxLayout(centralWidget)

        # Etiquetas para mostrar información
        self.batchLabel = QLabel("Lote Actual:  | Lotes Pendientes: ", self)
        self.currentProcessLabel = QLabel("="*15+"\n"+"Proceso actual:"+"\n"+"="*15+"\n", self)
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
        currentProcesVlayout.addWidget(self.currentProcessIdLabel)
        currentProcesVlayout.addWidget(self.currentProcessOperationLabel)
        currentProcesVlayout.addWidget(self.currentProcessTimeLabel)
        currentProcesVlayout.addWidget(self.elapsedTimeLabel)
        currentProcesVlayout.addWidget(self.remainingTimeLabel)
        currentProcesVlayout.addWidget(self.globalTimeLabel)
        currentProcesVlayout.addWidget(self.finishedButton)

        #Datos de Lote en Ejecución
        self.currentBatchList = QLabel("Procesos pendientes en el lote Actual: ", self)
        self.currentBatchVlayout.addWidget(self.currentBatchList)

        # Añadir layout al contenedor central
        globalHlayout.addLayout(currentProcesVlayout)
        globalHlayout.addWidget(self.finishedProcessTable)
        globalHlayout.addLayout(self.currentBatchVlayout)
        centralWidget.setLayout(globalHlayout)

        #ocultamos el boton de finalizar
        self.finishedButton.hide()

        # Timer para simular el paso del tiempo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProcess)
        self.timer.start(1000)  # Actualiza cada segundo

        self.firstProcess() #Inicia el primer proceso

    def firstProcess(self): #Setea los labels y las variables para el primer proceso e inicia el timer
        self.currentBatch = 0 #Lote actual
        self.currentProcessIndex = 0 #Indice del proceso actual
        self.remainingBatches = len(self.lotes) - 1 #Lotes pendientes
        self.current_process = self.lotes[self.currentBatch][self.currentProcessIndex] #Proceso actual
        self.endedProcesses = [] #Lista para guardar los procesos terminados
        self.globalTime = 0 #Reloj global
        self.elapsedTime = 0 # Tiempo transcurrido del proceso
        self.remainingTime = self.current_process['tiempo'] #Tiempo restante del proceso

        for proceso in self.lotes[self.currentBatch][self.currentProcessIndex:]: #Muestra los procesos pendientes del primer lote
            self.currentBatchList.setText(self.currentBatchList.text() + "\n" + f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}")

    def updateProcess(self): #Actualiza el tiempo de los procesos
        self.globalTime += 1 #Aumenta el reloj global en 1
        self.elapsedTime += 1 #Aumenta el tiempo transcurrido del proceso en 1 si el proceso no ha terminado
        self.remainingTime -= 1 #Disminuye el tiempo restante del proceso en 1 si el proceso no ha terminado
        self.updateLabels()
        self.updateTableAndQueue()

    def updateLabels(self): #Actualiza las etiquetas con la información de los procesos
        self.globalTimeLabel.setText(f"Reloj Global: {self.globalTime}")
        self.elapsedTimeLabel.setText(f"Tiempo Transcurrido de Proceso: {self.elapsedTime}")
        self.remainingTimeLabel.setText(f"Tiempo Restante de Proceso: {self.remainingTime}")
        self.batchLabel.setText(f"Lote Actual: {self.currentBatch+1} | Lotes Pendientes: {self.remainingBatches}")
        self.currentProcessIdLabel.setText(f"ID: {self.current_process['id']}")
        self.currentProcessOperationLabel.setText(f"Operación: {self.current_process['operacion']}")
        self.currentProcessTimeLabel.setText(f"Tiempo estimado: {self.current_process['tiempo']}")

    def updateTableAndQueue(self): #Actualiza la tabla de procesos terminados y la lista de procesos pendientes
        if self.remainingTime == 0: #Si el proceso ha terminado
            self.currentBatchList.setText("Procesos pendientes en el lote Actual: ")
            rowPosition = self.finishedProcessTable.rowCount() #Fila en la que se insertará el proceso terminado
            self.finishedProcessTable.insertRow(rowPosition) #Inserta una fila en la tabla
            self.finishedProcessTable.setItem(rowPosition, 0, QTableWidgetItem(str(self.current_process['id']))) #Añade el id del proceso
            self.finishedProcessTable.setItem(rowPosition, 1, QTableWidgetItem(self.current_process['operacion'])) #Añade la operación del proceso
            self.finishedProcessTable.setItem(rowPosition, 2, QTableWidgetItem(str(eval(self.current_process['operacion'])))) #Añade el resultado del proceso

            if self.currentProcessIndex == 0: #Si el proceso es el primero del lote
                self.finishedProcessTable.setItem(rowPosition, 3, QTableWidgetItem("Inicio de Lote"))
            elif self.currentProcessIndex == len(self.lotes[self.currentBatch]) - 1: #Si el proceso es el último del lote
                self.finishedProcessTable.setItem(rowPosition, 3, QTableWidgetItem("Fin de Lote"))

            if self.currentProcessIndex < len(self.lotes[self.currentBatch]) - 1: #Si hay procesos pendientes en el lote
                self.currentProcessIndex += 1 #Aumenta el índice del proceso actual
                self.current_process = self.lotes[self.currentBatch][self.currentProcessIndex] #Cambia el proceso actual
                for proceso in self.lotes[self.currentBatch][self.currentProcessIndex:]: #Muestra los procesos pendientes del lote
                    self.currentBatchList.setText(self.currentBatchList.text() + "\n" + f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}")
                self.elapsedTime = 0 #Reinicia el tiempo transcurrido del proceso a 0
                self.remainingTime = self.current_process['tiempo'] #Reinicia el tiempo restante del proceso al tiempo estimado
            else: #Si no hay procesos pendientes en el lote
                self.currentBatch += 1 #Cambia al siguiente lote
                self.remainingBatches -= 1 #Disminuye el número de lotes pendientes
                if self.currentBatch < len(self.lotes): #Si hay lotes pendientes
                    self.currentProcessIndex = 0 #Reinicia el índice del proceso actual
                    self.current_process = self.lotes[self.currentBatch][self.currentProcessIndex] #Cambia el proceso actual
                    for proceso in self.lotes[self.currentBatch][self.currentProcessIndex:]: #Muestra los procesos pendientes del lote
                        self.currentBatchList.setText(self.currentBatchList.text() + "\n" + f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}")
                    self.elapsedTime = 0 #Reinicia el tiempo transcurrido del proceso a 0
                    self.remainingTime = self.current_process['tiempo'] #Reinicia el tiempo restante del proceso al tiempo estimado
                else: #Si no hay lotes pendientes
                    self.timer.stop() #Detiene el timer
                    self.finishedButton.show() #Muestra el botón de finalizar

    def showEvent(self, event): #Método para asegurar que la ventana tenga el foco cuando se muestra
        super().showEvent(event)
        self.setFocus()  # Asegura que la ventana tenga el foco cuando se muestra

    def focusInEvent(self, event): #Método para asegurar que la ventana tenga el foco cuando se muestra
        super().focusInEvent(event)
        self.setFocus()

    def keyPressEvent(self, event): #Método para manejar los eventos de teclado
        if event.key() == Qt.Key_I: #Si se presiona la tecla I se interrumpe el proceso
            self.interruptProcess()
        elif event.key() == Qt.Key_E: #Si se presiona la tecla E se marca el proceso como error
            self.errorProcess()
        elif event.key() == Qt.Key_P: #Si se presiona la tecla P se pausa el proceso
            self.timer.stop()
        elif event.key() == Qt.Key_C: #Si se presiona la tecla C se continúa el proceso
            self.timer.start()
        else:
            super().keyPressEvent(event)

    def interruptProcess(self):
        if self.lotes and self.currentBatch < len(self.lotes) and self.lotes[self.currentBatch]: # Si hay lotes y el lote actual tiene procesos
            interrupted_process = self.lotes[self.currentBatch].pop(self.currentProcessIndex) #Se interrumpe el proceso actual sacándolo de la lista
            self.lotes[self.currentBatch].append(interrupted_process) #Se añade el proceso interrumpido al final de la lista
            self.moveToNextProcess() #Se pasa al siguiente proceso

    def moveToNextProcess(self):
        # Reinicia la lista de procesos pendientes
        self.currentBatchList.setText("Procesos pendientes en el lote Actual: ")
        if self.lotes and self.currentBatch < len(self.lotes):
            # Verifica si el lote actual aún tiene procesos
            if len(self.lotes[self.currentBatch]) > 0:
                # Ajusta el índice del proceso actual si es necesario
                self.currentProcessIndex = min(self.currentProcessIndex, len(self.lotes[self.currentBatch]) - 1)
                self.current_process = self.lotes[self.currentBatch][self.currentProcessIndex]
                # Actualiza la visualización de procesos pendientes
                for proceso in self.lotes[self.currentBatch][self.currentProcessIndex:]:
                    self.currentBatchList.setText(
                        self.currentBatchList.text() + "\n" + f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}")
                self.updateProcessDisplay()
            else:
                # Si el lote está vacío, intenta mover al siguiente lote si hay más lotes disponibles
                if self.currentBatch + 1 < len(self.lotes):
                    self.currentBatch += 1
                    self.currentProcessIndex = 0
                    self.moveToNextProcess()  # Llama recursivamente para manejar el siguiente lote
                else:
                    # Si no hay más lotes, finaliza el procesamiento
                    self.timer.stop()
                    self.finishedButton.show()

    def updateProcessDisplay(self): #Actualiza las etiquetas con la información del proceso actual
        self.elapsedTime = 0
        self.remainingTime = self.current_process['tiempo']
        self.updateLabels()

    def errorProcess(self):  # Marca el proceso actual como error
        if self.lotes and self.currentBatch < len(self.lotes) and self.lotes[
            self.currentBatch]:  # Si hay lotes y el lote actual tiene procesos
            error_process = self.lotes[self.currentBatch].pop(
                self.currentProcessIndex)  # Se saca el proceso actual de la lista
            self.logErrorProcess(error_process)  # Se marca el proceso como error
            if self.currentProcessIndex >= len(self.lotes[self.currentBatch]):  # Ajusta el índice si es necesario
                self.currentProcessIndex = max(0, len(self.lotes[self.currentBatch]) - 1)
            self.moveToNextProcess()  # Se pasa al siguiente proceso

    def logErrorProcess(self, process):
        rowPosition = self.finishedProcessTable.rowCount()
        self.finishedProcessTable.insertRow(rowPosition)
        self.finishedProcessTable.setItem(rowPosition, 0, QTableWidgetItem(str(process['id'])))
        self.finishedProcessTable.setItem(rowPosition, 1, QTableWidgetItem(process['operacion']))
        self.finishedProcessTable.setItem(rowPosition, 2, QTableWidgetItem("ERROR"))

        # Verificar si el proceso es el inicio o el fin de un lote
        if self.currentProcessIndex == 0:  # Primer proceso del lote
            self.finishedProcessTable.setItem(rowPosition, 3, QTableWidgetItem("Inicio de Lote"))
        if len(self.lotes[self.currentBatch]) == 0 or self.currentProcessIndex == len(self.lotes[self.currentBatch]):  # Último proceso del lote
            self.finishedProcessTable.setItem(rowPosition, 3, QTableWidgetItem("Fin de Lote"))
            if self.remainingBatches > 0:
                self.remainingBatches -= 1  # Ajustar los lotes restantes si es el fin de un lote

    def divideInBatches(self): #divide los procesos en lotes de 3
        self.lotes = [] #Lista para guardar los lotes
        lote = []
        for proceso in self.procesos: #Ciclo para dividir los procesos en lotes
            lote.append(proceso)
            if len(lote) == 3:
                self.lotes.append(lote)
                lote = []
        if lote: #Si quedan procesos
            self.lotes.append(lote)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FirstWindow()
    window.show()
    sys.exit(app.exec_())