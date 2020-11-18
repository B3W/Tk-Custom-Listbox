import autoscrollbar as asb
import math
import tkinter as tk
from tkinter import ttk


class SimpleScrollableFrame(ttk.Frame):
    '''
    UI element displaying widgets that can be scrolled through. UI element also
    dynamically determines which widgets in the scrollable region are visible.
    '''
    def __init__(self, master, *args, **kwargs):
        '''
        Override of ttk.Frame's initialization function

        :param master: Widget's master
        :param tpad: Padding applied around top of widgets in scroll frame
        :param lpad: Padding applied around left of widgets in scroll frame
        :param sfunc: Pointer to function to call on widgets set to visible
        :param hfunc: Pointer to function to call on widgets set to hidden
        '''
        # Initialize root frame
        ttk.Frame.__init__(self, master, *args, **kwargs)

        self.columnconfigure(0, weight=1)  # Canvas/Scrollable Frame
        self.columnconfigure(1, weight=0)  # AutoScrollbar
        self.rowconfigure(0, weight=1)

        self.widgets = []
        self.configuring = False

        # Initialize Canvas to hold 'scrollable' frame
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.grid(column=0, row=0, sticky=tk.NSEW)

        # Initialize vertical AutoScrollbar and link to the Canvas
        self.vsb = asb.AutoScrollbar(self,
                                     column=1, row=0,
                                     orient=tk.VERTICAL,
                                     command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Initialize 'scrollable' frame for actual message content
        self.widget_frame = ttk.Frame(self.canvas, style=self['style'])
        self.widget_frame.columnconfigure(0, weight=1)

        canvas_win_location = (0, 0)
        self.cframe_id = self.canvas.create_window(canvas_win_location,
                                                   window=self.widget_frame,
                                                   anchor='nw')

        # Bind callbacks for when the Message Frame/Canvas is resized
        self.widget_frame.bind('<Configure>', self.__update_scrollregion)
        self.canvas.bind('<Configure>', self.__on_canvas_configure)

        # Bind callbacks for the mouse wheel
        self.widget_frame.bind('<Enter>', self.__bind_mousewheel)
        self.widget_frame.bind('<Leave>', self.__unbind_mousewheel)

    def scroll_bottom(self):
        self.canvas.update_idletasks()  # Let canvas finish layout calculations
        self.canvas.yview_moveto(1.0)   # Scroll to bottom of canvas

    # CALLBACKS
    def __on_canvas_configure(self, event):
        '''Callback for canvas's <Configure> event'''
        if not self.configuring:
            # Configure and then delay until next config to lower CPU load
            self.configuring = True

            width = event.width
            self.__configure_canvas(width, False)
            self.after(75, self.__configure_canvas, width, True)

    def __configure_canvas(self, width, reset):
        self.canvas.itemconfigure(self.cframe_id, width=width)
        self.configuring = not reset

    def __update_scrollregion(self, event=None):
        '''Callback for inner frame's <Configure> event'''
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def __bind_mousewheel(self, event):
        '''Callback for inner frame's <Enter> event'''
        # Bind the root scrollable widget to the scrolling callback
        self.canvas.bind_all('<MouseWheel>', self.__on_mousewheel)

    def __unbind_mousewheel(self, event):
        '''Callback for inner frame's <Leave> event'''
        # Unbind the root scrollable widget from the scrolling callback
        self.canvas.unbind_all('<MouseWheel>')

    def __on_mousewheel(self, event):
        '''Callback for all widget's <Mousewheel> event'''
        if self.vsb.hidden:
            # Do not allow scrolling if scrollbars are hidden
            return

        # Get sign of delta then reverse to get scroll direction
        scroll_dir = -1 * int(math.copysign(1, event.delta))
        self.canvas.yview_scroll(scroll_dir, 'units')
