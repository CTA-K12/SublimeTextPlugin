import sublime, sublime_plugin

class SaveandexitCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('save')
        self.window.run_command('close')

class Rot13Command(sublime_plugin.TextCommand):
    def run(self, view, args):
        for region in view.sel():
            if not region.empty():
                # Get the selected text
                s = view.substr(region)
                # Transform it via rot13
                s = s.encode('rot13')
                # Replace the selection with transformed text
                view.replace(region, s)