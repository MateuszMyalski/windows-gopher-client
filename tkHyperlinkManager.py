from tkinter import *

FILENAME_CHAR_WHITELIST = "qwertyuiopasdfghjklzxcvbnm|1234567890._"


class HyperlinkManager:

    def __init__(self, text, downloadFile_handler):
        self.text = text
        self.downloadFile_handler = downloadFile_handler

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.text.tag_bind("hyper", "<Button-2>", self._download)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action, link_details):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)

        self.links[tag] = [action, link_details]
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag][0](self.links[tag][1])
                return

    def _download(self, event):
        link_details = []
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                link_details = self.links[tag][1]

        link_type, link_name, adress, domain, port = link_details
        gopher_url = "gopher://" + domain + ":" + port + adress

        auto_exec_formats = [".gif", ".jpeg", ".jpg", ".bmp", ".png", ".txt"]

        # When middle click on DIR type open new tab
        if link_details[0] == '1':
            import os
            from os import path
            os.path.dirname(os.path.realpath(__file__))
            programm_path = (path.abspath(sys.modules['__main__'].__file__))
            os.system(programm_path + " " + gopher_url)
            return

        link_name = link_name.replace(" ", "_")
        file_type = link_name[-4:].lower()

        if link_type in '01':
            file_type = ".txt"
            link_name += file_type
        elif file_type[0] != '.':
            file_type = ".unknown"
            link_name += file_type

        file_name = ""
        for letter in link_name:
            if not letter.lower() in FILENAME_CHAR_WHITELIST:
                letter = "_"
            file_name += letter

        self.text.config(cursor="watch")
        self.downloadFile_handler(gopher_url, file_name)
        self.text.config(cursor="")

        if file_type in auto_exec_formats:
            import os
            os.path.dirname(os.path.realpath(__file__))
            os.system("start " + file_name)
