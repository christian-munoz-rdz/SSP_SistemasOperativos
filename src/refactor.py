from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSpinBox, QComboBox, QMessageBox, QGridLayout
from PyQt5.QtGui import QIntValidator, QDoubleValidator
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
                self.newWindow = ExecuteProcess(self.procesos)
                self.newWindow.show()
                self.hide()
            else:
                pass
        else:
            QMessageBox.warning(self, "Error", "Verifique que no tenga campos vacios", QMessageBox.Ok)


class ExecuteProcess(QWidget):
    def __init__(self, procesos):
        super().__init__()
        self.setWindowTitle("Ejecución de Procesos")
        self.setFixedSize(800, 400)
        self.procesos = procesos
        self.createUI()

    def createUI(self):

        #definir un grid layout
        self.main_layout = QGridLayout()

        self.vlyt_proceso_actual = QVBoxLayout()
        self.lbl_proceso_actual = QLabel("Proceso actual")
        self.lbl_nombre_proceso = QLabel(f"Nombre:  Proceso 1")
        self.lbl_id_proceso = QLabel("ID: 3")
        self.lbl_operacion_proceso = QLabel("Operación: 2 + 3")
        self.lbl_tiempo_proceso = QLabel("Tiempo estimado: 5 segundos")
        self.lbl_tiempo_transcurrido = QLabel("Tiempo transcurrido: 0 segundos")
        self.vlyt_proceso_actual.addWidget(self.lbl_proceso_actual)
        self.vlyt_proceso_actual.addWidget(self.lbl_nombre_proceso)
        self.vlyt_proceso_actual.addWidget(self.lbl_id_proceso)
        self.vlyt_proceso_actual.addWidget(self.lbl_operacion_proceso)
        self.vlyt_proceso_actual.addWidget(self.lbl_tiempo_proceso)
        self.vlyt_proceso_actual.addWidget(self.lbl_tiempo_transcurrido)
        self.vlyt_proceso_actual.setSpacing(1)

        self.main_layout.addLayout(self.vlyt_proceso_actual)

        self.setLayout(self.main_layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExecuteProcess([])
    ex.show()
    sys.exit(app.exec_())
