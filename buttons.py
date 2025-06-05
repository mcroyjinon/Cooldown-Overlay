import tkinter as Tk
import customtkinter as CTk
from configparser import ConfigParser

class Input(CTk.CTk):

    def __init__(self,key,type,text_var):
        super().__init__()

        self.geometry('300x100')
        self.resizable(False,False)
        self.title('Cooldown Overlay: Settings: Entry')  
        self.attributes('-topmost', True)
        self.wm_attributes('-toolwindow','true')

        self.key=key
        self.type=type
        self.text_var=text_var

        self.entry = CTk.CTkEntry(master=self,width=30)
        self.entry.pack(side='top',pady=15,fill='x',padx=5)

        enter = CTk.CTkButton(master=self,width=30,text='Enter',command=self.submit)
        enter.pack(side='top')

        self.mainloop()

    def submit(self):
        text = self.entry.get()

        previous_value=self.text_var.get()
        self.text_var.set(text)

        save_file = ConfigParser()
        save_file.read('saves.ini')

        match self.type:
            case 'keybind':
                saved_value=save_file['keybinds'][previous_value]
                save_file.remove_option('keybinds',previous_value)
                save_file['keybinds'][text]=saved_value
            case 'name':
                save_file['keybinds'][self.key]=text

                saved_value=save_file['cooldowns'][previous_value]
                save_file.remove_option('cooldowns',previous_value)
                save_file['cooldowns'][text]=saved_value
            case 'cooldown':
                save_file['cooldowns'][save_file['keybinds'][self.key]]=text

        with open('saves.ini','w') as file:
            save_file.write(file)

        self.after(150,lambda: self.destroy())

class Changeable_Buttons(CTk.CTkButton):

    def __init__(self,parent,key,type):

        saves_file = ConfigParser()
        saves_file.read('saves.ini')

        text_var = CTk.StringVar(master=parent)

        match type:
            case 'keybind':
                text_var.set(key)
            case 'name':
                text_var.set(saves_file['keybinds'][key])
            case 'cooldown':
                text_var.set(saves_file['cooldowns'][saves_file['keybinds'][key]])

        super().__init__(parent,height=30,command=lambda: Input(key,type,text_var),textvariable=text_var,width=56)

if  __name__ == '__main__':
    App = CTk.CTk()

    button = Changeable_Buttons(App,'1','cooldown')

    button.pack()

    App.mainloop()