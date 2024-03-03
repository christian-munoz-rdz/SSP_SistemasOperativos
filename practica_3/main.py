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
        self.setWindowTitle('FCFS') # Título de la ventana
        self.procesos = procesos #Lista de procesos
        self.setGeometry(100, 100, 800, 600) # Tamaño de la ventana
        self.initUI() # Llamada al método para crear la interfaz
        self.processesInReady = [] #Lista para guardar los procesos en listo
        self.processesBlocked = [] #Lista para guardar los procesos bloqueados
        self.currentProcess = None #Proceso actual
        self.finsihedProcesses = [] #Lista para guardar los procesos terminados

    def initUI(self):

        globalMaxTime = sum(tiempo['tiempo'] for tiempo in self.procesos)  # Tiempo máximo global

        # Contenedor central y layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        globalHlayout = QHBoxLayout(centralWidget)
        ready_current_Vlayout = QVBoxLayout()
        finished_Vlayout = QVBoxLayout()
        processtime_Vlayout = QVBoxLayout()

        '''Interfaces de procesos en nuevo, listo, bloqueado y en ejecución'''

        #Labels para mostrar los procesos en nuevo y listo
        self.processesInNewLabel = QLabel("Procesos en Nuevo:", self)
        self.processesInReadyLabel = QLabel("Procesos en Listo:", self)

        #Tabla para mostrar los procesos en listo
        self.processesInReadyTable = QTableWidget(0, 3, self)
        self.processesInReadyTable.setHorizontalHeaderLabels(["ID", "T. Maximo", "T. Transcurrido"])
        self.processesInReadyTable.verticalHeader().setVisible(False)
        self.processesInReadyTable.setRowCount(0)

        #Tabla para mostrar procesos bloqueados
        self.processesBlockedLabel = QLabel("Procesos Bloqueados:", self)
        self.processesBlockedTable = QTableWidget(0, 2, self)
        self.processesBlockedTable.setHorizontalHeaderLabels(["ID", "T. Restante"])
        self.processesBlockedTable.verticalHeader().setVisible(False)
        self.processesBlockedTable.setRowCount(0)

        #Tabla y labels para mostrar el proceso en ejecución
        self.currentProcessLabel = QLabel("Proceso actual:", self)
        self.currentProcessTable = QTableWidget(0, 2, self)
        self.currentProcessTable.setHorizontalHeaderLabels(["ID", "Operación"])
        self.currentProcessTable.verticalHeader().setVisible(False)
        self.currentProcessTable.setRowCount(0)
        #Labels para mostrar el tiempo de los procesos
        self.currentProcessTimeLabel = QLabel("Tiempo estimado: ", self)
        self.elapsedTimeLabel = QLabel("Tiempo Transcurrido de Proceso: ", self)
        self.remainingTimeLabel = QLabel("Tiempo Restante de Proceso: ", self)

        #Añadir widgets al layout de procesos en nuevo, listo, bloqueado y en ejecución
        ready_current_Vlayout.addWidget(self.processesInNewLabel)
        ready_current_Vlayout.addWidget(self.processesInReadyLabel)
        ready_current_Vlayout.addWidget(self.processesInReadyTable)
        ready_current_Vlayout.addWidget(self.processesBlockedLabel)
        ready_current_Vlayout.addWidget(self.processesBlockedTable)
        ready_current_Vlayout.addWidget(self.currentProcessLabel)
        ready_current_Vlayout.addWidget(self.currentProcessTable)
        ready_current_Vlayout.addWidget(self.currentProcessTimeLabel)
        ready_current_Vlayout.addWidget(self.elapsedTimeLabel)
        ready_current_Vlayout.addWidget(self.remainingTimeLabel)

        '''Interfaces para mostrar los procesos terminados'''

        #Labels para mostrar tiempos globales
        self.globalMaxTimeLabel = QLabel(f"Tiempo Global Máximo: {globalMaxTime}", self)
        self.globalTimeLabel = QLabel("Tiempo Global Transcurrido: ", self)
        self.finishedProcessLabel = QLabel("Procesos Terminados:", self)
        #Tabla para mostrar los procesos terminados
        self.finishedProcessTable = QTableWidget(0, 4, self)
        self.finishedProcessTable.setHorizontalHeaderLabels(["ID", "Operación", "Resultado", "Tiempo"])
        self.finishedProcessTable.verticalHeader().setVisible(False)
        self.finishedProcessTable.setRowCount(0)

        #Añadir widgets al layout de procesos terminados
        finished_Vlayout.addWidget(self.globalMaxTimeLabel)
        finished_Vlayout.addWidget(self.globalTimeLabel)
        finished_Vlayout.addWidget(self.finishedProcessLabel)
        finished_Vlayout.addWidget(self.finishedProcessTable)

        '''Interfaces para mostrar calculos de los tiempos de los procesos'''

        #Labels para mostrar los tiempos de los procesos
        self.processTimeLabel = QLabel("Tiempo de los Procesos:", self)
        #Tabla para mostrar los tiempos de los procesos
        self.processTimeTable = QTableWidget(0, 7, self)
        self.processTimeTable.setHorizontalHeaderLabels(["ID", "Llegada", "Finalización", "T. Retorno", "T. Respuesta", "T. Espera", "T. Servicio"])
        self.processTimeTable.verticalHeader().setVisible(False)
        self.processTimeTable.setRowCount(0)
        #Boton para finalizar el programa al terminar los procesos
        self.finishedButton = QPushButton("Finalizar", self)
        self.finishedButton.clicked.connect(self.close)

        #Añadir widgets al layout de calculos de los tiempos de los procesos
        processtime_Vlayout.addWidget(self.processTimeLabel)
        processtime_Vlayout.addWidget(self.processTimeTable)
        processtime_Vlayout.addWidget(self.finishedButton)


        # Añadir layouts al contenedor central
        globalHlayout.addLayout(ready_current_Vlayout)
        globalHlayout.addLayout(finished_Vlayout)
        globalHlayout.addLayout(processtime_Vlayout)
        centralWidget.setLayout(globalHlayout)

        #ocultamos el boton de finalizar
        self.finishedButton.hide()

        #Variables para el tiempo
        self.currentProcessTime = 0 #Tiempo del proceso actual
        self.globalTime = 0 #Reloj global
        self.elapsedTime = 0 # Tiempo transcurrido del proceso
        self.remainingTime = 0 # Tiempo restante del proceso
        self.processEnded = False #Variable para saber si el proceso ha terminado

        # Timer para simular el paso del tiempo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop)
        self.timer.start(1000)  # Actualiza cada segundo

    def loop(self):
        #Actualizar las variables de tiempo de los procesos
        self.globalTime += 1 #Aumenta el reloj global en 1
        self.elapsedTime += 1 #Aumenta el tiempo transcurrido del proceso en 1 si el proceso no ha terminado
        self.remainingTime -= 1 #Disminuye el tiempo restante del proceso en 1 si el proceso no ha terminado

        self.updateLabels() #Actualiza las etiquetas con la información de los procesos

        if self.elapsed_time == self.currentProcessTime:


        if self.procesos:
            if len(self.processesInReady) < 3:
                self.processesInReady.append(self.procesos.pop(0))

            if len(self.processesInReady) == 3:
                self.currentProcessUpdate()
                self.processesInReady.append(self.procesos.pop(0))
        else:
            if self.processesInReady:
                self.currentProcessUpdate()

        self.updateRFTables()

    def updateLabels(self):
        #Actualizar Labels
        self.globalTimeLabel.setText(f"Reloj Global: {self.globalTime}")
        self.elapsedTimeLabel.setText(f"Tiempo Transcurrido de Proceso: {self.elapsedTime}")
        self.remainingTimeLabel.setText(f"Tiempo Restante de Proceso: {self.remainingTime}")
        self.currentProcessTimeLabel.setText(f"Tiempo estimado: {self.currentProcessTime}")
        self.processesInNewLabel.setText(f"Procesos en Nuevo: {len(self.procesos)}")
        self.processesInReadyLabel.setText(f"Procesos en Listo: {len(self.processesInReady)}")
        self.finishedProcessLabel.setText(f"Procesos Terminados: {len(self.finsihedProcesses)}")

    def currentProcessUpdate(self):
        self.currentProcess = self.processesInReady.pop(0)
        self.currentProcessTime = self.currentProcess['tiempo']
        self.remainingTime = self.currentProcessTime
        self.currentProcessTable.setRowCount(1)
        self.currentProcessTable.setItem(0, 0, QTableWidgetItem(str(self.currentProcess['id'])))
        self.currentProcessTable.setItem(0, 1, QTableWidgetItem(self.currentProcess['operacion']))
        self.finsihedProcesses.append(self.currentProcess)

    def updateRFTables(self):
        # Actualizar la tabla de procesos en listo
        self.processesInReadyTable.setRowCount(len(self.processesInReady))
        for i, proceso in enumerate(self.processesInReady):
            self.processesInReadyTable.setItem(i, 0, QTableWidgetItem(str(proceso['id'])))
            self.processesInReadyTable.setItem(i, 1, QTableWidgetItem(str(proceso['tiempo'])))
            self.processesInReadyTable.setItem(i, 2, QTableWidgetItem("0"))

        # Actualizar la tabla de procesos terminados
        self.finishedProcessTable.setRowCount(len(self.finsihedProcesses))
        for i, proceso in enumerate(self.finsihedProcesses):
            self.finishedProcessTable.setItem(i, 0, QTableWidgetItem(str(proceso['id'])))
            self.finishedProcessTable.setItem(i, 1, QTableWidgetItem(proceso['operacion']))
            self.finishedProcessTable.setItem(i, 2, QTableWidgetItem(str(eval(proceso['operacion']))))
            self.finishedProcessTable.setItem(i, 3, QTableWidgetItem(str(proceso['tiempo'])))


    def loadProcesses(self): #Carga los procesos en listo (Maximo 3)
        #subset de procesos en listo
        self.ready_processes = self.procesos[:3]
        self.procesos = self.procesos[3:]
        self.endedProcesses = [] #Lista para guardar los procesos terminados
        self.globalTime = 0 #Reloj global
        self.elapsedTime = 0 # Tiempo transcurrido del proceso


        for proceso in self.lotes[self.currentBatch][self.currentProcessIndex:]: #Muestra los procesos pendientes del primer lote
            self.currentBatchList.setText(self.currentBatchList.text() + "\n" + f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}")

    #ssdef currentProcess(self): #carga el proceso al frente de la lista de procesos en listo para ejecutarse

    def updateUI(self): #Actualiza el tiempo de los procesos
        self.updateLabels()
        self.updateTableAndQueue()

    def updateLabels(self): #Actualiza las etiquetas con la información de los procesos


        self.currentProcessIdLabel.setText(f"ID: {self.current_process['id']}")
        self.currentProcessOperationLabel.setText(f"Operación: {self.current_process['operacion']}")
        self.currentProcessTimeLabel.setText(f"Tiempo estimado: {self.current_process['tiempo']}")

    def updateTableAndQueue(self): #Actualiza la tabla de procesos terminados y la lista de procesos pendientes
        if self.remainingTime == 0: #Si el proceso ha terminado
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
                self.elapsedTime = 0 #Reinicia el tiempo transcurrido del proceso a 0
                self.remainingTime = self.current_process['tiempo'] #Reinicia el tiempo restante del proceso al tiempo estimado
            else: #Si no hay procesos pendientes en el lote
                self.currentBatch += 1 #Cambia al siguiente lote
                self.remainingBatches -= 1 #Disminuye el número de lotes pendientes
                if self.currentBatch < len(self.lotes): #Si hay lotes pendientes
                    self.currentProcessIndex = 0 #Reinicia el índice del proceso actual
                    self.current_process = self.lotes[self.currentBatch][self.currentProcessIndex] #Cambia el proceso actual
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FirstWindow()
    window.show()
    sys.exit(app.exec_())