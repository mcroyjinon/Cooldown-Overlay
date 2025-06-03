import tkinter as Tk
import customtkinter as CTk
from pynput import keyboard,mouse
from configparser import ConfigParser
from labels import Hotkey_Display

class Main_App(CTk.CTk):
        
    def __init__(self):
        super().__init__()

        w=300
        h=150

        self.geometry(f'{w}x{h}')
        self.resizable(False,False)
        self.title('Cooldown Overlay')
        
        self.attributes('-topmost', True)
        self.wm_attributes('-toolwindow','true')

        main_frame = CTk.CTkFrame(self,fg_color='transparent')
        main_frame.pack(fill='both',expand='true',pady=5,padx=5)

        def display_frame():
            frame = CTk.CTkFrame(main_frame,fg_color='#b1b1b1',width=130)
            counter=CTk.IntVar(frame,0)
            frame.pack(side='left',fill='both',expand='true',padx=5)
            frame.pack_propagate(False)

            return frame,counter

        left_frame, left_counter = display_frame()

        right_frame, right_counter = display_frame()

        saves = ConfigParser()
        saves.read('saves.ini')

        hotkeys={}

        self.current_key=None

        current_cooldown=[]

        for key in saves['keybinds'].keys():
            hotkeys[keyboard.KeyCode.from_char(key)]=key

        def change_key(key):
            if not key in hotkeys: return
            
            codecc=keyboard.KeyCode.from_char(self.current_key)
            if key !=  codecc: 
                self.current_key=hotkeys[key]
            elif key == codecc:
                self.current_key=None
            print(self.current_key)
            
        keyboard_listener = keyboard.Listener(on_press=lambda key: change_key(key))
        keyboard_listener.start()

        def timed():
            current_cooldown.pop(0)

        def display(x,y,button,pressed):
            if self.current_key==None: return
            if not pressed: return
            if self.current_key in current_cooldown: return
            
            parent=left_frame
            if left_counter.get() > 5:
                parent=right_frame

            Hotkey_Display(parent,saves['keybinds'][self.current_key],saves['cooldowns'][saves['keybinds'][self.current_key]])

            self.after(int(saves['cooldowns'][saves['keybinds'][self.current_key]])*1000,lambda: timed())

            left_counter.set(left_counter.get()+1)

            current_cooldown.append(self.current_key)

        mouse_listener = mouse.Listener(on_click=lambda x,y,button,pressed: display(x,y,button,pressed))
        mouse_listener.start()

if __name__=='__main__':
    App = Main_App()
    App.mainloop()