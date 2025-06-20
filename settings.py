import customtkinter as CTk
from keysettings import KeySettings


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


        self.mainloop()


if __name__ == '__main__':
    Settings()