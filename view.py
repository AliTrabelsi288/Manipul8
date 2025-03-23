from tkinter import Frame

class View(Frame):
    def __init__(self, parent, os):
        super().__init__(parent)  # Now correctly initializes as a Frame
        self.controller = None
        self.os = os

    def setController(self, controller):
        self.controller = controller
