from model import Model
from view import View
from controller import Controller
from tkinter import Tk

class MVC(Tk):
    def __init__(self, os_system):
        try:
            super().__init__()

            self.title('Manipul8')

            model = Model()

            view = View(self, os_system)
            view.grid(row=0, column=0, padx=10, pady=10)

            controller = Controller(model, view)

            view.setController(controller)

            model.set_view(view)
        except Exception as error:
            print(f"Initialization Error: {error}")
