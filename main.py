import tkinter as tk
from tkinter import ttk
import extendedlistbox as elb
import listboxitem as lbi


def insert_widget(index):
    global num_inserts
    w = lbi.ListboxItem(lb.widget_frame, f'Insert {num_inserts}')
    w.grid(padx=(5, 5), pady=(0, 0), sticky=tk.EW)
    lb.insert(index, w)
    num_inserts += 1


def insert_widgets(index, num):
    global num_inserts
    widgets = []
    for i in range(num):
        w = lbi.ListboxItem(lb.widget_frame, f'Insert {num_inserts}')
        w.grid(padx=(5, 5), pady=(0, 0), sticky=tk.EW)
        widgets.append(w)
        num_inserts += 1

    lb.insert(index, *widgets)


if __name__ == '__main__':
    # Toplevel widget
    root = tk.Tk()
    root.geometry('200x300')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)

    # Styles
    style = ttk.Style()

    style.configure('Listbox.TFrame',
                    background='white')

    style.configure('TestArea.TFrame',
                    background='dark gray')

    # Listbox
    lb = elb.ExtendedListbox(root, style='Listbox.TFrame')
    lb.grid(column=0, row=0, sticky=tk.NSEW)

    # Frame holding manual testing buttons
    test_frame = ttk.Frame(root, style='TestArea.TFrame')
    test_frame.columnconfigure(0, weight=1)
    test_frame.columnconfigure(1, weight=1)
    test_frame.rowconfigure(0, weight=0)
    test_frame.rowconfigure(1, weight=0)
    test_frame.rowconfigure(2, weight=0)
    test_frame.rowconfigure(3, weight=0)
    test_frame.rowconfigure(4, weight=0)
    test_frame.rowconfigure(5, weight=0)
    test_frame.grid(column=0, row=1, sticky=tk.EW)

    num_inserts = 0
    istart_btn = ttk.Button(test_frame,
                            text='Insert Start',
                            command=lambda: insert_widget(0))
    istart_btn.grid(column=0, row=0, pady=(10, 0))

    iend_btn = ttk.Button(test_frame,
                          text='Insert End',
                          command=lambda: insert_widget(tk.END))
    iend_btn.grid(column=0, row=1, pady=(10, 0))

    dstart_btn = ttk.Button(test_frame,
                            text='Delete Start',
                            command=lambda: lb.delete(0))
    dstart_btn.grid(column=1, row=0, pady=(10, 0))

    dend_btn = ttk.Button(test_frame,
                          text='Delete End',
                          command=lambda: lb.delete(tk.END))
    dend_btn.grid(column=1, row=1, pady=(10, 0))

    imany_btn = ttk.Button(test_frame,
                           text='Insert Many',
                           command=lambda: insert_widgets(1, 3))
    imany_btn.grid(column=0, row=2, pady=(10, 0))

    dmany_btn = ttk.Button(test_frame,
                           text='Delete Many',
                           command=lambda: lb.delete(1, 3))
    dmany_btn.grid(column=1, row=2, pady=(10, 0))

    gstart_btn = ttk.Button(test_frame,
                            text='Get Start',
                            command=lambda: print(lb.get(0)))
    gstart_btn.grid(column=0, row=3, pady=(10, 0))

    gend_btn = ttk.Button(test_frame,
                          text='Get End',
                          command=lambda: print(lb.get(tk.END)))
    gend_btn.grid(column=1, row=3, pady=(10, 0))

    gactive_btn = ttk.Button(test_frame,
                             text='Get Active',
                             command=lambda: print(lb.get(tk.ACTIVE)))
    gactive_btn.grid(column=0, row=4, pady=(10, 0))

    gall_btn = ttk.Button(test_frame,
                          text='Get All',
                          command=lambda: print(lb.get(0, tk.END)))
    gall_btn.grid(column=1, row=4, pady=(10, 0))

    astart_btn = ttk.Button(test_frame,
                            text='Activate Start',
                            command=lambda: lb.activate(0))
    astart_btn.grid(column=0, row=5, pady=(10, 0))

    aend_btn = ttk.Button(test_frame,
                          text='Activate End',
                          command=lambda: lb.activate(tk.END))
    aend_btn.grid(column=1, row=5, pady=(10, 0))

    root.mainloop()
