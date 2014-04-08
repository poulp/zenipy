from unittest import TestCase, main, skip
import gtk

from pythonzenity import Base, PZSimpleDialog, PZEntryMessage, PZEntryPassword


def refresh_gui():
    while gtk.events_pending():
        gtk.main_iteration_do(block=False)

####################################
# TEST
####################################

TEST_TITLE = "Base Title"
TEST_WIDTH = 300
TEST_HEIGHT = 100


class BaseTest(TestCase):
    def setUp(self):
        self._window = Base(
            title=TEST_TITLE,
            width=TEST_WIDTH,
            height=TEST_HEIGHT
        )
        self._window.dialog = gtk.MessageDialog(
            parent=None,
            flags=0,
            type=gtk.MESSAGE_INFO,
            buttons=gtk.BUTTONS_OK,
            message_format=None
        )
        self._window.init_dialog()

    def test_title(self):
        self.assertEqual(TEST_TITLE, self._window.dialog.get_title())

    def test_width(self):
        self.assertEqual(TEST_WIDTH, self._window.dialog.get_size()[0])

    def test_height(self):
        self.assertEqual(TEST_HEIGHT, self._window.dialog.get_size()[1])


class MessageTest(BaseTest):

    def setUp(self):
        self.label = "Message Label"
        self._window = PZSimpleDialog(
            type=gtk.MESSAGE_INFO,
            title=TEST_TITLE,
            width=TEST_WIDTH,
            height=TEST_HEIGHT,
            text="Message Label"
        )

    def test_label(self):
        self.assertEqual("Message Label", self._window.dialog.get_message_area().get_children()[1].get_text())


class EntryTest(BaseTest):

    def setUp(self):
        self._window = PZEntryMessage(
            title=TEST_TITLE,
            width=TEST_WIDTH,
            height=TEST_HEIGHT,
            entry_text="Entry Text"
        )

    def test_entry_text(self):
        self.assertEqual("Entry Text", self._window.entry_widget.get_text())


class EntryPasswordTest(BaseTest):

    def setUp(self):
        self._window = PZEntryPassword(
            title=TEST_TITLE,
            width=TEST_WIDTH,
            height=TEST_HEIGHT,
            entry_text="Entry Text"
        )

    def test_entry_text_is_password(self):
        self.assertFalse(self._window.entry_widget.get_visibility())

if __name__ == "__main__":
    main()
