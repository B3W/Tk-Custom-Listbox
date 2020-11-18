'''Module providing resizable text widget'''
import tkinter as tk


class ResizableText(tk.Text):
    def __init__(self, master, *args, **kwargs):
        tk.Text.__init__(self, master, *args, **kwargs)
        self.line_count = 0
        self._resizing = False

        self.bind('<<Modified>>', self.resize)

    def resize(self, event=None):
        # Count number of lines needed to display text
        resized_line_count = self.count(1.0, tk.END, 'displaylines')[0]

        # Only configure height if it has changed
        if resized_line_count != self.line_count:
            self.configure(height=resized_line_count)
            self.line_count = resized_line_count

        self._resizing = False

    def on_configure(self, event):
        # NOTE 'event.width' is the pixel width of the text
        # Only resize every ~200ms
        if not self._resizing:
            self._resizing = True
            self.after(200, self.resize)
