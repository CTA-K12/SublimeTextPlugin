import string
import sublime_plugin

class SaveandcloseCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('save')
        self.window.run_command('close')

class ReindentallCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('select_all')
        self.window.run_command('reindent')

class Transformer(sublime_plugin.TextCommand):
    def run(self, edit):
        self.transform(self.transformer[0], self.view, edit)

    def transform(self, f, view, edit):
        for s in view.sel():
            if s.empty():
                s = view.word(s)

            txt = f(view.substr(s))
            view.replace(edit, s, txt)

def rot13(ch):
    o = ord(ch)
    if o >= ord('a') and o <= ord('z'):
        return unichr((o - ord('a') + 13) % 26 + ord('a'))
    if o >= ord('A') and o <= ord('Z'):
        return unichr((o - ord('A') + 13) % 26 + ord('A'))
    return ch

class RotCommand(Transformer):
    transformer = lambda s: "".join([rot13(ch) for ch in s]),
