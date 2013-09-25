import string
import sublime, sublime_plugin
import re, os

class SaveandcloseCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('save')
        self.window.run_command('close')

class ReindentandcloseCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('select_all')
        self.window.run_command('oddspace')
        self.window.run_command('reindent')
        self.window.run_command('php_tidy')
        self.window.run_command('save')
        self.window.run_command('close')

class ReindentallCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('select_all')
        self.window.run_command('oddspace')
        self.window.run_command('reindent')
        self.window.run_command('save')

class FinishCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('php_tidy')
        self.window.run_command('save')

class TidyCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('php_tidy')

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

class PrintThemeRule(sublime_plugin.TextCommand):

  def load_theme(self):
    theme = self.view.settings().get('color_scheme')
    # strip the Packages/
    theme = theme[9:]

    path = os.path.join(sublime.packages_path(), theme)
    with open(path, 'r') as f:
      contents = f.read()

    return contents

  def parse_theme(self, theme):
    return re.findall(r'<key>\s*scope\s*</key>\s*<string>([^<]+)</string>', theme)

  def run(self, edit):
    scope_name = self.view.scope_name(self.view.sel()[0].a)
    selectors = self.parse_theme(self.load_theme())
    best, bestScore = '', 0
    for selector in selectors:
      score = sublime.score_selector(scope_name, selector)
      if score > bestScore:
        bestScore = score
        best = selector

    str = "Selector: |%s| Scope: |%s| Score %d " % (best, scope_name, bestScore)
    print str
    sublime.status_message(str)
