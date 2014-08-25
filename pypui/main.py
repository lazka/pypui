# The MIT License
# 
# Copyright (c) 2014 Christoph Reiter
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import json

from pgi.repository import WebKit, Gtk


class WebWindow(Gtk.Window):

    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, *args, **kwargs)
        self.set_default_size(800, 600)
        scroll = Gtk.ScrolledWindow()
        self._view = view = WebKit.WebView()
        scroll.add(view)
        self.add(scroll)
        self._callback = None
        self._view.connect("console-message", self._log_message)
        self._view.connect("script-alert", self._alert_message)
        self._done = False

    def _log_message(self, view, msg, line, source_id):
        source_id = source_id.decode("utf-8")
        msg = msg.decode("utf-8")
        print("%s(%d): %s" % (source_id.rsplit("/")[-1], line, msg))
        return True

    def set_callback(self, callback):
        self._callback = callback

    def _alert_message(self, view, frame, msg):
        msg = msg.decode("utf-8")
        data = json.loads(msg)
        response_data = self._callback(data)
        if response_data is None:
            response = ''
        else:
            response = json.dumps(response_data)
            response = response.replace("\\", "\\\\")
            response = response.replace("\"", "\\\"")

        self._view.execute_script("PYPUI._send_response('%s');" % response)
        return True

    def load_path(self, path):
        with open(path, "rb") as h:
            self._view.load_string(
                h.read(), "text/html", "UTF-8", "http://pypui.pypui")

    def execute_script(self, data):

        if self._done:
            self._view.execute_script(data)
            return

        def cb(*args):
            self._done = True
            self._view.execute_script(data)

        self._view.connect('load-committed', cb)


class JS(object):

    def __init__(self, window):
        self._window = window

    def __getattr__(self, name):
        def wrap(*args):
            json_data = json.dumps(args)
            json_data = json_data.replace("\\", "\\\\")
            json_data = json_data.replace("\"", "\\\"")
            self._window.execute_script(
                "PYPUI._call_func('%s', '%s');" % (name, json_data))

        return wrap


class Application(object):

    def __init__(self, name, html_path):
        """
        name -- a lowercase name without spaces of the application
        html_path -- path to the HTML file that will be loaded
        """

        self._window = WebWindow()
        self._window.set_callback(self._on_command)
        self._window.connect("delete-event", Gtk.main_quit)

        self.js = JS(self._window)

        self._path = html_path
        self._commands = {}

    def _on_command(self, js):
        name = js["name"]
        args = tuple()
        if "data" in js:
            args = (js["data"],)
        return self._commands[name](*args)

    def register(self, command_name):
        """Register a function, exposed in JS"""

        def wrap(func):
            self._commands[command_name] = func
            return func
        return wrap

    def set_title(self, title):
        """Set the window title"""

        self._window.set_title(title)

    def send_event(self, name, data):
        """Send an event to the client site.

        Data should be representable in JSON.
        """
        raise NotImplementedError

    def quit(self):
        Gtk.main_quit()

    def start(self):
        assert self._path

        # inject js api
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(cur_dir, "api.js"), "rb") as h:
            self._window.execute_script(h.read())

        # register our functions
        for name in self._commands.keys():
            self._window.execute_script("PYPUI._register_function('%s');" % name)

        # load page
        self._window.load_path(self._path)

        # go go go
        self._window.show_all()
        Gtk.main()
