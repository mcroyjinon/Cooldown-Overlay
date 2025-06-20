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
        self.title("Cooldown Overlay: Settings")
        self.attributes("-topmost", True)
        self.wm_attributes("-toolwindow", "true")

        main_frame: CTk.CTkScrollableFrame = CTk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        # Access [saves.ini]
        file: ConfigParser = ConfigParser()
        file.read("saves.ini")

        keybinds: list[str] = list(file["keybinds"].keys())

        for i in range(0, len(keybinds)):
            frame = Display(main_frame)
            frame.display_buttons(i)

        self.mainloop()


if __name__ == "__main__":
    App = KeySettings()
