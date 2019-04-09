#! /usr/bin/env python
# -*- coding:utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


DEFAULT_WIDTH = 330
DEFAULT_HEIGHT = 120
ZLIST_HEIGHT = 400


class Base(object):
    def __init__(self, title, width, height, timeout):
        self.title = title
        self.width = width
        self.height = height
        self.timeout = timeout
        self.dialog = None
        self.response = None

    def init_dialog(self):
        # global config
        self.dialog.set_resizable(True)
        self.dialog.resize(self.width, self.height)
        self.dialog.set_border_width(5)
        if self.timeout:
            GLib.timeout_add_seconds(
                self.timeout,
                self._destroy,
                self.dialog
            )

        if self.title:
            self.dialog.set_title(self.title)
        self.dialog.connect("destroy", self._destroy)

    def run(self):
        self.dialog.show()
        self.dialog.connect("response", self._response)
        Gtk.main()

    def _response(self, dialog, response):
        self.set_response(response)
        self._destroy(self.dialog)

    def _destroy(self, dialog):
        self.dialog.destroy()
        Gtk.main_quit()

    def set_response(self, response):
        self.response = response


class ZSimpleDialog(Base):
    def __init__(self, dialog_type, text, *args, **kwargs):
        super(ZSimpleDialog, self).__init__(*args, **kwargs)
        self.text = text
        self.dialog_type = dialog_type

        # Buttons
        if self.dialog_type == Gtk.MessageType.QUESTION:
            buttons = Gtk.ButtonsType.YES_NO
        else:
            buttons = Gtk.ButtonsType.OK
        # Dialog
        self.dialog = Gtk.MessageDialog(
            parent=None,
            flags=0,
            type=self.dialog_type,
            buttons=buttons,
            message_format=None
        )
        self.init_dialog()

    def init_dialog(self):
        super(ZSimpleDialog, self).init_dialog()
        if self.text:
            self.dialog.set_markup(self.text)


class ZEntry(Base):
    def __init__(self, text, placeholder, *args, **kwargs):
        super(ZEntry, self).__init__(*args, **kwargs)
        self.text = text
        self.placeholder = placeholder
        # Widget
        self.entry_widget = Gtk.Entry()
        self.entry_widget.show()
        # Focus on the text input
        self.entry_widget.set_activates_default(True)
        # Dialog
        self.dialog = Gtk.Dialog()
        self.init_dialog()

    def init_dialog(self):
        super(ZEntry, self).init_dialog()

        if self.placeholder:
            self.entry_widget.set_text(self.placeholder)

        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK
        )
        self.dialog.set_default(
            self.dialog.get_widget_for_response(
                Gtk.ResponseType.OK
            )
        )

    def set_response(self, response):
        if response == Gtk.ResponseType.OK:
            self.response = self.entry_widget.get_text()


class ZEntryMessage(ZEntry):
    def __init__(self, *args, **kwargs):
        super(ZEntryMessage, self).__init__(*args, **kwargs)

    def init_dialog(self):
        super(ZEntryMessage, self).init_dialog()
        # Display text on the dialog before the input
        if self.text:
            text_label = Gtk.Label()
            text_label.set_text(self.text)
            text_label.show()
            self.dialog.get_content_area().add(text_label)
        self.dialog.get_content_area().add(self.entry_widget)


class ZEntryPassword(ZEntry):
    def __init__(self, *args, **kwargs):
        super(ZEntryPassword, self).__init__(*args, **kwargs)

    def init_dialog(self):
        super(ZEntryPassword, self).init_dialog()
        hb_up = Gtk.HBox(spacing=20)
        hb_up.show_all()

        # Password icon
        icon = Gtk.Image()
        icon.set_from_stock(Gtk.STOCK_DIALOG_AUTHENTICATION, Gtk.IconSize.DIALOG)
        icon.show()
        hb_up.add(icon)
        # Text display on the dialog
        if self.text:
            text_label = Gtk.Label()
            text_label.set_text(self.text)
            text_label.show()
            hb_up.add(text_label)
        self.dialog.get_content_area().add(hb_up)

        hb_down = Gtk.HBox(spacing=20)
        hb_down.show_all()

        hb_down.add(self.entry_widget)
        self.dialog.get_content_area().add(hb_down)
        self.entry_widget.set_visibility(False)


