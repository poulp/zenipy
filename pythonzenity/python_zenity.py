#! /usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import pygtk
import gtk
import gobject
pygtk.require('2.0')


####################################
# CONSTANTS
####################################
DEFAULT_WIDTH = 330
DEFAULT_HEIGHT = 120

####################################
# WIDGETS
####################################


class Base(object):
    def __init__(self, title=None, width=None, height=None, timeout=None):
        self.title = title
        self.width = width
        self.height = height
        self.timeout = timeout
        self.dialog = None

    def init_dialog(self):
        # global config
        self.dialog.set_resizable(True)

        # default window size
        if self.width < 0 or self.width is None:
            self.width = DEFAULT_WIDTH
        if self.height < 0 or self.height is None:
            self.height = DEFAULT_HEIGHT

        self.dialog.resize(self.width, self.height)
        self.dialog.set_border_width(5)

        if self.timeout:
            gobject.timeout_add(self.timeout, self.destroy)

        if self.title:
            self.dialog.set_title(self.title)

    def run(self):
        rep = self.dialog.run()
        self.dialog.hide()
        return rep

    def destroy(self):
        self.dialog.destroy()


class PZSimpleDialog(Base):
    def __init__(self, type, text=None, *args, **kwargs):
        super(PZSimpleDialog, self).__init__(*args, **kwargs)

        self.text = text
        self.type = type

        if self.type == gtk.MESSAGE_QUESTION:
            buttons = gtk.BUTTONS_YES_NO
        else:
            buttons = gtk.BUTTONS_OK

        self.dialog = gtk.MessageDialog(
            parent=None,
            flags=0,
            type=self.type,
            buttons=buttons,
            message_format=None
        )

        self.init_dialog()

    def init_dialog(self):
        super(PZSimpleDialog, self).init_dialog()

        if self.title:
            self.dialog.set_title(self.title)
        else:
            if self.type == gtk.MESSAGE_INFO:
                self.dialog.set_title("Information")
            if self.type == gtk.MESSAGE_WARNING:
                self.dialog.set_title("Warning")
            if self.type == gtk.MESSAGE_ERROR:
                self.dialog.set_title("Error")
            if self.type == gtk.MESSAGE_QUESTION:
                self.dialog.set_title("Question")

        if self.text:
            self.dialog.set_markup(self.text)
        else:
            if self.type == gtk.MESSAGE_INFO:
                self.dialog.set_markup("All updates are complete.")
            if self.type == gtk.MESSAGE_WARNING:
                self.dialog.set_markup("Continue ?")
            if self.type == gtk.MESSAGE_ERROR:
                self.dialog.set_markup("An error occurred.")
            if self.type == gtk.MESSAGE_QUESTION:
                self.dialog.set_markup("Nice to meet you ?")


class PZEntry(Base):
    def __init__(self, text=None, entry_text=None, *args, **kwargs):
        super(PZEntry, self).__init__(*args, **kwargs)

        self.text = text
        self.entry_text = entry_text

        self.entry_widget = gtk.Entry()
        self.entry_widget.show()
        self.entry_widget.set_activates_default(True)

        self.dialog = gtk.Dialog()

        self.init_dialog()

    def init_dialog(self):
        super(PZEntry, self).init_dialog()

        if self.entry_text:
            self.entry_widget.set_text(self.entry_text)

        self.dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.dialog.set_default(self.dialog.get_widget_for_response(gtk.RESPONSE_OK))


class PZEntryMessage(PZEntry):
    def __init__(self, *args, **kwargs):
        super(PZEntryMessage, self).__init__(*args, **kwargs)

    def init_dialog(self):
        super(PZEntryMessage, self).init_dialog()

        # window title
        if self.title:
            self.dialog.set_title(self.title)
        else:
            self.dialog.set_title("Entry")

        # information label
        text_label = gtk.Label()
        if self.text:
            text_label.set_text(self.text)
        else:
            text_label.set_text("Text : ")
        text_label.show()
        self.dialog.get_content_area().add(text_label)

        self.dialog.get_content_area().add(self.entry_widget)


class PZEntryPassword(PZEntry):
    def __init__(self, *args, **kwargs):
        super(PZEntryPassword, self).__init__(*args, **kwargs)

    def init_dialog(self):
        super(PZEntryPassword, self).init_dialog()

        if self.title:
            self.dialog.set_title(self.title)
        else:
            self.dialog.set_title("Password")

        hb_up = gtk.HBox(spacing=20)
        hb_up.show_all()

        # auth icon
        icon = gtk.Image()
        icon.set_from_stock(gtk.STOCK_DIALOG_AUTHENTICATION, gtk.ICON_SIZE_DIALOG)
        icon.show()
        hb_up.add(icon)

        text_label = gtk.Label()
        if self.text:
            text_label.set_text(self.text)
        else:
            text_label.set_text("Set your password")
        text_label.show()
        hb_up.add(text_label)
        self.dialog.get_content_area().add(hb_up)

        hb_down = gtk.HBox(spacing=20)
        hb_down.show_all()

        input_label = gtk.Label("Password : ")
        input_label.show()
        hb_down.add(input_label)

        hb_down.add(self.entry_widget)
        self.dialog.get_content_area().add(hb_down)

        # pwd property
        self.entry_widget.set_visibility(False)


