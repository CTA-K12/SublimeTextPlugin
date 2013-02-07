import string
import sublime_plugin
import re

class SaveandcloseCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('save')
        self.window.run_command('close')

class ReindentallCommand(sublime_plugin.WindowCommand):
    def run(self):
        #self.window.run_command('select_all')
        self.window.run_command('oddspace')
        self.window.run_command('reindent')

class FinishCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('select_all')
        self.window.run_command('oddspace')
        self.window.run_command('reindent')
        self.window.run_command('save')
        self.window.run_command('close')

class Transformer(sublime_plugin.TextCommand):
    def run(self, edit):
        self.transform(self.transformer[0], self.view, edit)

    def transform(self, f, view, edit):
        for s in view.sel():
            if s.empty():
                s = view.word(s)

            txt = f(view.substr(s))
            view.replace(edit, s, txt)

class OddspaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        r = v.sel()
        c = []
        for s in r:
            q=self.view.substr(s).split("\n")
            for l in q:
                k = (l.__len__() - l.lstrip().__len__()) % 4
                if k:
                    l=l[k:]
                c.append(l)
            v.replace(edit, s, "\n".join(c))

#1
 #1
  #1
   #1
    #1
     #1
      #1
       #1
        #1
         #1
          #1



def rot13(ch):
    o = ord(ch)
    if o >= ord('a') and o <= ord('z'):
        return unichr((o - ord('a') + 13) % 26 + ord('a'))
    if o >= ord('A') and o <= ord('Z'):
        return unichr((o - ord('A') + 13) % 26 + ord('A'))
    return ch

class RotCommand(Transformer):
    transformer = lambda s: "".join([rot13(ch) for ch in s]),
