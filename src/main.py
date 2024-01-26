from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSpinBox, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
import time
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Procesos por Lotes")
        self.setFixedSize(600, 800)
        self.creatUI()

    def creatUI(self):
        #Definimos Layouts
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.hlyt_spin = QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        #Seleccion de N procesos
        self.spn_label = QLabel("Seleccione el número procesos a ejecutar:")
        self.spn_nprocesos = QSpinBox()
        self.spn_nprocesos.setRange(1, 1000)
        self.spn_nprocesos.setValue(1)

        #Boton para crear procesos
        self.btn_crear = QPushButton("Crear Procesos")
        self.btn_crear.clicked.connect(self.createProcess)

        #Agregamos los widgets a los layouts
        self.hlyt_spin.addWidget(self.spn_label)
        self.hlyt_spin.addWidget(self.spn_nprocesos)
        self.mainLayout.addLayout(self.hlyt_spin)
        self.mainLayout.addWidget(self.btn_crear)

    def createProcess(self):

        #Lista de procesos y lista de verificacion de ID
        self.procesos = []
        self.process_ids = []

        #Numero de procesos a crear
        self.nprocesos = self.spn_nprocesos.value()

        #Nombre del programador
        self.hlyt_nombre = QHBoxLayout()
        self.lbl_nombre = QLabel("Nombre del programador: ")
        self.txt_nombre = QLineEdit()

        #Operacion a realizar
        self.hlyt_operacion = QHBoxLayout()
        self.lbl_operacion = QLabel("Operacion a realizar ")
        self.txt_operacion = QComboBox()
        self.txt_operacion.addItems(["+", "-", "*", "/", "%", "**"])
        #Numeros a operar
        self.val_num1 = QLineEdit()
        self.val_num1.setValidator(QDoubleValidator())
        self.val_num2 = QLineEdit()
        self.val_num2.setValidator(QDoubleValidator())

        #Tiempo Maximo Estimado (Mayor a 0)
        self.hlyt_time = QHBoxLayout()
        self.lbl_time = QLabel("Tiempo máximo estimado (segundos): ")
        self.value_time = QSpinBox()
        self.value_time.setRange(1, 1000)
        self.value_time.setValue(1)

        #ID del proceso (debe ser unico)
        self.hlyt_id = QHBoxLayout()
        self.lbl_id = QLabel("ID del proceso: ")
        self.value_id = QLineEdit()
        self.value_id.setValidator(QIntValidator())

        #Boto para agregar proceso
        self.btn_agregar = QPushButton("Agregar proceso")
        self.btn_agregar.clicked.connect(self.addProcess)

        #Agregamos los widgets a los layouts
        self.hlyt_nombre.addWidget(self.lbl_nombre)
        self.hlyt_nombre.addWidget(self.txt_nombre)
        self.hlyt_operacion.addWidget(self.val_num1)
        self.hlyt_operacion.addWidget(self.txt_operacion)
        self.hlyt_operacion.addWidget(self.val_num2)
        self.hlyt_time.addWidget(self.lbl_time)
        self.hlyt_time.addWidget(self.value_time)
        self.hlyt_id.addWidget(self.lbl_id)
        self.hlyt_id.addWidget(self.value_id)
        self.mainLayout.addLayout(self.hlyt_nombre)
        self.mainLayout.addWidget(self.lbl_operacion)
        self.mainLayout.addLayout(self.hlyt_operacion)
        self.mainLayout.addLayout(self.hlyt_time)
        self.mainLayout.addLayout(self.hlyt_id)
        self.mainLayout.addWidget(self.btn_agregar)

        #Ocultamos los widgets de la ventana principal
        self.spn_label.hide()
        self.spn_nprocesos.hide()
        self.btn_crear.hide()

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
                self.executeProcess()
                self.lbl_nombre.hide()
                self.txt_nombre.hide()
                self.lbl_operacion.hide()
                self.txt_operacion.hide()
                self.val_num1.hide()
                self.val_num2.hide()
                self.lbl_time.hide()
                self.value_time.hide()
                self.lbl_id.hide()
                self.value_id.hide()
                self.btn_agregar.hide()
            else:
                pass
        else:
            QMessageBox.warning(self, "Error", "Verifique que no tenga campos vacios", QMessageBox.Ok)

    def executeProcess(self):
        #dividir lotes en grupos de 4
        if len(self.procesos) < 4:
            lote = self.procesos
            self.lotes = [lote]
        else:
            self.lotes = []
            self.lote = []
            for proceso in self.procesos:
                if len(self.lote) < 4:
                    self.lote.append(proceso)
                else:
                    self.lotes.append(self.lote)
                    self.lote = []
                    self.lote.append(proceso)

        lote_en_ejecucion = 0
        lotes_pendientes = len(self.lotes)

        procesos_terminados = []

        #ejecutar procesos por lotes
        while lote_en_ejecucion < len(self.lotes):
            if procesos_terminados != []:
                print("Procesos terminados: ")
                for proceso in procesos_terminados:
                    print("Numero de programa: ", proceso["id"])
                    print("Operacion: ", proceso["operacion"])
                    print("Resultado: ", resultado)
            print("Lote: ", lote_en_ejecucion)
            print("Lotes pendientes: ", lotes_pendientes)
            print("--------------------------------------------------")
            for proceso in self.lotes[lote_en_ejecucion]:
                print("Numero de programa: ", proceso["id"])
                print("Tiempo Maximo Estimado: ", proceso["tiempo"])

            #ejecutar procesos del lote
            for proceso in self.lotes[lote_en_ejecucion]:
                tiempo_transcurrido = 0
                tiempo_restante = proceso["tiempo"]
                print("Nombre del programador: ", proceso["nombre"])
                print("Operacion a realizar: ", proceso["operacion"])
                print("Tiempo Maximo Estimado: ", proceso["tiempo"])
                print("ID del proceso: ", proceso["id"])
                print("Tiempo transcurrido: ", tiempo_transcurrido)
                print("Tiempo restante: ", tiempo_restante)
                time.sleep(proceso["tiempo"])
                resultado = eval(proceso["operacion"])
                print("Resultado:", resultado)
                print("--------------------------------------------------")
                procesos_terminados.append(proceso)
            lote_en_ejecucion += 1
            #Limpiar pantalla
            os.system("cls")
            print("--------------------------------------------------")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())