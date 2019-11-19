import sublime, sublime_plugin
import os
import subprocess
import re
import tempfile
from os.path import expandvars

EXTENSION  = ['.mq5','mq4']

class Mql5CompilerCommand(sublime_plugin.TextCommand):

    def init(self):
        view = self.view
        self.is_error = True
        self.settings = sublime.load_settings("Mql5LanguagePack.sublime-settings")
        if view.file_name() is not None :
            self.metaeditor = self.settings.get("metaeditor_file")
            self.log_file = tempfile.gettempdir() + '/compile.log'
            self.mql_home = self.settings.get("mql5_home")
            self.inc_path = expandvars(self.mql_home)
            self.dirname   = os.path.realpath(os.path.dirname(view.file_name()))
            self.filename  = os.path.basename(view.file_name())
            self.extension = os.path.splitext(self.filename)[1]
            self.is_error = False
            if not os.path.exists(self.metaeditor):
                print("Mql5Compiler - metaeditor64.exe not found:" + self.metaeditor)
                self.is_error = True
            if self.extension not in EXTENSION:
                print("Mql5Compiler - Wrong file extension: ({0})".format(self.extension))
                self.is_error = True
            if self.view.is_dirty():
                print("Mql5Compiler - Save file before compiling")
                self.is_error = True

    def compile(self):
        proc = subprocess.Popen([self.metaeditor,"/compile:"+self.filename,"/log:"+self.log_file,"/inc:"+self.inc_path],
        cwd= self.dirname,
        stdout=subprocess.PIPE,
        shell=False,
        startupinfo=None)
        return proc.stdout.read()

    def showlog_file(self):
        with open(self.log_file, 'r', encoding='utf-16') as myfile:
            content = myfile.read()
        window = self.view.window()

        new_view = window.create_output_panel("mql5log")
        new_view.run_command('erase_view')
        new_view.run_command('append', {'characters': content})
        window.run_command("show_panel", {"panel": "output.mql5log"})

        sublime.status_message('metaeditor64')

        pass

    def run(self , edit):
        self.init()
        if not self.is_error:
            self.compile()
            self.showlog_file()
