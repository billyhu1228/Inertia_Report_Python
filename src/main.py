# src/main.py
import customtkinter as ctk
from menu import MenuPanel
from content import ContentPanel


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inertia Application ")
        self.geometry("800x800")

        self.menu_panel = MenuPanel(self)
        self.menu_panel.pack(side='left', fill='y')

        self.content_panel = ContentPanel(self)
        self.content_panel.pack(side='right', expand=True, fill='both')

    # if __name__ == "__main__":
    #     app =App()
    #     app.mainloop()
app =MainApplication()
app.mainloop()
