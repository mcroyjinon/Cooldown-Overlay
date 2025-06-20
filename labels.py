import tkinter as Tk
import customtkinter as CTk
import time


class Hotkey_Label(CTk.CTkLabel):

    def __init__(self, parent, txt: str):
        super().__init__(master=parent, text=txt)

        self.pack(side="left", padx=5)


class Hotkey_Cooldown(CTk.CTkLabel):

    def __init__(self, parent, time: int):

        timer: CTk.StringVar = CTk.StringVar()
        timer.set(time)

        super().__init__(master=parent, textvariable=timer)

        self.pack(side="right", padx=5)

        counter = int(timer.get())

        def func(i: int):
            new_count = str(counter - i)
            self.after(i * 1000, lambda: timer.set(new_count))

        for i in range(0, int(timer.get()), 1):
            func(i)
        self.after(int(time) * 1000, lambda: self.after(150, parent.destroy()))


class Hotkey_Display(CTk.CTkFrame):

    def __init__(self, parent, name: str, time: int):
        super().__init__(master=parent, width=70, height=20)
        self.pack_propagate(False)
        self.pack(side="top", padx=10, pady=2, fill="x")

        label: Hotkey_Label = Hotkey_Label(self, name)
        cd: Hotkey_Cooldown = Hotkey_Cooldown(self, time)