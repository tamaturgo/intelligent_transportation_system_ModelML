import customtkinter
import tkinter as tk
from CONST import outputResolution
class ImageFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) 
        self.canvas = customtkinter.CTkCanvas(self, width = outputResolution[0], height = outputResolution[1])
        self.canvas.pack( fill = "both", expand = True)
        self.canvas.create_rectangle(0, 0, 1000,600, fill="black")
        self.canvas.create_text(400, 300, text="Carregando...", font=("Arial", 20), fill="white")
