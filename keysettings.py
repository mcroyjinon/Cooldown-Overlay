import tkinter as Tk
import customtkinter as CTk
from configparser import ConfigParser
from buttons import ChangeableButtons


class Display(CTk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, height=30)
        self.pack(fill="x", pady=5)

    def display_buttons(self, index):
        # Access [saves.ini]
        file: ConfigParser = ConfigParser()
        file.read("saves.ini")

        keybinds: list[str] = list(file["keybinds"].keys())

        keybind_button: ChangeableButtons = ChangeableButtons(self, keybinds[index], "keybind")
        keybind_button.pack(expand=True, side="left", fill="x", padx=2.5)

        name_button: ChangeableButtons = ChangeableButtons(self, keybinds[index], "name")
        name_button.pack(expand=True, side="left", fill="x", padx=2.5)

        cooldown_button: ChangeableButtons = ChangeableButtons(self, keybinds[index], "cooldown")
        cooldown_button.pack(expand=True, side="left", fill="x", padx=2.5)


class KeySettings(CTk.CTk):

    def __init__(self):
        super().__init__()

        # App Configuration
        self.geometry("300x170")
        self.title("Cooldown Overlay: Settings: Keybinds")
        self.attributes("-topmost", True)
        self.wm_attributes("-toolwindow", "true")

        # Tools Frame

        tools_frame: CTk.CTkFrame = CTk.CTkFrame(
            self,
            fg_color='transparent'
        )
        tools_frame.pack(side='top',fill='x',pady=3,padx=5)

        add_button: CTk.CTkButton = CTk.CTkButton(
            tools_frame,
            width=10,
            height=10,
            command=self.add_new,
            text='+'
        )
        add_button.pack(side='right')

        # Main Frame
        self.main_frame: CTk.CTkScrollableFrame = CTk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, side='top')

        # Access [saves.ini]
        self.file: ConfigParser = ConfigParser()
        self.file.read("saves.ini")

        self.display_keybinds()

        self.mainloop()

    def display_keybinds(self):
        keybinds: list[str] = list(self.file["keybinds"].keys())

        for i in range(0, len(keybinds)):
            self.display_frame = Display(self.main_frame)
            self.display_frame.display_buttons(i)

    def add_new(self):
        for window in self.main_frame.winfo_children():
            window.destroy()

        self.file['keybinds']['New'] = 'New'
        self.file['cooldowns']['New'] = 'New'

        with open('saves.ini', 'w') as content:
            self.file.write(content)
        
        self.display_keybinds()


if __name__ == "__main__":
    App = KeySettings()
