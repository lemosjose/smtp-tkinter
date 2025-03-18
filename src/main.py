import tkinter as tk
from tkinter import ttk, Text

import DNSOutput
import VPSConnect


class SMTPConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Configurador SMTP")
        self.geometry("650x700")

        self.entries = {}

        # Tabs
        tab_control = ttk.Notebook(self)
        vps_tabs = [ttk.Frame(tab_control) for _ in range(10)]
        for i, tab in enumerate(vps_tabs, 1):
            tab_control.add(tab, text=f"VPS {i}")
        tab_control.pack(pady=10, fill="x")

        # Labels & Inputs
        self.entries["IP"] = self.create_label_entry("IP da sua VPS", 50)
        self.entries["user"] = self.create_label_entry("Usuário da VPS", 90)
        self.entries["password"] = self.create_label_entry("Senha do Usuário na VPS", 130, password=True)
        self.entries["port"] = self.create_label_entry("Porta SSH utilizada", 170)
        self.entries["Domínio"] = self.create_label_entry("Domínio/Subdomínio", 210)
        self.create_label_entry("Novo usuário SMTP", 250)
        self.create_label_entry("Senha do novo usuário SMTP", 290, password=True)

        # Output Textbox
        tk.Label(self, text="Output dos Comandos").place(x=10, y=330)
        self.output_text = Text(self, height=6, width=80)
        self.output_text.place(x=10, y=350)

        # Buttons
        self.create_button("Conectar à VPS", 450, self.connect_vps)
        self.create_button("Criar Usuário do SMTP", 480, self.create_smtp_user)
        self.create_button("Configurar o Serviço SMTP", 510, self.configure_smtp)
        self.create_button("Obter Registros do Domínio", 540, self.get_domain_records)

    def create_label_entry(self, label_text, y_pos, password=False):
        """Helper function to create labels and entry fields."""
        tk.Label(self, text=label_text).place(x=10, y=y_pos)
        entry = tk.Entry(self, width=50, show="*" if password else "")
        entry.place(x=200, y=y_pos)
        return entry

    def create_button(self, text, y_pos, command):
        """Helper function to create buttons."""
        btn = tk.Button(self, text=text, command=command)
        btn.place(x=10, y=y_pos)

    # Dummy functions for button actions
    def connect_vps(self):
        connectAtributes = [self.entries["IP"], self.entries["user"], self.entries["password"], self.entries["port"]]
        connection = VPSConnect.ConnectionObj(*connectAtributes)
        connection.connect()
        self.output_text.insert(tk.END, f" {connection.runUname()} \n")

        

        

    def create_smtp_user(self):
        self.output_text.insert(tk.END, "Creating SMTP user...\n")

    def configure_smtp(self):
        self.output_text.insert(tk.END, "Configuring SMTP...\n")

    def get_domain_records(self):
        dominio = self.entries["Domínio"].get()

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"\n Domínios: \n {DNSOutput.getRecords(dominio)} DNS Utilizado:Goole")


if __name__ == "__main__":
    app = SMTPConfigApp()
    app.mainloop()

