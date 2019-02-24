import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog

import errorHandler
import constans as const
import historyFunc as history
import browse

# STYLES ----------------------------------------------------------------------
FONT_SIZE = const.FONT_SIZE
COLOR_SCHEME = const.DARK_SCHEME


def applyScheme(scheme):
    hyperlink_font_size = str(FONT_SIZE + 2)
    error_font_size = str(FONT_SIZE + 5)

    font_color =\
        const.COLOR_SCHEME[scheme]["font_color"]
    hyperlink_color = \
        const.COLOR_SCHEME[scheme]["hyperlink_color"]
    international_message_color = \
        const.COLOR_SCHEME[scheme]["international_message_color"]
    error_color = \
        const.COLOR_SCHEME[scheme]["error_color"]
    background_color = \
        const.COLOR_SCHEME[scheme]["background_color"]
    select_background_color = \
        const.COLOR_SCHEME[scheme]["select_background_color"]

    browser_field.tag_config(
        "hyper",
        foreground=hyperlink_color,
        font=const.FONT + ' ' + hyperlink_font_size
    )
    browser_field.tag_config(
        "error",
        foreground="red",
        font=const.FONT + ' ' + error_font_size
    )
    browser_field.tag_config(
        "international",
        foreground=international_message_color,
        font=const.FONT + ' ' + str(FONT_SIZE)
    )
    browser_field.config(
        bg=background_color,
        fg=font_color,
        font=const.FONT + ' ' + str(FONT_SIZE),
        selectbackground=select_background_color
    )


# MAIN PROGRAMM ---------------------------------------------------------------

# EXECUTE WITH SYSTEM`S ARGS --------------------------------------------------
if len(sys.argv) == 2:
    const.DEFAULT_ADRESS = sys.argv[1]

# LINK BEHAVIOUR --------------------------------------------------------------


def _downloadType(link_details):
    link_type, link_name, adress, domain, port = link_details
    gopher_url = "gopher://" + domain + ":" + port + adress

    auto_exec_formats = [".gif", ".jpeg", ".jpg", ".bmp", ".png", ".txt"]

    link_name = link_name.replace(" ", "_")
    file_type = link_name[-4:].lower()
    if file_type[0] != '.':
        file_type = ".unknown"
        link_name += file_type

    answer = messagebox.askquestion(
        file_type.upper() + " FILE",
        "To open this file you need to download it. Shall I to do that?"
    )

    if answer == "no":
        return 0

    file_name = ""
    for letter in link_name:
        if not letter.lower() in const.FILENAME_CHAR_WHITELIST:
            letter = "_"
        file_name += letter

    try:
        browse.downloadFile(gopher_url, file_name)
    except Exception as ex:
        errorHandler.handle(ex, browser_field)

    if file_type in auto_exec_formats:
        os.path.dirname(os.path.realpath(__file__))
        os.system("start " + file_name)


def _searchType(link_details):
    link_type, link_name, adress, domain, port = link_details
    gopher_url = "gopher://" + domain + ":" + port + adress
    query = simpledialog.askstring(
        "Search",
        "Enter parameters for the remote application"
    )

    if not query:
        return 0

    gopher_url += "?" + query

    adress_field.delete(0, "end")
    adress_field.insert(0, gopher_url)
    go_handler()


# SHORTCUTS BEHAVIOUR ---------------------------------------------------------
def loadPage():
    file_name = filedialog.askopenfilename(
        initialdir=os.path.realpath(__file__),
        title="Select file",
        filetypes=(
            ("All files", "*.*"),
            ("Gopher raw files", "*.gopherraw"),
            ("Text files", "*.txt")
        )
    )

    if file_name:
        with open(file_name, "rb") as file:
            parsePageLocally(file)


def dumpPage(method):
    """Dump page to txt file"""
    file_name = filedialog.asksaveasfilename(
        initialdir=os.path.realpath(__file__),
        defaultextension='.txt',
        title="Select file",
        filetypes=(
            ("Gopher raw files", "*.gopherraw"),
            ("Text files", "*.txt")
        )
    )

    if file_name[-3:] == "txt":
        try:
            with open(file_name, "w") as file:
                file.write(browser_field.get("1.0", "end"))
        except Exception as ex:
            errorHandler.handle(ex, browser_field)

    if file_name[-3:] == "raw":
        try:
            browse.downloadFile(adress_field.get(), file_name)
        except Exception as ex:
            errorHandler.handle(ex, browser_field)


def altColors():
    """Alternate color scheme"""
    global COLOR_SCHEME
    if COLOR_SCHEME == const.DARK_SCHEME:
        COLOR_SCHEME = const.LIGHT_SCHEME
    elif COLOR_SCHEME == const.LIGHT_SCHEME:
        COLOR_SCHEME = const.DARK_SCHEME

    applyScheme(COLOR_SCHEME)


def changeFontSize(inc):
    """Change font size"""
    global FONT_SIZE

    if inc == "+" and FONT_SIZE < 90:
        FONT_SIZE += 3

    if inc == "-" and FONT_SIZE > 1:
        FONT_SIZE -= 3

    applyScheme(COLOR_SCHEME)