class ZList(Base):
    def __init__(self, columns, items, print_columns, text, *args, **kwargs):
        super(ZList, self).__init__(*args, **kwargs)
        self.columns = columns
        self.items = items
        self.print_columns = print_columns
        self.text = text
        self.selection = None
        self.dialog = Gtk.Dialog()
        self.init_dialog()

    def init_dialog(self):
        super(ZList, self).init_dialog()
        len_col = len(self.columns)
        coltypes = [str] * len_col
        store = Gtk.ListStore(*coltypes)

        # Zenity's Example is filling the cells row by row
        # (https://help.gnome.org/users/zenity/stable/list.html.en)
        # To imitate this we probably need a helper to flatten the items
        # example: [1,2,3,4,5] -> (1,2,3), (4,5,'')
        def group(items, nb_cols):
            for i in range(0, len(items), nb_cols):
                group = items[i:i+nb_cols]
                if len(group) == nb_cols:
                    yield(tuple(group))
                else:
                    # fill empty indices with empty string
                    yield(tuple(group + ['']*(nb_cols-len(group))))

        for g in group(self.items, len_col):
            store.append(g)

        cell = Gtk.CellRendererText()
        treeview = Gtk.TreeView(store)
        treeview.set_border_width(40)
        treeview.show()
        treeview.get_selection().connect("changed", self._on_item_selected)

        for i, column in enumerate(self.columns):
            tvcolumn = Gtk.TreeViewColumn(column)
            tvcolumn.set_sort_column_id(0)
            tvcolumn.pack_start(cell, True)
            tvcolumn.add_attribute(cell, 'text', i)
            treeview.append_column(tvcolumn)

        hb = Gtk.HBox()
        hb.show()
        frame = Gtk.Frame()
        if self.text:
            label = Gtk.Label()
            label.set_text(self.text)
            label.show()
            frame.set_label(self.text)
        frame.show()
        scrolledwindow = Gtk.ScrolledWindow(expand=True)
        scrolledwindow.show()
        scrolledwindow.add(treeview)
        frame.add(scrolledwindow)
        hb.pack_start(frame, True, True, 10)
        vb = self.dialog.get_content_area()
        vb.set_spacing(10)
        vb.add(hb)
        self.dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.dialog.set_default(
            self.dialog.get_widget_for_response(
                Gtk.ResponseType.OK))

    def _on_item_selected(self, selection):
        model, treeiter = selection.get_selected()
        if not treeiter:
            self.selection = None
            return
        if self.print_columns is None:
            self.selection = [x for x in model[treeiter]]
        else:
            try:
                self.selection = [model[treeiter][self.print_columns]]
            except IndexError:
                print("Error: Column index out of range")
            except TypeError:
                print("Error: Column index must be integer")

    def set_response(self, response):
        if response == Gtk.ResponseType.OK:
            self.response = self.selection


class ZFileSelection(Base):
    def __init__(self, multiple, directory, save, confirm_overwrite,
                 filename, *args, **kwargs):
        super(ZFileSelection, self).__init__(*args, **kwargs)
        self.multiple = multiple
        self.directory = directory
        self.save = save
        self.confirm_overwrite = confirm_overwrite
        self.filename = filename
        self.dialog = Gtk.FileChooserDialog(
            buttons=(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK)
        )
        self.init_dialog()

    def init_dialog(self):
        super(ZFileSelection, self).init_dialog()
        if not self.save and self.multiple:
            self.dialog.set_select_multiple(True)
        if self.directory:
            self.dialog.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        if self.save:
            self.dialog.set_action(Gtk.FileChooserAction.SAVE)
        if self.confirm_overwrite:
            self.dialog.set_do_overwrite_confirmation(True)
        if self.filename:
            self.dialog.set_filename(self.filename)

    def set_response(self, response):
        if response == Gtk.ResponseType.OK:
            if self.multiple:
                self.response = self.dialog.get_filenames()
            else:
                self.response = self.dialog.get_filename()


