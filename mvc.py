from model import Model
from view import View
from controller import Controller
from tkinter import Tk

class MVC(Tk):
    def __init__(self, os_system):
        try:
            super().__init__()

            self.title('Manipul8')

            # Create a model
            model = Model()

            # Create a view and place it on the root window
            view = View(self, os_system)
            view.grid(row=0, column=0, padx=10, pady=10)

            # Create a controller
            controller = Controller(model, view)

            # Set the controller to view
            view.setController(controller)

            # Link the model back to the view for updates
            model.set_view(view)
        except Exception as error:
            print(f"Initialization Error: {error}")