def parsePageLocally(file):
    adress_field.delete(0, "end")
    browser_field.config(state="normal", cursor="wait")
    browser_field.delete('1.0', "end")
    import tkHyperlinkManager
    hyperlink_manager = tkHyperlinkManager.HyperlinkManager(
        browser_field,
        browse.downloadFile)

    for line in file:
        parsed_line = browse.parseLine(line, hyperlink_manager)
        browser_field.insert("insert", parsed_line[0], parsed_line[1])

    browser_field.config(state="disabled", cursor="")


def showAbout():
    """Show instruction about client"""
    with open("about.txt", "rb") as file:
        parsePageLocally(file)


def _ctrPressed(event):
    pressedKey = event.keycode

    if pressedKey == 83:
        dumpPage("raw")

    if pressedKey == 189:
        changeFontSize("-")

    if pressedKey == 187:
        changeFontSize("+")


# GUI INIT --------------------------------------------------------------------
browser_app = tk.Tk()
browser_app.geometry(const.DEFAULT_GEOMETRY)
browser_app.title(const.DEFAULT_WINDOW_TITLE)

# SETUP FRAME WRAPPERS --------------------------------------------------------
top_wrapper = tk.Frame(browser_app)
main_wrapper = tk.Frame(browser_app)
bottom_wrapper = tk.Frame(browser_app)

top_wrapper.pack(side="top", fill="x")
main_wrapper.pack(fill="both", expand=True)
bottom_wrapper.pack(side="bottom", fill="x")

main_wrapper.grid_rowconfigure(0, weight=1)
main_wrapper.grid_columnconfigure(0, weight=1)

# ADRESS & BUTTONS ------------------------------------------------------------


def go_handler():
    browser_field.config(cursor="watch")
    try:
        browse.go(adress_field, browser_field)
        history.add(adress_field.get())
    except Exception as ex:
        errorHandler.handle(ex, browser_field)
    browser_field.config(cursor="")


def historyBack_handler(event=None):
    history.back(adress_field, go_handler)


def enterPressed_handler(event):
    go_handler()


def rightClick_handler(event):
    index = browser_field.index("@%s,%s" % (event.x, event.y))
    tag_indices = list(browser_field.tag_ranges('adj'))


def linkClick_handler(link_details):
    print(link_details)
    link_type, link_name, adress, domain, port = link_details
    gopher_url = "gopher://" + domain + ":" + port + adress

    # CLICKABLE type item
    if link_type in "01+":
        adress_field.delete(0, "end")
        adress_field.insert(0, gopher_url)
        go_handler()

    # CSO type item
    if link_details == '2':
        pass

    # ERROR type item
    if link_type == '3':
        historyBack_handler()

    # DOWNLOAD type item
    if link_type in "4569gId":
        _downloadType(link_details)

    # SEARCH type item
    if link_type == '7':
        _searchType(link_details)

    # HTML type item
    if link_type == 'h':
        http_url = link_details[2].replace("URL:", "")
        os.system("start " + http_url)


browse.linkClick = linkClick_handler

adress_field = ttk.Entry(top_wrapper)
back_button = ttk.Button(top_wrapper, text="BACK",
                         width=10, command=historyBack_handler)
go_button = ttk.Button(top_wrapper, text="GO", width=40, command=go_handler)

adress_field.insert(0, const.DEFAULT_ADRESS)
back_button.pack(side="left", padx=3)
adress_field.pack(side="left", fill="x", expand=True, padx=3)
go_button.pack(side="right", padx=3)

# SHORTCUTS BEHAVIOUR ---------------------------------------------------------
browser_app.bind("<Return>", enterPressed_handler)
browser_app.bind("<Button-3>", historyBack_handler)
browser_app.bind("<Control-Key>", _ctrPressed)

# BROWSER TEXT AREA -----------------------------------------------------------
browser_field = tk.Text(main_wrapper, spacing1=5, spacing2=10)
browser_field.pack(side="left", fill="both", expand=True, padx=3, pady=3)

browser_field.config(state="disabled")

browser_scrollbar = tk.Scrollbar(main_wrapper, command=browser_field.yview)
browser_scrollbar.pack(side="right", fill="y")
browser_field['yscrollcommand'] = browser_scrollbar.set

# STYLING APPLYING ------------------------------------------------------------
applyScheme(COLOR_SCHEME)

# WINDOW`S MENU ---------------------------------------------------------------
browser_menubar = tk.Menu(browser_app)

browser_menubar.add_command(label="Save page", command=dumpPage)
browser_menubar.add_command(label="Load page", command=loadPage)
browser_menubar.add_command(label="Alternate color scheme", command=altColors)
browser_menubar.add_command(label="About", command=showAbout)
browser_app.config(menu=browser_menubar)


# STATUS BAR ------------------------------------------------------------------
statusbar = ttk.Label(bottom_wrapper, border=1, relief="sunken", anchor="w")
statusbar.config(text=const.MOTD)
statusbar.pack(fill="x", expand="true")

# MAIN LOOP -------------------------------------------------------------------
go_handler()

browser_app.mainloop()