class PZList(Base):
    def __init__(self, columns, items, print_columns=0, text=None, *args,
                 **kwargs):
        super(PZList, self).__init__(*args, **kwargs)

        self.columns = columns
        self.colnum = len(columns)
        self.items = items
        self.print_columns = print_columns
        self.text = text
        self.selection = None

        self.dialog = gtk.Dialog()
        self.init_dialog()

    def init_dialog(self):
        super(PZList, self).init_dialog()

        if self.title:
            self.dialog.set_title(self.title)
        else:
            self.dialog.set_title("Choose an item from the list")

        label = gtk.Label()
        label.show()
        if self.text:
            label.set_text(self.text)
        else:
            label.set_text("Choose items from the list down below")

        coltypes = [str] * self.colnum
        store = gtk.ListStore(*coltypes)

        # Zenity's Example is filling the cells row by row
        # (https://help.gnome.org/users/zenity/stable/list.html.en)
        # To imitate this we probably need a helper to flatten the items
        # example: [1,2,3,4,5] -> (1,2,3), (4,5,'')
        def group(list, size):
            for i in range(0, len(list), size):
                group = list[i:i+size]
                if len(group) == size:
                    yield(tuple(group))
                else:
                    # fill empty indices with empty string
                    yield(tuple(group + ['']*(size-len(group))))

        for g in group(self.items, self.colnum):
            store.append(g)

        cell = gtk.CellRendererText()
        treeview = gtk.TreeView(store)
        treeview.set_border_width(40)
        treeview.show()
        treeview.get_selection().connect("changed", self._on_item_selected)

        for i, column in enumerate(self.columns):
            tvcolumn = gtk.TreeViewColumn(column)
            tvcolumn.set_sort_column_id(0)
            tvcolumn.pack_start(cell, True)
            tvcolumn.add_attribute(cell, 'text', i)
            treeview.append_column(tvcolumn)

        hb = gtk.HBox()
        hb.show()
        frame = gtk.Frame("Choose items from the list down below")
        frame.show()
        frame.add(treeview)
        hb.pack_start(frame, padding=10)
        self.dialog.get_content_area().add(hb)

        self.dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OK, gtk.RESPONSE_OK,)
        self.dialog.set_default(self.dialog.get_widget_for_response(
            gtk.RESPONSE_OK))

    def _on_item_selected(self, selection):
        model, treeiter = selection.get_selected()
        if not treeiter:
            self.selection = None
            return
        if self.print_columns == 'ALL':
            self.selection = [x for x in model[treeiter]]
        else:
            try:
                self.selection = [model[treeiter][self.print_columns]]
            except IndexError:
                print("Error: Column index out of range")
            except TypeError:
                print("Error: Column index must be integer")


class PZFileSelection(Base):
    def __init__(self, multiple=False, directory=False, save=False, confirm_overwrite=False, filename=None, *args, **kwargs):
        super(PZFileSelection, self).__init__(*args, **kwargs)

        self.multiple = multiple
        self.directory = directory
        self.save = save
        self.confirm_overwrite = confirm_overwrite
        self.filename = filename

        self.dialog = gtk.FileChooserDialog(buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))

        self.init_dialog()

    def init_dialog(self):
        super(PZFileSelection, self).init_dialog()

        if self.title:
            self.dialog.set_title(self.title)
        else:
            self.dialog.set_title("File Chooser")

        if not self.save and self.multiple:
            self.dialog.set_select_multiple(True)

        if self.directory:
            self.dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

        if self.save:
            self.dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)

        if self.confirm_overwrite:
            self.dialog.set_do_overwrite_confirmation(True)

        if self.filename:
            self.dialog.set_filename(self.filename)


