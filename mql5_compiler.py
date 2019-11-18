import sublime, sublime_plugin
import os
import subprocess
import re
import tempfile
from os.path import expandvars

settings = sublime.load_settings("MQL5 Compiler.sublime-settings")

METAEDITOR = settings.get("metaeditor_file")
COMPILELOG = tempfile.gettempdir() + '/compile.log'
EXTENSION  = ['.mq5','mq4']
INC_PATH = expandvars(settings.get("mql5_home"))

class Mql5CompilerCommand(sublime_plugin.TextCommand):

    def init(self):
        view = self.view

        if view.file_name() is not None :
            self.dirname   = os.path.realpath(os.path.dirname(view.file_name()))
            self.filename  = os.path.basename(view.file_name())
            self.extension = os.path.splitext(self.filename)[1]

    def isError(self):
        iserror = False
        if not os.path.exists(METAEDITOR):
            print ("Mql5 Compiler | error: metaeditor64.exe not found")
            iserror = True

        else :
            if self.extension not in EXTENSION:
                print ("Mql5 Compiler | error: Wrong file extension: ({0})".format(self.extension))
                iserror = True

            if self.view.is_dirty():
                print ("Mql5 Compiler | error: Save File before compiling")
                iserror = True
                
        return iserror

    def compile(self):
        proc = subprocess.Popen([METAEDITOR,"/compile:"+self.filename,"/log:"+COMPILELOG,"/inc:"+INC_PATH],
        cwd= self.dirname,
        stdout=subprocess.PIPE,
        shell=False,
        startupinfo=None)
        return proc.stdout.read()

    def showCompileLog(self):
        with open(COMPILELOG, 'r', encoding='utf-16') as myfile:
            content = myfile.read()
        window = self.view.window()

        new_view = window.create_output_panel("mql5log")
        new_view.run_command('erase_view')
        new_view.run_command('append', {'characters': content})
        window.run_command("show_panel", {"panel": "output.mql5log"})

        sublime.status_message('Metaeditor64')

        pass

    def run(self , edit):
        self.init()
        if self.isError():
            return

        self.compile()
        self.showCompileLog()
