from tkinter import *
from tkinter import messagebox
import constans as const


class HyperlinkManager:

    def __init__(self, text, downloadFile_handler):
        self.text = text
        self.downloadFile_handler = downloadFile_handler

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

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