class PZCalendar(Base):
    def __init__(self, text_info=None, day=None, month=None, *args, **kwargs):
        super(PZCalendar, self).__init__(*args, **kwargs)
        self.text_info = text_info
        self.day = day
        self.month = month
        self.calendar = gtk.Calendar()
        self.dialog = gtk.Dialog()
        self.init_dialog()

    def init_dialog(self):
        super(PZCalendar, self).init_dialog()

        if self.title:
            self.dialog.set_title(self.title)
        else:
            self.dialog.set_title("Calendar")

        vb = gtk.VBox()
        vb.show()

        hb = gtk.HBox()
        hb.show()

        if self.text_info:
            # justify label on the left
            halign = gtk.Alignment(0, 1, 0, 0)
            halign.show()

            text_info = gtk.Label(self.text_info)
            text_info.show()
            text_info.set_justify(gtk.JUSTIFY_LEFT)
            halign.add(text_info)
            hb.pack_start(halign, padding=10)
            vb.pack_start(hb, padding=10)

        if self.day:
            self.calendar.select_day(self.day)
        if self.month:
            self.calendar.select_month(self.month)

        self.calendar.show()
        self.calendar.connect('day-selected-double-click', self._day_selected, None)
        vb.add(self.calendar)

        self.dialog.get_content_area().add(vb)
        self.dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK,)
        self.dialog.set_default(self.dialog.get_widget_for_response(gtk.RESPONSE_OK))

    def _day_selected(self, calendar, event):
        self.dialog.response(gtk.RESPONSE_OK)


class PZScale(Base):
    def __init__(self, text_info=None, value=0, min=0, max=100, step=1, draw_value=True, *args, **kwargs):
        super(PZScale, self).__init__(*args, **kwargs)
        self.text_info = text_info
        adj2 = gtk.Adjustment(value, min, max, step, 0, 0)
        self.scale = gtk.HScale(adj2)
        if not draw_value:
            self.scale.set_draw_value(False)
        self.dialog = gtk.Dialog()
        self.init_dialog()

    def init_dialog(self):
        super(PZScale, self).init_dialog()

        if self.title:
            self.dialog.set_title(self.title)
        else:
            self.dialog.set_title("Scale")

        vb = gtk.VBox()
        vb.show()

        hb = gtk.HBox()
        hb.show()

        if self.text_info:
            # justify label on the left
            halign = gtk.Alignment(0, 1, 0, 0)
            halign.show()

            text_info = gtk.Label(self.text_info)
            text_info.show()
            text_info.set_justify(gtk.JUSTIFY_LEFT)
            halign.add(text_info)
            hb.pack_start(halign, padding=10)
            vb.pack_start(hb, padding=10)

        # scale settings
        self.scale.show()
        self.scale.set_digits(0)
        vb.add(self.scale)

        self.dialog.get_content_area().add(vb)
        self.dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK,)
        self.dialog.set_default(self.dialog.get_widget_for_response(gtk.RESPONSE_OK))


class PZColorSelection(Base):
    def __init__(self, title="Color Selection", show_palette=False, *args, **kwargs):
        super(PZColorSelection, self).__init__(*args, **kwargs)
        self.dialog = gtk.ColorSelectionDialog(title)
        if show_palette:
            self.dialog.get_color_selection().set_has_palette(True)
        self.init_dialog()

    def init_dialog(self):
        super(PZColorSelection, self).init_dialog()


####################################
# GENERAL FUNCTION
####################################
def Message(**kwargs):
    message = PZSimpleDialog(type=gtk.MESSAGE_INFO, **kwargs)
    return message.run()


def Error(**kwargs):
    error = PZSimpleDialog(type=gtk.MESSAGE_ERROR, **kwargs)
    return error.run()


def Warning(**kwargs):
    warning = PZSimpleDialog(type=gtk.MESSAGE_WARNING, **kwargs)
    return warning.run()


def Question(**kwargs):
    question = PZSimpleDialog(type=gtk.MESSAGE_QUESTION, **kwargs)
    answer = question.run()
    return True if answer == gtk.RESPONSE_YES else False


def Entry(**kwargs):
    entry = PZEntryMessage(**kwargs)
    response = entry.run()
    if response == gtk.RESPONSE_OK:
        return entry.entry_widget.get_text()
    else:
        return None


def Password(**kwargs):
    pwd = PZEntryPassword(**kwargs)
    response = pwd.run()
    if response == gtk.RESPONSE_OK:
        return pwd.entry_widget.get_text()
    else:
        return None


def List(**kwargs):
    listp = PZList(**kwargs)
    l = listp.run()
    if l == gtk.RESPONSE_OK:
        return listp.selection
    else:
        return None


def FileSelection(**kwargs):
    file = PZFileSelection(**kwargs)
    answer = file.run()
    if answer == gtk.RESPONSE_OK:
        if file.multiple:
            return file.dialog.get_filenames()
        else:
            return file.dialog.get_filename()
    else:
        return None


def Calendar(**kwargs):
    calendar = PZCalendar(**kwargs)
    c = calendar.run()
    if c == gtk.RESPONSE_OK:
        return calendar.calendar.get_date()
    else:
        return None


def Scale(**kwargs):
    scale = PZScale(**kwargs)
    s = scale.run()
    if s == gtk.RESPONSE_OK:
        return scale.scale.get_adjustment().get_value()
    else:
        return None


def ColorSelection(**kwargs):
    cs = PZColorSelection(**kwargs)
    color = cs.run()
    if color == gtk.RESPONSE_OK:
        return cs.dialog.get_color_selection().get_current_color().to_string()
    else:
        return None
