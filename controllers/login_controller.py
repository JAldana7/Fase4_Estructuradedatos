# importaciones necesarias
from models.auth_model import Auth
from models.about_info import AboutInfo
from tkinter import messagebox
import tkinter as tk

from views.main_view import MainView
from controllers.main_controller import MainController

# Controlador para la ventana de login
class LoginController:
    def __init__(self, view):
        self.view = view
        self.login_model = Auth()  # Instancia del modelo de autenticación
        self.view.set_controller(self)  # Asignar el controlador a la vista
        self.about_info = AboutInfo()  # Instancia de la clase AboutInfo

    # función para procesar el login
    def procesar_login(self):
        password_input = self.view.txt_password.get()  # Obtener la contraseña ingresada

        # Validar que el campo de contraseña no esté vacío
        if not password_input:
            messagebox.showwarning("Warning", "Please enter your password.")
            return

        # Validar credenciales con el modelo
        if self.login_model.validate_password(password_input):
            messagebox.showinfo("Success", "Welcome to the system!")
            
            self.view.destroy() #cerrar la ventana de Login actual
            
            main_root = tk.Tk()  # Crear la ventana principal de registro
            app_registro = MainView(main_root)
            controller_registro = MainController(app_registro)  # Asocia el controlador a la vista
            main_root.mainloop()
        else:
            messagebox.showerror("Access Denied", "Incorrect password. Please try again.") # Mostrar mensaje de error
            self.view.txt_password.delete(0, 'end')  # Limpiar el campo de contraseña

    # función para mostrar la información de "About"
    def mostrar_about(self):
        informacion = self.about_info.get_info()

        messagebox.showinfo(
            "About",
            informacion,
            parent=self.view
        )