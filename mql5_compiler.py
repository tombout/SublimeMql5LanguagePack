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

        if view.file_name() is not None :
            self.dirname   = os.path.realpath(os.path.dirname(view.file_name()))
            self.filename  = os.path.basename(view.file_name())
            self.extension = os.path.splitext(self.filename)[1]

    def isError(self):
        iserror = False
        if not os.path.exists(metaeditor):
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
        settings = sublime.load_settings("SublimeMql5Compiler.sublime-settings")
        metaeditor = settings.get("metaeditor_file")
        log_file = tempfile.gettempdir() + '/compile.log'
        inc_path = expandvars(settings.get("mql5_home"))
        proc = subprocess.Popen([metaeditor,"/compile:"+self.filename,"/log:"+log_file,"/inc:"+inc_path],
        cwd= self.dirname,
        stdout=subprocess.PIPE,
        shell=False,
        startupinfo=None)
        return proc.stdout.read()

    def showlog_file(self):
        with open(log_file, 'r', encoding='utf-16') as myfile:
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
        if self.isError():
            return

        self.compile()
        self.showlog_file()
