import socket
from urllib.parse import urlparse

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

import tkHyperlinkManager

DEFAULT_ADRESS = r"gopher://gopher.floodgap.com:70"
# DEFAULT_ADRESS = r"gopher://gopher.floodgap.com:70/7/v2/vs"


# STYLES ----------------------------------------------------------------------
FONT = "fixedsys"
FONT_SIZE = "9"
FONT_COLOR = "white"
HYPERLINK_COLOR = "green"
BACKGROUND_COLOR = "black"

# TYPES TO STRING -------------------------------------------------------------
TYPENAME = {'0': '<TEXT>',
            '1': '<DIR>',
            '2': '<CSO>',
            '3': '<ERROR>',
            '4': '<BINHEX>',
            '5': '<DOS>',
            '6': '<UUENCODE>',
            '7': '<SEARCH>',
            '8': '<TELNET>',
            '9': '<BINARY>',
            '+': '<REDUNDANT>',
            's': '<SOUND>',
            'h': '<HTML>',
            'g': '<GIF>',
            'i': '',
            }

# IMPORTANT CONSTANTS ---------------------------------------------------------
CRLF = '\r\n'
TAB = '\t'

MAX_HISTORY_LIST = 20
HISTORY_LIST = []


def openConnection(domain, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = socket.gethostbyname(domain)
    except socket.gaierror:
        raise
        
    try:
        s.connect((host_ip, 70))
    except:
        raise

    return s


def getData(connection, command=""):
    command += CRLF
    received = "ERROR"
    try:
        connection.send(command.encode())
        connection.settimeout(2)
        received = connection.makefile("rb")
    except:
        raise
    finally:
        connection.close()

    return received


def parseMenuItem(line):
    # Slice the line
    menu_item = line.replace("\r\n", "")
    menu_item_details = []
    menu_item_details.append(menu_item[0:1])
    menu_item = menu_item[1:]
    menu_item_details += menu_item.split(TAB)

    # International message
    if line.startswith("i") and line.endswith("1" + CRLF):
        line = line[1:]
        line = line[:-3]
        line += CRLF
        return line

    # Valid menu item consist:
    # type:name:adress:domain:port
    if len(menu_item_details) != 5:
        return line

    item_name = TYPENAME[menu_item_details[0]] + \
        TAB + menu_item_details[1] + CRLF

    return (item_name,
            menu_item_details[0],
            menu_item_details[2],
            menu_item_details[3],
            menu_item_details[4],
            )


class App(Tk):
    """Gopher windows client."""

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # WINDOW`S MENU -------------------------------------------------------
        MainMenu(self)

        # SETUP FRAME WRAPPERS ------------------------------------------------
        top_wrapper = Frame(self)
        main_wrapper = Frame(self)
        bottom_wrapper = Frame(self)

        top_wrapper.pack(side="top", fill=X)
        main_wrapper.pack(fill="both", expand=True)
        bottom_wrapper.pack(side="bottom")

        main_wrapper.grid_rowconfigure(0, weight=1)
        main_wrapper.grid_columnconfigure(0, weight=1)


        # ADRESS & BUTTONS ----------------------------------------------------
        back_button = Button(top_wrapper, text="BACK",
                             width=10, command=self._back)
        back_button.pack(side=LEFT, padx=3)

        self.adress_field = Entry(top_wrapper)
        self.adress_field.insert(0, DEFAULT_ADRESS)
        self.adress_field.pack(side=LEFT, fill=X, expand=True, padx=3)

        go_button = Button(top_wrapper, text="GO", width=40, command=self.go)
        go_button.pack(side=RIGHT, padx=3)

        # STATUS BAR ----------------------------------------------------------
        self.process_name = ""
        self.process_value = ""
        self.statusbar = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(fill=X)
        self.statusbar.config(text=self.process_name+self.process_value)

        self.browserFrame = BrowserPage(main_wrapper, self)
        self.browserFrame.grid(row=0, column=0, sticky="nsew")
        self.browserFrame.tkraise()

        # SHORTCUTS -----------------------------------------------------------
        self.bind("<Return>", self._enter)

        self.go()

    def _back(self):
        """Back in browsing history."""
        try:
            current_index = HISTORY_LIST.index(self.adress_field.get())
        except ValueError:
            current_index = len(HISTORY_LIST)

        self.adress_field.delete(0, END)
        self.adress_field.insert(0, HISTORY_LIST[current_index - 1])
        HISTORY_LIST.pop(-1)

        self.go()

    def _linkClick(self, link_type, domain, adress, port):
        """Describe how programm will behave after clicked on link."""

        url = "gopher://" + domain + ":" + port + adress
        
        # Error type item
        if link_type == '3':
            self._back()
            return 0
        # Search type item
        if link_type == '7':
            query = simpledialog.askstring("Search", "Enter query")
            url += "?"+query

        self.adress_field.delete(0, END)
        self.adress_field.insert(0, url)
        self.go()

    def _enter(self, evt):
        """Enter event handler handler"""
        self.go()

    def go(self):
        """Connect & translate the page."""

        # Prepare information about connection
        parsed_url = urlparse(self.adress_field.get())
        scheme = parsed_url.scheme
        domain = parsed_url.hostname
        adress = parsed_url.path
        port = parsed_url.port
        query = parsed_url.query

        # When not start with gopher:// process to Veronica
        if scheme != "gopher":
            domain = "gopher.floodgap.com"
            adress = "v2/vs"
            port = 70
            query = self.adress_field.get()

        # When URL have arguments
        if query:
            query = "\t" + query

        # Append visited site in history
        if not len(HISTORY_LIST) <= MAX_HISTORY_LIST:
            HISTORY_LIST.pop(0)

        if not len(HISTORY_LIST) == 0:
            if not HISTORY_LIST[-1] == self.adress_field.get():
                HISTORY_LIST.append(self.adress_field.get())
        else:
            HISTORY_LIST.append(self.adress_field.get())

        # Prepare browser screen for new data
        browser = self.browserFrame.browser_area
        hyperlink_manager = tkHyperlinkManager.HyperlinkManager(browser)
        browser.config(state=NORMAL)
        browser.delete('1.0', END)

        # Establish connection
        try:
            connection = openConnection(domain, port)
            page_source = getData(connection, adress + query)
        except Exception as e:
            browser.insert(INSERT, repr(e), "error")
            return 0

        import os
        os.system('cls')
        # Parse received data
        for line in page_source.readlines():
            print(line)
            line = line.decode("UTF-8")

            if not line:
                line = 'Problem while displaying line.'
                browser.insert(INSERT, line)
                break

            # END OF PAGE
            if line.replace(CRLF, "") == '.':
                continue

            # I don`t why I get it sometimes.
            line = line.replace("error.host", "")
            line = line.replace("null.host", "")

            # Known type of line
            if line.startswith(tuple(TYPENAME.keys())):
                parsed_line = parseMenuItem(line)

                if type(parsed_line) == tuple:
                    browser.insert(INSERT,
                                   parsed_line[0],
                                   hyperlink_manager.add(
                                       self._linkClick,
                                       parsed_line[1],
                                       parsed_line[2],
                                       parsed_line[3],
                                       parsed_line[4]
                                   ))
                else:
                    browser.insert(INSERT, parsed_line)
                continue

            browser.insert(INSERT, line)

        browser.config(state=DISABLED)


class BrowserPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.browser_area = Text(self,
                                 bg=BACKGROUND_COLOR,
                                 fg=FONT_COLOR,
                                 font=FONT + ' ' + FONT_SIZE,
                                 spacing1=5,
                                 spacing2=10
                                 )
        self.browser_area.pack(side=LEFT, fill=BOTH, expand=True)

        # BROWSER STYLING -----------------------------------------------------
        hyperlink_font_size = str(int(FONT_SIZE)+2)
        error_font_size = str(int(FONT_SIZE)+5)
        self.browser_area.tag_config(
            "hyper", foreground="green", font=FONT + ' ' + hyperlink_font_size)

        self.browser_area.tag_config(
            "error", foreground="red", font=FONT + ' ' + error_font_size)

        self.browser_area.config(state=DISABLED)

        browser_scrollbar = Scrollbar(self, command=self.browser_area.yview)
        browser_scrollbar.pack(side=RIGHT, fill=Y)
        self.browser_area['yscrollcommand'] = browser_scrollbar.set


class MainMenu:
    # Bookmarks
    # Color scheme
    # Dump page
    # Help
    # Upadate
    def __init__(self, master):
        self.status = 0
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)

        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)


if __name__ == "__main__":
    app = App()
    app.geometry("980x800")
    app.title('GOPHER CLIENT')
    app.mainloop()
