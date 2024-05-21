# src/menu.py
import customtkinter as ctk

class MenuPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=200, corner_radius=0)
        self.pack_propagate(False)

        # Add buttons
        ctk.CTkButton(self, text="SetUp", command=lambda: print("Home clicked")).pack(pady=10)
        ctk.CTkButton(self, text="Result", command=lambda: print("Settings clicked")).pack(pady=5)

        # Add an option menu
        self.option_menu = ctk.CTkOptionMenu(self, values=["option 1", "option 2"],
                                             command=self.optionmenu_callback)
        self.option_menu.set("option 2")
        self.option_menu.pack(pady=20)

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
