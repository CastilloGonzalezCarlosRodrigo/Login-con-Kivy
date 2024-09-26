from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

# Ruta del archivo de usuarios
USER_DATA_FILE = 'users.txt'


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.build_login_form()

    def build_login_form(self):
        self.clear_widgets()  # Limpiar los widgets existentes para cambiar de formulario

        # Formulario de Login
        self.username = TextInput(hint_text='Usuario', multiline=False)
        self.add_widget(self.username)

        self.password = TextInput(hint_text='Contraseña', multiline=False, password=True)
        self.add_widget(self.password)

        self.login_button = Button(text='Iniciar sesión')
        self.login_button.bind(on_press=self.validate_credentials)
        self.add_widget(self.login_button)

        self.register_button = Button(text='Registrarse')
        self.register_button.bind(on_press=self.build_register_form)  # Cambiar a formulario de registro
        self.add_widget(self.register_button)

        self.message = Label(text='')
        self.add_widget(self.message)

    def build_register_form(self, instance):
        self.clear_widgets()  # Limpiar los widgets existentes para cambiar de formulario

        # Formulario de Registro
        self.new_username = TextInput(hint_text='Nuevo usuario', multiline=False)
        self.add_widget(self.new_username)

        self.new_password = TextInput(hint_text='Nueva contraseña', multiline=False, password=True)
        self.add_widget(self.new_password)

        self.register_button = Button(text='Registrar')
        self.register_button.bind(on_press=self.register_user)
        self.add_widget(self.register_button)

        self.back_button = Button(text='Volver al inicio de sesión')
        self.back_button.bind(on_press=lambda x: self.build_login_form())  # Volver al login
        self.add_widget(self.back_button)

        self.message = Label(text='')
        self.add_widget(self.message)

    def validate_credentials(self, instance):
        username = self.username.text
        password = self.password.text

        if self.check_credentials(username, password):
            self.message.text = 'Inicio de sesión exitoso'
            self.message.color = (0, 1, 0, 1)  # Verde
        else:
            self.message.text = 'Credenciales incorrectas'
            self.message.color = (1, 0, 0, 1)  # Rojo

    def check_credentials(self, username, password):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                for line in f:
                    user, pwd = line.strip().split(',')
                    if user == username and pwd == password:
                        return True
        except FileNotFoundError:
            return False
        return False

    def register_user(self, instance):
        username = self.new_username.text
        password = self.new_password.text

        if self.user_exists(username):
            self.message.text = 'El usuario ya existe'
            self.message.color = (1, 0, 0, 1)  # Rojo para error
        else:
            self.save_user(username, password)
            self.message.text = 'Usuario registrado con éxito'
            self.message.color = (0, 1, 0, 1)  # Verde para éxito
            self.build_login_form()  # Volver al formulario de inicio de sesión tras registro exitoso

    def user_exists(self, username):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                for line in f:
                    user, _ = line.strip().split(',')
                    if user == username:
                        return True
        except FileNotFoundError:
            return False
        return False

    def save_user(self, username, password):
        with open(USER_DATA_FILE, 'a') as f:
            f.write(f'{username},{password}\n')


class LoginApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    LoginApp().run()
