import tkinter as tk


class ListboxItem(tk.Button):
    def __init__(self, master, text, *args, **kwargs):
        '''
        Override of tk.Text's initialization function

        :param master: Widget's master
        '''
        # Initialize root text
        tk.Button.__init__(self, master,
                           text=text,
                           relief=tk.FLAT,
                           background='white',
                           padx=5,
                           pady=5,
                           *args, **kwargs)

        self.selected = False

        self.bind('<Button-1>', self.__click_callback)
        self.bind('<Enter>', self.__hover_enter)
        self.bind('<Leave>', self.__hover_exit)

    def select(self, event=None):
        self.selected = True
        self.configure(background='light sky blue')

    def deselect(self):
        self.selected = False
        self.configure(background='white')

    # CALLBACKS
    def __click_callback(self, event):
        self.event_generate('<<ItemSelect>>')
        return 'break'

    def __hover_enter(self, event):
        if not self.selected:
            self.configure(background='light sky blue')

    def __hover_exit(self, event):
        if not self.selected:
            self.configure(background='white')