class ZCalendar(Base):
    def __init__(self, text, day, month, *args, **kwargs):
        super(ZCalendar, self).__init__(*args, **kwargs)
        self.text = text
        self.day = day
        self.month = month
        self.calendar = Gtk.Calendar()
        self.dialog = Gtk.Dialog()
        self.init_dialog()

    def init_dialog(self):
        super(ZCalendar, self).init_dialog()
        vb = Gtk.VBox()
        vb.show()
        hb = Gtk.HBox()
        hb.show()

        if self.text:
            # justify label on the left
            halign = Gtk.Alignment(xalign=0, yalign=1, xscale=0, yscale=0)
            halign.show()
            text_info = Gtk.Label(self.text)
            text_info.show()
            text_info.set_justify(Gtk.Justification.LEFT)
            halign.add(text_info)
            hb.pack_start(halign, True, True, 10)
            vb.pack_start(hb, True, True, 10)

        if self.day:
            self.calendar.select_day(self.day)
        if self.month:
            self.calendar.select_month(self.month)

        self.calendar.show()
        self.calendar.connect('day-selected-double-click', self._day_selected, None)
        vb.add(self.calendar)

        self.dialog.get_content_area().add(vb)
        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK)
        self.dialog.set_default(
            self.dialog.get_widget_for_response(
                Gtk.ResponseType.OK))

    def _day_selected(self, calendar, event):
        self.dialog.response(Gtk.ResponseType.OK)

    def set_response(self, response):
        if response == Gtk.ResponseType.OK:
            self.response = self.calendar.get_date()


class ZScale(Base):
    def __init__(self, text, value, min, max, step, draw_value, *args, **kwargs):
        super(ZScale, self).__init__(*args, **kwargs)
        self.text = text
        adjustement = Gtk.Adjustment(value, min, max, step, 0, 0)
        self.scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL,
            adjustment=adjustement)
        self.scale.set_draw_value(draw_value)
        self.dialog = Gtk.Dialog()
        self.init_dialog()

    def init_dialog(self):
        super(ZScale, self).init_dialog()
        vb = Gtk.VBox()
        vb.show()
        hb = Gtk.HBox()
        hb.show()

        if self.text:
            # justify label on the left
            halign = Gtk.Alignment(xalign=0, yalign=1, xscale=0, yscale=0)
            halign.show()
            text_info = Gtk.Label(self.text)
            text_info.show()
            text_info.set_justify(Gtk.Justification.LEFT)
            halign.add(text_info)
            hb.pack_start(halign, True, True, 10)
            vb.pack_start(hb, True, True, 10)

        # scale settings
        self.scale.show()
        self.scale.set_digits(0)
        vb.add(self.scale)

        self.dialog.get_content_area().add(vb)
        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,)
        self.dialog.set_default(
            self.dialog.get_widget_for_response(
                Gtk.ResponseType.OK))

    def set_response(self, response):
        if response == Gtk.ResponseType.OK:
            self.response = self.scale.get_adjustment().get_value()


class ZColorSelection(Base):
    def __init__(self, show_palette, opacity_control, *args, **kwargs):
        super(ZColorSelection, self).__init__(*args, **kwargs)
        self.dialog = Gtk.ColorSelectionDialog()
        self.dialog.get_color_selection().set_has_palette(show_palette)
        self.opacity_control = opacity_control
        self.dialog.get_color_selection().set_has_opacity_control(opacity_control)
        self.init_dialog()

    def set_response(self, response):
        if response == Gtk.ResponseType.OK:
            self.response = self.dialog.get_color_selection().get_current_rgba().to_string()


def _simple_dialog(dialog_type, text, title,
                   width, height, timeout):
    dialog = ZSimpleDialog(dialog_type, text,
                           title, width, height, timeout)
    dialog.run()
    return dialog.response


def message(title="", text="", width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT, timeout=None):
    """
    Display a simple message

    :param text: text inside the window
    :type text: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    """
    return _simple_dialog(Gtk.MessageType.INFO,
                          text, title, width, height, timeout)


def error(title="", text="", width=DEFAULT_WIDTH,
          height=DEFAULT_HEIGHT, timeout=None):
    """
    Display a simple error

    :param text: text inside the window
    :type text: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    """
    return _simple_dialog(Gtk.MessageType.ERROR,
                          text, title, width, height, timeout)


def warning(title="", text="", width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT, timeout=None):
    """
    Display a simple warning

    :param text: text inside the window
    :type text: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    """
    return _simple_dialog(Gtk.MessageType.WARNING,
                          text, title, width, height, timeout)


