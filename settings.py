import customtkinter as CTk
from keysettings import KeySettings
from configparser import ConfigParser

class BoolButtons(CTk.CTkButton):

    def on_click(self) -> None:
        self.configure(text= 'True' if not self.value else 'False')
        self.value = not self.value

        file: ConfigParser = ConfigParser()
        file.read('saves.ini')

        file['config'][self.setting] = str(self.value).lower()

        with open('saves.ini', 'w') as content:
            file.write(content)

    def __init__(self, master, value: bool,setting: str):
        super().__init__(
            master=master,
            text=str(value),
            command=self.on_click,
            width=2
        )

        self.value: bool = value
        self.setting: str = setting

        

class Settings(CTk.CTk):

    def __init__(self):
        super().__init__()

        # App Configuration
        self.geometry("300x170")
        self.title("Cooldown Overlay: Settings")
        self.attributes("-topmost", True)
        self.wm_attributes("-toolwindow", "true")
        self.resizable(False,False)

        # Main Frame
        main_frame: CTk.CTkFrame = CTk.CTkFrame(
            self,
            fg_color='grey'
        )
        main_frame.pack(pady=7,padx=7,expand=True,fill='both')

        #Keybind Button
        keybind_button: CTk.CTkButton = CTk.CTkButton(
            main_frame,
            width=15,
            height=15,
            command=KeySettings,
            text='Keybinds'
        )
        keybind_button.place(x=215,y=130)

        #Settings
        file: ConfigParser = ConfigParser()
        file.read('saves.ini')

        settings: dict[str: bool] = {key: (True if value == 'true' else False) for key, value in file['config'].items()}
        print(settings)
        
        for setting, value in settings.items():
            frame: CTk.CTkFrame = CTk.CTkFrame(main_frame, fg_color='transparent')

            setting_label: CTk.CTkLabel = CTk.CTkLabel(
                frame,
                height=7,
                width=5,
                text=setting
            )
            setting_label.pack(side='left',expand=True)

            value_button: BoolButtons = BoolButtons(
                frame,
                value,
                setting
            )
            value_button.pack(side='right',expand=True)

            frame.pack(side='top',pady=1,fill='x',padx=5)

        self.mainloop()


if __name__ == '__main__':
    Settings()