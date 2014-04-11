import sublime, sublime_plugin, subprocess, platform, urllib, os


def plugin_loaded():
    global cs_settings
    cs_settings = sublime.load_settings('SublimeJAD.sublime-settings')
    call_default_command(sublime.active_window().active_view())

class JavaJadCommand(sublime_plugin.TextCommand):
    def run(self, edit, new_view = False):
        filename = self.view.file_name()
        text, errormessages = self.decompile(filename)
        if 'Not a class file' not in str(errormessages):
            populate_view(self, edit, text, filename, new_view)

    def decompile(self, filename):
        executable = cs_settings.get('java_jad_path')
        filepath, extension = os.path.splitext(filename)
        #print('SublimeJAD decompile: ' + str(filename))
        command = [executable, '-o', '-p', filename]
        return exec_command(command)

class JavaJavapCommand(sublime_plugin.TextCommand):
    def run(self, edit, new_view = False):
        filename = self.view.file_name()
        text, errormessages = self.disassemble(filename)
        if 'class not found' not in str(errormessages):
            populate_view(self, edit, text, filename, new_view)

    def disassemble(self, filename):
        executable = cs_settings.get('java_javap_path')
        filepath, extension = os.path.splitext(filename)
        #print('SublimeJAD disassemble: ' + str(filename))
        basename = os.path.basename(filepath)
        dirname = os.path.dirname(filepath)
        command = [executable, '-c', '-l', '-private', '-verbose', '-classpath', dirname, basename]
        return exec_command(command)

class JavaJadUndoCommand(sublime_plugin.WindowCommand):
    def run(self, forward = False, fallback_command = False, fallback_scope = 'window', fallback_args = {}):
        #print('Call undo ')
        self.window.active_view().set_read_only(False)
        self.window.active_view().set_scratch(False)
        self.window.run_command('undo')

class OpenClassFileCommand(sublime_plugin.EventListener):
    def on_load(self, view):
        call_default_command(view)


def exec_command(command):
    #print('Execute command:' + str(command))
    os_alias = platform.system().lower()
    if 'windows' in os_alias:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
        out, err = p.communicate()
        if err:
            print('Command executed, errors:' + str(err))
        fixed = out.decode("utf-8").replace('\r\n', '\n')
        return (fixed, err)
    else:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            print('Command executed, errors:' + str(err))
        fixed = out.decode("utf-8")
        return (fixed, err)

def populate_view(self, edit, text, filename, new_view):
    if new_view:
        populate_new_view(self, edit, text, filename)
    else:
        populate_current_view(self.view, edit, text, filename)

def populate_current_view(view, edit, text, filename):
    window = sublime.active_window()
    if view != window.transient_view_in_group(window.active_group()):
        view.set_read_only(False)
        view.set_scratch(True)
        view.replace(edit, sublime.Region(0, view.size()), text)
        view.set_read_only(True)
        view.set_syntax_file('Packages/Java/Java.tmLanguage')

def populate_new_view(self, edit, text, filename):
        new_view = self.view.window().new_file()
        new_view.set_name(filename + '~')
        new_view.insert(edit, 0, text)
        new_view.set_syntax_file('Packages/Java/Java.tmLanguage')

def call_default_command(view):
    filename = view.file_name()
    #print('call_default_command: ' + str(filename))
    extension = os.path.splitext(filename)[1]
    if extension.lower() == ".class" :
        command = cs_settings.get('java_jad_default_command')
        if command:
            view.run_command(command)
