import tkinter as Tk
import customtkinter as CTk
from configparser import ConfigParser
import win32gui
import win32con


class Input(CTk.CTk):

    def __init__(self, key: str, type: str, text_var: CTk.StringVar):
        super().__init__()

        self.geometry("300x100")
        self.resizable(False, False)
        self.title("Cooldown Overlay: Settings: Entry")
        self.attributes("-topmost", True)
        self.wm_attributes("-toolwindow", "true")

        self.key: str = key
        self.type: str = type
        self.text_var: CTk.StringVar = text_var

        self.entry: CTk.CTkEntry = CTk.CTkEntry(master=self, width=30)
        self.entry.pack(side="top", pady=15, fill="x", padx=5)

        enter: CTk.CTkButton = CTk.CTkButton(master=self, width=30, text="Enter", command=self.submit)
        enter.pack(side="top")

        self.mainloop()

    def submit(self):
        text: str = self.entry.get()

        match self.type:
            case "keybind":
                if len(text) > 1:
                    return
            case "cooldown":
                try:
                    int(text)
                except ValueError:
                    return

        previous_value: str = self.text_var.get()
        self.text_var.set(text)

        save_file: ConfigParser = ConfigParser()
        save_file.read("saves.ini")

        match self.type:
            case "keybind":
                saved_value: str = save_file["keybinds"][previous_value]
                save_file.remove_option("keybinds", previous_value)
                save_file["keybinds"][text] = saved_value
            case "name":
                save_file["keybinds"][self.key] = text

                saved_value: str = save_file["cooldowns"][previous_value]
                save_file.remove_option("cooldowns", previous_value)
                save_file["cooldowns"][text] = saved_value
            case "cooldown":
                save_file["cooldowns"][save_file["keybinds"][self.key]] = text

        with open("saves.ini", "w") as file:
            save_file.write(file)

        hwnd: int|None = win32gui.FindWindow(None, "Cooldown Overlay: Settings: Keybinds")
        if hwnd:
            self.after(100, win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0))

        self.after(100, lambda: self.destroy())


class ChangeableButtons(CTk.CTkButton):

    def __init__(self, parent, key, type:str):

        saves_file: ConfigParser = ConfigParser()
        saves_file.read("saves.ini")

        text_var: CTk.StringVar = CTk.StringVar(master=parent)

        match type:
            case "keybind":
                text_var.set(key)
            case "name":
                text_var.set(saves_file["keybinds"][key])
            case "cooldown":
                text_var.set(saves_file["cooldowns"][saves_file["keybinds"][key]])

        super().__init__(
            parent,
            height=30,
            command=lambda: Input(key, type, text_var),
            textvariable=text_var,
            width=56,
        )


if __name__ == "__main__":
    App = CTk.CTk()

    button = ChangeableButtons(App, "1", "cooldown")

    button.pack()

    App.mainloop()
