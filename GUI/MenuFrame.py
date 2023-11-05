import tkinter as tk
import customtkinter
import json

class MenuFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = customtkinter.CTkLabel(
            self, text="ITS - Intelligent Transportation System", font=("Arial", 10), anchor=tk.CENTER)
        self.label.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
        self.btn_add_area = customtkinter.CTkButton(
            self, text="Area", command=area_control)
        self.btn_add_area.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
        self.btn_list_rules = customtkinter.CTkButton(
            self, text="Regras", command=list_rules)
        self.btn_list_rules.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)
        self.btn_list_registries = customtkinter.CTkButton(
            self, text="Registros", command=watch_alerts)
        self.btn_list_registries.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)

        self.btn_configure_rules = customtkinter.CTkButton(
            self, text="Configurar", command=configure_rules)
        self.btn_configure_rules.pack(
            side=tk.BOTTOM, pady=10, fill=tk.X, padx=10)
        
        area_control()

def area_control():
    action_context = {
        "action": "add area",
        "payload": None
    }
    with open('context.json', 'w') as outfile:
        json.dump(action_context, outfile)

def rule_control():
    action_context = {
        "action": "add rule",
        "payload": None
    }
    with open('context.json', 'w') as outfile:
        json.dump(action_context, outfile)

def registry_control():
    action_context = {
        "action": "add registry",
        "payload": None
    }
    with open('context.json', 'w') as outfile:
        json.dump(action_context, outfile)
        
def list_rules():
    action_context = {
        "action": "add rule",
        "payload": None
    }
    with open('context.json', 'w') as outfile:
        json.dump(action_context, outfile)

def watch_alerts():
    action_context = {
        "action": "add registry",
        "payload": None
    }
    with open('context.json', 'w') as outfile:
        json.dump(action_context, outfile)

def configure_rules():
    action_context = {
        "action": "add rule",
        "payload": None
    }
    with open('context.json', 'w') as outfile:
        json.dump(action_context, outfile)