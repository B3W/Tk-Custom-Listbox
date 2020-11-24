import tkinter as tk
import scrollableframe as sf


class CustomListbox(sf.SimpleScrollableFrame):
    '''UI element providing listbox-like functionality'''
    def __init__(self, master, *args, **kwargs):
        '''
        Override of ScrollableFrame's initialization function

        :param master: Widget's master
        '''
        sf.SimpleScrollableFrame.__init__(self, master, *args, **kwargs)

        self.selected_index = -1

    def insert(self, index, *widgets):
        '''
        Insert one or more new items into the listbox before the line specified
        by index. Use END as first argument to add to the end of the listbox.
        '''
        if index == tk.END:
            insert_index = len(self.widgets)
        elif index == tk.ACTIVE:
            insert_index = self.selected_index
        else:
            # Clamp top range of index
            if index > len(self.widgets):
                insert_index = len(self.widgets)
            else:
                insert_index = index

        if insert_index < 0:
            return

        # Get list of widgets that will need to be shifted down
        shifted_widgets = self.widgets[insert_index:]
        num_shifts = 0

        # Check if selection index will change
        if self.selected_index >= insert_index:
            shift_selection = True
        else:
            shift_selection = False

        # Insert new widgets into listbox
        for widget in widgets:
            self.widgets.insert(insert_index, widget)
            widget.grid(column=0, row=insert_index)
            widget.bind('<<ItemSelect>>', self.__selection_callback)
            num_shifts += 1
            insert_index += 1

        # Shift selection
        if shift_selection:
            self.selected_index += num_shifts

        # Shift widgets
        for widget in shifted_widgets:
            current_row = widget.grid_info()['row']
            shifted_row = current_row + num_shifts
            widget.grid_configure(row=shifted_row)

        self.update_idletasks()  # Allow UI to update

    def delete(self, first, last=None):
        '''
        Deletes the items whose indices are in the range [first, last]. If the
        second argument is omitted, a single line with index first is deleted.
        '''
        # Determine index to start deletion
        if first == tk.END:
            get_start = len(self.widgets) - 1
        else:
            if first < 0:
                get_start = 0
            else:
                get_start = first

        if get_start >= len(self.widgets):
            return

        # Determine index to stop deletion
        if last is not None:
            if last == tk.END:
                get_end = len(self.widgets) - 1
            else:
                get_end = last
        else:
            get_end = get_start

        if get_end < get_start:
            return

        # Get list of widgets to be shifted up
        get_end += 1  # List slices have exclusive end
        shifted_widgets = self.widgets[get_end:]
        num_shifts = 0

        # Delete widgets
        for i in range(get_start, get_end):
            try:
                if self.widgets[i].selected:
                    self.selected_index = -1

                self.widgets[i].destroy()

            except IndexError:
                break

            num_shifts += 1

        del(self.widgets[get_start:get_end])

        # Shift selection
        if self.selected_index >= get_end:
            self.selected_index -= num_shifts

        # Shift widgets
        for widget in shifted_widgets:
            current_row = widget.grid_info()['row']
            shifted_row = current_row - num_shifts
            widget.grid_configure(row=shifted_row)

        self.update_idletasks()  # Allow UI to update

    def get(self, first, last=None):
        '''
        Returns tuple of items with indices from first to last, inclusive. If
        second argument is omitted, returns item closest to first
        '''
        # Determine index to start get range
        if first == tk.END:
            get_start = len(self.widgets) - 1
        elif first == tk.ACTIVE:
            get_start = self.selected_index
        else:
            if first < 0:
                get_start = 0
            else:
                get_start = first

        if get_start >= len(self.widgets):
            if last is not None:
                return ()
            else:
                return None

        # Determine index to stop get range
        if last is not None:
            if last == tk.END:
                get_end = len(self.widgets) - 1
            elif last == tk.ACTIVE:
                get_end = self.selected_index
            else:
                get_end = last
        else:
            get_end = get_start

        if get_end < get_start:
            return ()

        if last is not None:
            # Get tuple of items
            return tuple(self.widgets[get_start:get_end + 1])
        else:
            # Get single item
            if get_start < 0:
                widget = None
            else:
                widget = self.widgets[get_start]

            return widget

    def activate(self, index):
        '''Sets active element in listbox to element at index'''
        if len(self.widgets) == 0:
            return

        # Determine index to activate
        if index == tk.END:
            activate_index = len(self.widgets) - 1
        elif index == tk.ACTIVE:
            activate_index = self.selected_index
        else:
            # Clamp top range of index
            if index >= len(self.widgets):
                activate_index = len(self.widgets) - 1
            else:
                activate_index = index

        # Clamp bottom range of index
        activate_index = max(0, activate_index)

        # Select new index
        self.widgets[activate_index].event_generate('<<ItemSelect>>')

    def curselection(self):
        '''
        Returns tuple containing indices of all elements currently selected.
        '''
        if self.selected_index < 0:
            return ()

        return (self.widgets[self.selected_index],)

    def index(self, index):
        '''
        Returns the numerical index (0 to size()-1) corresponding to the given
        index. Index 'END' returns count of elements in listbox.
        '''
        if index == tk.END:
            returned_index = len(self.widgets)
        elif index == tk.ACTIVE:
            returned_index = self.selected_index
        else:
            try:
                returned_index = int(index)
            except ValueError:
                err_msg = f'Bad listbox index "{index}": ' \
                        + 'must be active, end, or a number'
                raise ValueError(err_msg)

        return returned_index

    def size(self):
        '''Returns the number of entries in the listbox'''
        return len(self.widgets)

    def __selection_callback(self, event):
        event_index = self.widgets.index(event.widget)

        if self.selected_index != event_index:
            # Deselect previous selection
            if self.selected_index >= 0:
                self.widgets[self.selected_index].deselect()

            # Select new
            event.widget.select()
            self.selected_index = event_index

        # Raise <<ListboxSelect>> event
        self.event_generate('<<ListboxSelect>>')
