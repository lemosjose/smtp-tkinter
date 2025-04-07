import tkinter as tk
from tkinter import ttk, Text
# Assuming you have these imports elsewhere for your button commands
# import VPSConnect
from DNSOutput import getRecords
import VPSConnect

class SMTPConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Configurador SMTP")
        self.geometry("650x700") # Adjusted height slightly

        # --- Main data storage ---
        # Key: tab index (1 to 10)
        # Value: dictionary holding widgets/vars for that tab
        self.tab_data = {}

        # --- Tabs ---
        # Store the notebook control so action methods can access it
        self.tab_control = ttk.Notebook(self)

        for i in range(1, 11): # Loop 1 to 10
            # Create a new Frame for each tab
            tab_frame = ttk.Frame(self.tab_control, padding="10") # Add padding inside tab
            self.tab_control.add(tab_frame, text=f"VPS {i}")

            self.tab_data[i] = {}


            _, self.tab_data[i]["IP_var"] = self.create_label_entry(tab_frame, "IP da sua VPS", 10)
            _, self.tab_data[i]["user_var"] = self.create_label_entry(tab_frame, "Usuário da VPS", 50)
            _, self.tab_data[i]["password_var"] = self.create_label_entry(tab_frame, "Senha do Usuário na VPS", 90, password=True)
            _, self.tab_data[i]["port_var"] = self.create_label_entry(tab_frame, "Porta SSH utilizada", 130)
            _, self.tab_data[i]["Domínio_var"] = self.create_label_entry(tab_frame, "Domínio/Subdomínio", 170)
            _, self.tab_data[i]["SMTPUser_var"] = self.create_label_entry(tab_frame, "Novo usuário SMTP", 210)
            _, self.tab_data[i]["SMTPPassword_var"] = self.create_label_entry(tab_frame, "Senha do novo usuário SMTP", 250, password=True)

            # Note: Using .place inside packed/gridded frames can be less reliable for resizing.
            # Consider using .grid() or .pack() for widgets within tab_frame if layout becomes an issue.

        self.tab_control.pack(pady=10, padx=10, fill="both", expand=True)

        # --- Widgets OUTSIDE the tabs (shared) ---

        # Output Textbox Frame (to allow placing label and text box together)
        output_frame = ttk.Frame(self)
        output_frame.pack(fill="x", padx=10, pady=(0, 5)) # Pack below notebook

        tk.Label(output_frame, text="Output dos Comandos").pack(anchor='w')
        self.output_text = Text(output_frame, height=8, width=80) # Increased height slightly
        self.output_text.pack(fill="x", expand=True)


        # Button Frame (to group buttons)
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        # Create buttons - Parent is button_frame, use pack or grid for layout
        # Use lambda to ensure the command is called without arguments immediately
        ttk.Button(button_frame, text="Conectar à VPS", command=lambda: self.connect_vps()).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Criar Usuário do SMTP", command=lambda: self.create_smtp_user()).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Configurar o Serviço SMTP", command=lambda: self.configure_smtp()).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Obter Registros do Domínio", command=lambda: self.get_domain_records()).pack(side=tk.LEFT, padx=5)

        # Removed self.create_button helper for simplicity with pack layout
        # If you prefer .place(), you can adapt create_button to use self as parent


    # --- MODIFIED Helper function ---
    def create_label_entry(self, parent, label_text, y_pos, password=False):
        """Helper function to create labels and entry fields within a specific parent."""
        # Using place as in original code, relative to 'parent'
        tk.Label(parent, text=label_text).place(x=10, y=y_pos)

        # Create a variable specific to this entry
        entry_var = tk.StringVar()

        entry = tk.Entry(parent, width=50, show="*" if password else "", textvariable=entry_var)
        entry.place(x=200, y=y_pos)

        # Return the widget AND its variable
        return entry, entry_var

    # --- Essa parte é gerada por IA 

    def _get_current_tab_data(self):
        """Helper to get the data dictionary for the currently selected tab."""
        try:
            # Get the widget path of the selected tab
            selected_tab_widget_path = self.tab_control.select()
            # Get the 0-based index of that tab
            current_index_0based = self.tab_control.index(selected_tab_widget_path)
            # Convert to 1-based index used in self.tab_data keys
            current_index_1based = current_index_0based + 1

            if current_index_1based in self.tab_data:
                return self.tab_data[current_index_1based]
            else:
                self.output_text.insert(tk.END, f"Error: No data found for tab index {current_index_1based}.\n")
                return None
        except tk.TclError:
             self.output_text.insert(tk.END, "Error: No tab selected or invalid tab state.\n")
             return None
        except Exception as e:
            self.output_text.insert(tk.END, f"Error getting current tab data: {e}\n")
            return None


    def connect_vps(self):
        current_data = self._get_current_tab_data()
        if not current_data: return # Stop if error fetching data

        self.output_text.delete(1.0, tk.END) 
        try:
            connAtributes = [
                current_data["IP_var"].get(),
                current_data["user_var"].get(), 
                current_data["password_var"].get(),
                current_data["port_var"].get(),
            ]
            connection = VPSConnect.ConnectionObj(*connAtributes)

            connection.connect()
            
            self.output_text.insert(tk.END, f"Conectado na VPS {connection.runUname()}")

        except Exception as e:
            self.output_text.insert(tk.END, f"Falhou, erro: {e}")

    def create_smtp_user(self):
        current_data = self._get_current_tab_data()
        if not current_data: return

        try:
            smtp_user = current_data["SMTPUser_var"].get()
            smtp_pass = current_data["SMTPPassword_var"].get()
            ip = current_data["IP_var"].get() # Might need IP/User/Pass for connection
            # ... get other needed vars ...

            self.output_text.insert(tk.END, f"Creating SMTP user '{smtp_user}' on {ip} for Tab {self.tab_control.index(self.tab_control.select()) + 1}...\n")
            # --- Your user creation logic ---
            self.output_text.insert(tk.END, "Simulated SMTP user creation.\n") # Placeholder
        except KeyError as e:
             self.output_text.insert(tk.END, f"Error: Missing data key {e} for current tab.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error creating SMTP user: {e}\n")


    def configure_smtp(self):
        current_data = self._get_current_tab_data()
        if not current_data: return

        try:
            domain = current_data["Domínio_var"].get()
            ip = current_data["IP_var"].get() # Might need IP/User/Pass for connection
            # ... get other needed vars ...

            self.output_text.insert(tk.END, f"Configuring SMTP for domain '{domain}' on {ip} for Tab {self.tab_control.index(self.tab_control.select()) + 1}...\n")
            # --- Your SMTP config logic ---
            self.output_text.insert(tk.END, "Simulated SMTP configuration.\n") # Placeholder
        except KeyError as e:
             self.output_text.insert(tk.END, f"Error: Missing data key {e} for current tab.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error configuring SMTP: {e}\n")


    def get_domain_records(self):
        current_data = self._get_current_tab_data()
        if not current_data: return

        try:
            dominio = current_data["Domínio_var"].get()
            self.output_text.delete(1.0, tk.END) 
            self.output_text.insert(tk.END, f"\n Registros para o dominio {dominio}: \n {getRecords(dominio)} DNS Utilizado:Google\n")
        except KeyError as e:
             self.output_text.insert(tk.END, f"Error: Missing data key {e} for current tab.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error getting domain records: {e}\n")


# --- Main part ---
if __name__ == "__main__":
    app = SMTPConfigApp()
    # Example: Set initial value for VPS 3's IP
    app.mainloop()
