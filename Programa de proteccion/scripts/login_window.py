from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from storage import (
    password_exists,
    save_password,
    load_password
)

from dashboard_window import DashboardWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout()

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.button = QPushButton()
        self.button.clicked.connect(self.handle_button)
        self.layout.addWidget(self.button)

        self.central.setLayout(self.layout)

        if password_exists():
            self.mode = "login"
            self.label.setText("Ingrese la contraseña:")
            self.button.setText("Entrar")
        else:
            self.mode = "create"
            self.label.setText("Cree una contraseña:")
            self.button.setText("Guardar")

    def handle_button(self):
        password = self.password_input.text()

        if self.mode == "create":

            if password == "":
                QMessageBox.warning(
                    self,
                    "Error",
                    "La contraseña no puede estar vacía"
                )
                return

            save_password(password)

            QMessageBox.information(
                self,
                "Éxito",
                "Contraseña guardada"
            )

            self.open_main()

        else:
            saved_password = load_password()

            if password == saved_password:
                self.open_main()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Contraseña incorrecta"
                )

    def open_main(self):
        self.main_window = DashboardWindow()
        self.main_window.show()
        self.close()