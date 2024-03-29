from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget,QHBoxLayout, QSpinBox, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QTimer, pyqtSignal
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
                "tiempo_maximo": random.randint(7, 18),
                "tiempo_transcurrido": 0,
                "tiempo_restante": None,
                "tiempo_bloqueo": 0,
                "operacion": f"{random.randint(1, 100)} {random.choice(operaciones)} {random.randint(1, 100)}",
                "resultado": None,
                "estado": "nuevo",
                "tiempo_llegada": 0,
                "tiempo_finalizacion": 0,
                "tiempo_retorno": 0,
                "first_response": False,
                "tiempo_respuesta": 0,
                "tiempo_espera": 0,
                "tiempo_servicio": 0
            })

        #Obtener los resultados de las operaciones
        for proceso in self.procesos:
            proceso['resultado'] = eval(proceso['operacion'])
            proceso['tiempo_restante'] = proceso['tiempo_maximo']

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
        self.lastProcessID = self.procesos[-1]['id'] #ID del último proceso

    def initUI(self):

        globalMaxTime = sum(tiempo['tiempo_maximo'] for tiempo in self.procesos)  # Tiempo máximo global

        # Contenedor central y layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        globalHlayout = QHBoxLayout(centralWidget)
        ready_current_Vlayout = QVBoxLayout()
        finished_Vlayout = QVBoxLayout()
        processtime_Vlayout = QVBoxLayout()
        self.vlyt_btns_spin = QVBoxLayout()

        '''Interfaces de procesos en nuevo, listo, bloqueado y en ejecución'''

        #Labels para mostrar los procesos en nuevo y listo
        self.processesInNewLabel = QLabel("Procesos en Nuevo:", self)
        self.processesInReadyLabel = QLabel("Procesos en Listo:", self)

        #Tabla para mostrar los procesos en listo
        self.processesInReadyTable = QTableWidget(0, 3, self)
        self.processesInReadyTable.setHorizontalHeaderLabels(["ID", "T. Maximo", "T. Restante"])
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
        self.currentProcessTable = QTableWidget(0, 4, self)
        self.currentProcessTable.setHorizontalHeaderLabels(["ID", "Operación", "T. Transcurrido", "T. Restante"])
        self.currentProcessTable.verticalHeader().setVisible(False)
        self.currentProcessTable.setRowCount(0)
        #Labels para mostrar el tiempo de los procesos
        self.currentProcessTimeLabel = QLabel("Tiempo estimado: ", self)
        #self.elapsedTimeLabel = QLabel("Tiempo Transcurrido de Proceso: ", self)
        #self.remainingTimeLabel = QLabel("Tiempo Restante de Proceso: ", self)

        #Añadir widgets al layout de procesos en nuevo, listo, bloqueado y en ejecución
        ready_current_Vlayout.addWidget(self.processesInNewLabel)
        ready_current_Vlayout.addWidget(self.processesInReadyLabel)
        ready_current_Vlayout.addWidget(self.processesInReadyTable)
        ready_current_Vlayout.addWidget(self.processesBlockedLabel)
        ready_current_Vlayout.addWidget(self.processesBlockedTable)
        ready_current_Vlayout.addWidget(self.currentProcessLabel)
        ready_current_Vlayout.addWidget(self.currentProcessTable)
        ready_current_Vlayout.addWidget(self.currentProcessTimeLabel)
        #ready_current_Vlayout.addWidget(self.elapsedTimeLabel)
        #ready_current_Vlayout.addWidget(self.remainingTimeLabel)

        '''Interfaces para mostrar los procesos terminados'''

        #Labels para mostrar tiempos globales
        self.globalMaxTimeLabel = QLabel(f"Tiempo Global Máximo: {globalMaxTime}", self)
        self.globalTimeLabel = QLabel("Tiempo Global Transcurrido: ", self)
        self.finishedProcessLabel = QLabel("Procesos Terminados:", self)
        #Tabla para mostrar los procesos terminados
        self.finishedProcessTable = QTableWidget(0, 3, self)
        self.finishedProcessTable.setHorizontalHeaderLabels(["ID", "Operación", "Resultado"])
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

        ''''Botones de pausa, continuar, interrupción y error'''

        #Crear botones
        self.pauseButton = QPushButton("Pausar", self)
        self.pauseButton.clicked.connect(self.pauseProcess)
        self.continueButton = QPushButton("Continuar", self)
        self.continueButton.clicked.connect(self.continueProcess)
        self.interruptButton = QPushButton("Interrumpir Proceso", self)
        self.interruptButton.clicked.connect(self.interruptProcess)
        self.errorButton = QPushButton("Error en Proceso", self)
        self.errorButton.clicked.connect(self.errorProcess)
        self.btn_agregarProceso = QPushButton("Agregar Nuevo Proceso", self)
        self.btn_agregarProceso.clicked.connect(self.agregarProceso)
        self.bcpTable = QPushButton("Tabla de Procesos", self)
        self.bcpTable.clicked.connect(self.openBCPTable)

        #Añadir botones al layout
        self.vlyt_btns_spin.addWidget(self.pauseButton)
        self.vlyt_btns_spin.addWidget(self.continueButton)
        self.vlyt_btns_spin.addWidget(self.interruptButton)
        self.vlyt_btns_spin.addWidget(self.errorButton)
        self.vlyt_btns_spin.addWidget(self.btn_agregarProceso)
        self.vlyt_btns_spin.addWidget(self.bcpTable)

        # Añadir layouts al contenedor central
        globalHlayout.addLayout(ready_current_Vlayout)
        globalHlayout.addLayout(finished_Vlayout)
        globalHlayout.addLayout(processtime_Vlayout)
        centralWidget.setLayout(globalHlayout)
        globalHlayout.addLayout(self.vlyt_btns_spin)

        #ocultamos el boton de finalizar
        self.finishedButton.hide()

        #Variables para el tiempo
        self.globalTime = 0 #Reloj global

        # Timer para simular el paso del tiempo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop)
        self.timer.start(1000)  # Actualiza cada segundo

    def loop(self):

        # Calcular la suma de las longitudes de las colas de Listo, Bloqueado y si hay un proceso en Ejecución
        total_en_memoria = len(self.processesInReady) + len(self.processesBlocked) + (1 if self.currentProcess else 0)
        
        # Verificar si hay un proceso actual en ejecución
        if self.currentProcess:
            # Actualizar las variables de tiempo de los procesos
            self.globalTime += 1  # Aumenta el reloj global en 1
            self.elapsedTime += 1  # Aumenta el tiempo transcurrido del proceso actual
            self.remainingTime -= 1  # Disminuye el tiempo restante del proceso actual
            self.currentProcess['tiempo_restante'] -= 1  # Disminuye el tiempo restante del proceso actual
            self.currentProcess['tiempo_transcurrido'] += 1 # Aumenta el tiempo transcurrido del proceso actual
            self.currentProcess['tiempo_servicio'] += 1

            self.currentProcessTable.setItem(0, 2, QTableWidgetItem(str(self.currentProcess['tiempo_transcurrido'])))
            self.currentProcessTable.setItem(0, 3, QTableWidgetItem(str(self.currentProcess['tiempo_restante'])))

            # Verificar si el proceso actual ha terminado
            if self.remainingTime <= 0:
                self.currentProcess['estado'] = 'terminado'
                self.currentProcess['tiempo_finalizacion'] = self.globalTime
                self.currentProcess['tiempo_retorno'] = self.currentProcess['tiempo_finalizacion'] - self.currentProcess['tiempo_llegada']
                # Mover el proceso actual a la lista de procesos terminados
                self.finsihedProcesses.append(self.currentProcess)
                # Reiniciar variables para el próximo proceso
                self.currentProcess = None
                self.elapsedTime = 0
                # Intentar cargar el próximo proceso
                self.currentProcessUpdate()
                total_en_memoria -= 1  # Actualizar el total en memoria ya que el proceso terminará

        # Cargar procesos en la lista de listos si hay espacio y aún hay procesos por cargar
        while len(self.processesInReady) < 3 and self.procesos and total_en_memoria < 3:
            proceso_listo = self.procesos.pop(0)
            proceso_listo['estado'] = 'listo'
            proceso_listo['tiempo_llegada'] = self.globalTime
            self.processesInReady.append(proceso_listo)
            total_en_memoria += 1

        for proceso in self.processesInReady:
            proceso['tiempo_espera'] += 1
            proceso['tiempo_servicio'] += 1

        # Si no hay un proceso en ejecución y hay procesos en la lista de listos, cargar el próximo proceso
        if not self.currentProcess and self.processesInReady:
            self.currentProcessUpdate()

        # Actualización de la lógica para el manejo de procesos bloqueados
        nuevos_procesos_bloqueados = []
        for proceso in self.processesBlocked:
            if proceso['tiempo_bloqueo'] > 0:
                proceso['tiempo_bloqueo'] -= 1  # Solo decrementamos si es mayor que 0
                proceso['tiempo_servicio'] += 1

            # Comprobamos si el proceso puede pasar a listo
            if proceso['tiempo_bloqueo'] <= 0:
                proceso['estado'] = 'listo'
                self.processesInReady.append(proceso)  # Actualizamos el total en memoria
            else:
                nuevos_procesos_bloqueados.append(proceso)

        self.processesBlocked = nuevos_procesos_bloqueados

        self.updateRFTables()
        self.updateLabels()

        # Verificar si todos los procesos han terminado
        if not self.procesos and not self.processesInReady and not self.currentProcess and not self.processesBlocked:
            #Limpiar tabla de proceso en ejecución
            self.currentProcessTable.setRowCount(0)

            # Actualizar la tabla de tiempos de los procesos
            self.processTimeTable.setRowCount(len(self.finsihedProcesses))
            for i, proceso in enumerate(self.finsihedProcesses):
                self.processTimeTable.setItem(i, 0, QTableWidgetItem(str(proceso['id'])))
                self.processTimeTable.setItem(i, 1, QTableWidgetItem(str(proceso['tiempo_llegada'])))
                self.processTimeTable.setItem(i, 2, QTableWidgetItem(str(proceso['tiempo_finalizacion'])))
                self.processTimeTable.setItem(i, 3, QTableWidgetItem(str(proceso['tiempo_retorno'])))
                self.processTimeTable.setItem(i, 4, QTableWidgetItem(str(proceso['tiempo_respuesta'])))
                self.processTimeTable.setItem(i, 5, QTableWidgetItem(str(proceso['tiempo_espera'])))
                self.processTimeTable.setItem(i, 6, QTableWidgetItem(str(proceso['tiempo_servicio'])))
            self.finishedButton.show()
            self.timer.stop()

    def updateLabels(self):
        #Actualizar Labels
        self.globalTimeLabel.setText(f"Reloj Global: {self.globalTime}")
        #Si tenemos información para mostrar
        if self.currentProcess:
            #self.elapsedTimeLabel.setText(f"Tiempo Transcurrido de Proceso: {self.elapsedTime}")
            #self.remainingTimeLabel.setText(f"Tiempo Restante de Proceso: {self.remainingTime}")
            self.currentProcessTimeLabel.setText(f"Tiempo estimado: {self.currentProcessTime}")
        else:
            #self.elapsedTimeLabel.setText("Tiempo Transcurrido de Proceso: ")
            #self.remainingTimeLabel.setText("Tiempo Restante de Proceso: ")
            self.currentProcessTimeLabel.setText("Tiempo estimado: ")
        self.processesInNewLabel.setText(f"Procesos en Nuevo: {len(self.procesos)}")
        self.processesInReadyLabel.setText(f"Procesos en Listo: {len(self.processesInReady)}")
        self.finishedProcessLabel.setText(f"Procesos Terminados: {len(self.finsihedProcesses)}")

    def currentProcessUpdate(self):
        if self.processesInReady:
            # Cargar el próximo proceso de la lista de listos
            self.currentProcess = self.processesInReady.pop(0)
            self.currentProcess['estado'] = 'ejecucion'
            if not self.currentProcess['first_response']:
                self.currentProcess['tiempo_respuesta'] = self.globalTime - self.currentProcess['tiempo_llegada']
                self.currentProcess['first_response'] = True
            self.currentProcessTime = self.currentProcess['tiempo_restante']
            self.remainingTime = self.currentProcessTime
            self.elapsedTime = 0  # Reiniciar el tiempo transcurrido para el nuevo proceso

            # Actualizar la tabla del proceso actual
            self.currentProcessTable.setRowCount(1)
            self.currentProcessTable.setItem(0, 0, QTableWidgetItem(str(self.currentProcess['id'])))
            self.currentProcessTable.setItem(0, 1, QTableWidgetItem(self.currentProcess['operacion']))
        else:
            self.currentProcess = None  # No hay más procesos por ejecutar

    def updateRFTables(self):
        # Actualizar la tabla de procesos en listo
        self.processesInReadyTable.setRowCount(len(self.processesInReady))
        for i, proceso in enumerate(self.processesInReady):
            self.processesInReadyTable.setItem(i, 0, QTableWidgetItem(str(proceso['id'])))
            self.processesInReadyTable.setItem(i, 1, QTableWidgetItem(str(proceso['tiempo_maximo'])))
            self.processesInReadyTable.setItem(i, 2, QTableWidgetItem(str(proceso['tiempo_restante'])))

        # Actualizar la tabla de procesos terminados
        self.finishedProcessTable.setRowCount(len(self.finsihedProcesses))
        for i, proceso in enumerate(self.finsihedProcesses):
            self.finishedProcessTable.setItem(i, 0, QTableWidgetItem(str(proceso['id'])))
            self.finishedProcessTable.setItem(i, 1, QTableWidgetItem(proceso['operacion']))
            self.finishedProcessTable.setItem(i, 2, QTableWidgetItem(str(proceso['resultado'])))

        # Actualizar la tabla de procesos bloqueados
        self.processesBlockedTable.setRowCount(len(self.processesBlocked))
        for i, proceso in enumerate(self.processesBlocked):
            self.processesBlockedTable.setItem(i, 0, QTableWidgetItem(str(proceso['id'])))
            self.processesBlockedTable.setItem(i, 1, QTableWidgetItem(str(proceso['tiempo_bloqueo'])))

    def pauseProcess(self):
        self.timer.stop()

    def continueProcess(self):
        self.timer.start()

    def interruptProcess(self):
        if self.currentProcess:
            self.currentProcess['estado'] = 'bloqueado'
            self.currentProcess['tiempo_bloqueo'] = 9  # Tiempo que el proceso permanecerá bloqueado
            self.processesBlocked.append(self.currentProcess)
            self.currentProcess = None
            self.updateRFTables()

    def errorProcess(self):
        if self.currentProcess:
            self.currentProcess['resultado'] = 'error'  # Marcamos el proceso como terminado por error
            self.currentProcess['estado'] = 'terminado'
            self.currentProcess['tiempo_finalizacion'] = self.globalTime
            self.currentProcess['tiempo_retorno'] = self.currentProcess['tiempo_finalizacion'] - self.currentProcess['tiempo_llegada']
            self.finsihedProcesses.append(self.currentProcess)
            self.currentProcess = None
            self.updateRFTables()

    def agregarProceso(self):
        operaciones = ["+", "-", "*", "/", "%", "**"]
        proceso_nuevo = {
            "id": self.lastProcessID + 1,
            "tiempo_maximo": random.randint(7, 18),
            "tiempo_transcurrido": 0,
            "tiempo_restante": None,
            "tiempo_bloqueo": 0,
            "operacion": f"{random.randint(1, 100)} {random.choice(operaciones)} {random.randint(1, 100)}",
            "resultado": None,
            "estado": "nuevo",
            "tiempo_llegada": 0,
            "tiempo_finalizacion": 0,
            "tiempo_retorno": 0,
            "first_response": False,
            "tiempo_respuesta": 0,
            "tiempo_espera": 0,
            "tiempo_servicio": 0
        }
        proceso_nuevo['resultado'] = eval(proceso_nuevo['operacion'])
        proceso_nuevo['tiempo_restante'] = proceso_nuevo['tiempo_maximo']
        self.procesos.append(proceso_nuevo)
        self.lastProcessID += 1
        #QmessageBox para mostrar una tabla con el proceso agregado
        msg = QMessageBox()
        msg.setWindowTitle("Proceso Agregado")
        msg.setText(f"Proceso Agregado: {proceso_nuevo['id']}")
        msg.setInformativeText(f"Operación: {proceso_nuevo['operacion']}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def openBCPTable(self):
        bcp_list = self.finsihedProcesses + [self.currentProcess] + self.processesInReady + self.processesBlocked + self.procesos
        self.bcpTableWindow = BCPTable(bcp_list)
        self.bcpTableWindow.closedSignal.connect(self.onBCPTableClosed)
        self.bcpTableWindow.show()
        self.pauseProcess()

    def onBCPTableClosed(self):
        self.continueProcess()


class BCPTable(QWidget):
    closedSignal = pyqtSignal()
    def __init__(self, procesos=None, parent=None, ):
        super(BCPTable, self).__init__(parent)
        self.setWindowTitle("Tabla de Procesos")
        self.procesos = procesos
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Contenedor principal y layout
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        #Tabla para mostrar los procesos
        self.bcpTable = QTableWidget(0, 12, self)
        self.mainLayout.addWidget(self.bcpTable)
        self.bcpTable.setHorizontalHeaderLabels(["ID", "Estado", "Operación", "Resultado", "T. Bloqueado", "T. LLegada", "T. Finalización",
                                                 "T. Retorno", "T. Espera", "T. Servicio", "T. Restante en CPU", "T. Respuesta"])
        self.bcpTable.verticalHeader().setVisible(False)
        self.bcpTable.setRowCount(0)
        for proceso in self.procesos:
            self.bcpTable.setRowCount(self.bcpTable.rowCount() + 1)
            self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 0, QTableWidgetItem(str(proceso['id'])))
            self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 1, QTableWidgetItem(proceso['estado']))
            if proceso['estado'] == "nuevo":
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 2, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 3, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 4, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 5, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 6, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 7, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 8, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 9, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 10, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 11, QTableWidgetItem(""))
            else:
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 2, QTableWidgetItem(proceso['operacion']))
                if proceso['estado'] == "terminado":
                    if proceso['resultado'] != "error":
                        self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 3, QTableWidgetItem(str(proceso['resultado'])))
                    else:
                        self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 3, QTableWidgetItem("Error"))
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 6, QTableWidgetItem(str(proceso['tiempo_finalizacion'])))
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 7, QTableWidgetItem(str(proceso['tiempo_retorno'])))
                else:
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 3, QTableWidgetItem(""))
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 6, QTableWidgetItem(""))
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 7, QTableWidgetItem(""))
                if proceso['estado'] == "bloqueado":
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 4, QTableWidgetItem(str(proceso['tiempo_bloqueo'])))
                else:
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 4, QTableWidgetItem(""))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 5, QTableWidgetItem(str(proceso['tiempo_llegada'])))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 8, QTableWidgetItem(str(proceso['tiempo_espera'])))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 9, QTableWidgetItem(str(proceso['tiempo_servicio'])))
                self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 10, QTableWidgetItem(str(proceso['tiempo_restante'])))
                if proceso['first_response']:
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 11, QTableWidgetItem(str(proceso['tiempo_respuesta'])))
                else:
                    self.bcpTable.setItem(self.bcpTable.rowCount() - 1, 11, QTableWidgetItem(""))

    def closeEvent(self, event):
        self.closedSignal.emit()  # Emitir la señal al cerrar la ventana
        super(BCPTable, self).closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FirstWindow()
    window.show()
    sys.exit(app.exec_())