def question(title="", text="", width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, timeout=None):
    """
    Display a question, possible answer are yes/no.

    :param text: text inside the window
    :type text: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    :return: The answer as a boolean
    :rtype: bool
    """
    response = _simple_dialog(Gtk.MessageType.QUESTION, text, title, width, height, timeout)
    if response == Gtk.ResponseType.YES:
        return True
    elif response == Gtk.ResponseType.NO:
        return False
    return None


def entry(text="", placeholder="", title="",
          width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, timeout=None):
    """
    Display a text input

    :param text: text inside the window
    :type text: str
    :param placeholder: placeholder for the input
    :type placeholder: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    :return: The content of the text input
    :rtype: str
    """
    dialog = ZEntryMessage(text, placeholder, title,
                           width, height, timeout)
    dialog.run()
    return dialog.response


def password(text="", placeholder="", title="",
             width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, timeout=None):
    """
    Display a text input with hidden characters

    :param text: text inside the window
    :type text: str
    :param placeholder: placeholder for the input
    :type placeholder: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    :return: The content of the text input
    :rtype: str
    """
    dialog = ZEntryPassword(text, placeholder, title,
                            width, height, timeout)
    dialog.run()
    return dialog.response


def zlist(columns, items, print_columns=None,
          text="", title="", width=DEFAULT_WIDTH,
          height=ZLIST_HEIGHT, timeout=None):
    """
    Display a list of values

    :param columns: a list of columns name
    :type columns: list of strings
    :param items: a list of values
    :type items: list of strings
    :param print_columns: index of a column (return just the values from this column)
    :type print_columns: int (None if all the columns)
    :param text: text inside the window
    :type text: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    :return: A row of values from the table
    :rtype: list
    """
    dialog = ZList(columns, items, print_columns,
                   text, title, width, height, timeout)
    dialog.run()
    return dialog.response


def file_selection(multiple=False, directory=False, save=False,
                   confirm_overwrite=False, filename=None,
                   title="", width=DEFAULT_WIDTH,
                   height=DEFAULT_HEIGHT, timeout=None):
    """
    Open a file selection window

    :param multiple: allow multiple file selection
    :type multiple: bool
    :param directory: only directory selection
    :type directory: bool
    :param save: save mode
    :type save: bool
    :param confirm_overwrite: confirm when a file is overwritten
    :type confirm_overwrite: bool
    :param filename: placeholder for the filename
    :type filename: str
    :param text: text inside the window
    :type text: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    :return: path of files selected.
    :rtype: string or list if multiple enabled
    """
    dialog = ZFileSelection(multiple, directory, save,
                            confirm_overwrite, filename,
                            title, width, height, timeout)
    dialog.run()
    return dialog.response


def calendar(text="", day=None, month=None, title="",
             width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, timeout=None):
    """
    Display a calendar

    :param text: text inside the window
    :type text: str
    :param day: default day
    :type day: int
    :param month: default month
    :type month: int
    :param text: text inside the window
    :type text: str
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    :return: (year, month, day)
    :rtype: tuple
    """
    dialog = ZCalendar(text, day, month,
                       title, width, height, timeout)
    dialog.run()
    return dialog.response


def color_selection(show_palette=False, opacity_control=False, title="",
                    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, timeout=None):
    """
    Display a color selection dialog

    :param show_palette: hide/show the palette with preselected colors
    :type show_palette: bool
    :param opacity_control: allow to control opacity
    :type opacity_control: bool
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    :return: the color selected by the user
    :rtype: str
    """
    dialog = ZColorSelection(show_palette, opacity_control, title, width, height, timeout)
    dialog.run()
    return dialog.response


def scale(text="", value=0, min=0 ,max=100, step=1, draw_value=True, title="",
          width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, timeout=None):
    """
    Select a number with a range widget

    :param text: text inside window
    :type text: str
    :param value: current value
    :type value: int
    :param min: minimum value
    :type min: int
    :param max: maximum value
    :type max: int
    :param step: incrementation value
    :type step: int
    :param draw_value: hide/show cursor value
    :type draw_value: bool
    :param title: title of the window
    :type title: str
    :param width: window width
    :type width: int
    :param height: window height
    :type height: int
    :param timeout: close the window after n seconds
    :type timeout: int
    :return: The value selected by the user
    :rtype: float
    """
    dialog = ZScale(text, value, min, max, step,
                    draw_value, title, width, height, timeout)
    dialog.run()
    return dialog.response
