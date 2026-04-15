import customtkinter as ctk

class AppMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión Pro")
        self.geometry("800x500")

        # Configurar el diseño de la cuadrícula (1 columna para menú, 1 para contenido)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- FRAME LATERAL (MENÚ) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Espaciador

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="OYASUMI", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botones del menú
        self.btn_inicio = ctk.CTkButton(self.sidebar_frame, text="Inicio", command=lambda: self.cambiar_seccion("Inicio"))
        self.btn_inicio.grid(row=1, column=0, padx=20, pady=10)

        self.btn_perfil = ctk.CTkButton(self.sidebar_frame, text="Perfil", command=lambda: self.cambiar_seccion("Perfil"))
        self.btn_perfil.grid(row=2, column=0, padx=20, pady=10)

        self.btn_ajustes = ctk.CTkButton(self.sidebar_frame, text="Ajustes", command=lambda: self.cambiar_seccion("Ajustes"))
        self.btn_ajustes.grid(row=3, column=0, padx=20, pady=10)

        # Selector de tema al final del menú
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # --- CONTENIDOR PRINCIPAL (CENTRO) ---
        self.main_content = ctk.CTkFrame(self, corner_radius=15)
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.label_titulo = ctk.CTkLabel(self.main_content, text="Bienvenido", font=("Arial", 22))
        self.label_titulo.pack(pady=50)

    # Funciones de lógica
    def cambiar_seccion(self, nombre_seccion):
        self.label_titulo.configure(text=f"Sección: {nombre_seccion}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = AppMenu()
    app.mainloop()