import tkinter as tk
import customtkinter


class BottomMenu(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title_label = customtkinter.CTkLabel(
            self, text="### Clique em uma regra para exibir informações", font=("Arial", 16), anchor="w")
        self.title_label.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
        self.information_label = customtkinter.CTkLabel(
            self, text="", font=("Arial", 14), anchor="w")
        self.information_label.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)

        self.btn_group = customtkinter.CTkFrame(self)
        self.btn_group.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)

        self.btn_edit_rules = customtkinter.CTkButton(
            self.btn_group, text="Editar", command=edit_rules)
        self.btn_edit_rules.pack(side=tk.LEFT, pady=10, fill=tk.X, padx=10)

        self.btn_delete_rules = customtkinter.CTkButton(
            self.btn_group, text="Deletar", command=delete_rules, fg_color="red")
        self.btn_delete_rules.pack(side=tk.LEFT, pady=10, fill=tk.X, padx=10)



def edit_rules():
    print("Edit rules")

def delete_rules():
    print("Delete rules")