import tkinter as Tk
import customtkinter as CTk
from pynput import keyboard, mouse
from configparser import ConfigParser
from labels import Hotkey_Display
from settings import Settings
import win32gui
import win32con


class Main_App(CTk.CTk):

    def __init__(self):
        super().__init__()

        # Create the Window
        w = 300
        h = 170

        self.geometry(f"{w}x{h}")  # Sets Size to 300 by 170
        self.resizable(False, False)  # Cannot be Resized
        self.title("Cooldown Overlay")

        self.attributes("-topmost", True)  # Always Ontop
        self.wm_attributes("-toolwindow", "true")  # Toolwindow Mode

        # Create Frame to hold + button
        settings_frame = CTk.CTkFrame(self, fg_color="transparent")
        settings_frame.pack(side="top", pady=5, fill="x", padx=10)

        settings_button = CTk.CTkButton(
            settings_frame,
            height=15,
            width=15,
            text="Settings",
            command=self.enter_settings,
        )
        settings_button.pack(side="right")

        update_button = CTk.CTkButton(
            settings_frame,
            height=15,
            width=15,
            text="Update Keybinds",
            command=self.update_keybinds,
        )
        update_button.pack(side="right")

        # Create Main Frame holding other Frames
        main_frame = CTk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand="true", pady=0, padx=5, side="top")

        self.left_frame, self.left_counter = self.display_frame(main_frame)
        self.right_frame, right_counter = self.display_frame(main_frame)

        self.update_keybinds()
        self.current_key = None

        keyboard_listener = keyboard.Listener(on_press=self.change_key)
        keyboard_listener.start()

        self.mouse_listener = mouse.Listener(on_click=self.display_on_click)

    # Create Display Frames
    def display_frame(self, parent):
        frame = CTk.CTkFrame(parent, fg_color="#b1b1b1", width=130)
        counter = CTk.IntVar(frame, 0)
        frame.pack(side="left", fill="both", expand="true", padx=5)
        frame.pack_propagate(False)

        return frame, counter

    # Enter Settings Window
    def enter_settings(self):
        hwnd = win32gui.FindWindow(
            None, "Cooldown Overlay: Settings"
        )  # Try to find Settings Window
        if hwnd:  # If Found then Open Tab and Focus
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return
        Settings()  # Else Create Settings Window

    # Changes the self.current_key to the keybind pressed
    def change_key(self, key):
        if not key in self.hotkeys:
            return

        codecc = keyboard.KeyCode.from_char(self.current_key)
        # Takes Key and Cast as keyboard.KeyCode

        # If the Key Pressed doesn't equal Current KeyCode, then set Key as Current Key
        if key != codecc:
            self.current_key = self.hotkeys[key]
        elif key == codecc:  # If it does equal, set Current Key as None (Deselected)
            self.current_key = None
        print(self.current_key)

        save_config = self.saves["config"]

        if save_config["click activation"] == "true":
            self.mouse_listener.start()
        else:
            self.display()
            if save_config["deselect after activation"] == "true":
                self.current_key = None
                print(self.current_key)

    # Cooldown is Over
    def timed(self, key, parent):
        self.cooldowns[key] = False
        if (
            parent == "left"
        ):  # If the Display was on the left side, Decrease [left_counter] by 1
            self.left_counter.set(self.left_counter.get() - 1)

    # Displays Cooldown
    def display(self):
        if self.current_key == None:
            return  # If No Key is Selected, then return
        if self.cooldowns[self.current_key] == True:
            return  # If Name is already On Cooldown, then return

        parent = self.left_frame  # Default Parent is Left
        parent_name = "left"

        # If Left has more than 5 displays, Set Parent to Right
        if self.left_counter.get() > 5:
            parent = self.right_frame
            parent_name = "right"
        else:
            self.left_counter.set(self.left_counter.get() + 1)
            # Else Increment Left Counter by 1

        keybind_name = self.saves["keybinds"][self.current_key]
        # Gets the Name of Keybind

        keybind_time = self.saves["cooldowns"][keybind_name]
        # Gets Cooldown  of Keybind

        Hotkey_Display(parent, keybind_name, keybind_time)
        # Displays Name and Cooldown Time

        stored_key = self.current_key  # [self.current_key] changes, so store Key in Var
        self.after(
            int(keybind_time) * 1000, lambda: self.timed(stored_key, parent_name)
        )
        # After Cooldown, do [timed] method

        self.cooldowns[self.current_key] = True  # Set On Cooldown of Keybind to True

    # Displays the Cooldown on Click
    def display_on_click(self, x, y, button, pressed):
        if not pressed:
            return  # If Click is Let Go, then return
        self.display()

    # Updates Keybind Info after making Changes
    def update_keybinds(self):
        #  Find Saves File
        self.saves = ConfigParser()
        self.saves.read("saves.ini")

        # Set Important Vars
        self.hotkeys = {}
        self.cooldowns = {}

        # Fill Tables
        for key in self.saves["keybinds"].keys():
            key_name = keyboard.KeyCode.from_char(key)
            self.hotkeys[key_name] = key
            self.cooldowns[key] = False
        print(self.cooldowns)


if __name__ == "__main__":
    App = Main_App()
    App.mainloop()
