import tkinter as tk
import customtkinter


class SecundaryMenuFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.area_menu = customtkinter.CTkFrame(self)
        self.label = customtkinter.CTkLabel(
            self.area_menu, text="Nova área de interesse", font=("Arial", 10), anchor=tk.CENTER)
        self.label.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
        self.entry_name = customtkinter.CTkEntry(
            self.area_menu)
        self.entry_name.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
        self.entry_description = customtkinter.CTkEntry(
            self.area_menu)
        self.entry_description.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
        self.btn_add_area = customtkinter.CTkButton(
            self.area_menu, text="Desenhar", command=draw_area_click)
        self.btn_add_area.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)

        self.save_area_menu = customtkinter.CTkFrame(self.area_menu)
        self.save_area_menu.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
        self.btn_save_area = customtkinter.CTkButton(
            self.save_area_menu, text="Salvar", command=save_area_click)
        self.btn_save_area.pack(side=tk.LEFT, pady=10, fill=tk.X, padx=10)
        self.btn_cancel_area = customtkinter.CTkButton(
            self.save_area_menu, text="Cancelar", command=cancel_area_click)
        self.btn_cancel_area.pack(side=tk.LEFT, pady=10, fill=tk.X, padx=10)

    def active_area_menu(self):
        self.area_menu.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
    
    def disable_area_menu(self):
        self.area_menu.pack_forget()




def draw_area_click():
    pass

def save_area_click():
    pass

def cancel_area_click():
    pass