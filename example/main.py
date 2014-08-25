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

from pypui import Application
from pgi.repository import Gtk


cur_dir = os.path.dirname(os.path.realpath(__file__))
index = os.path.join(cur_dir, "index.html")

app = Application("myapp", index)
app.set_title("Some Title")


@app.register("quit")
def quit():
    app.quit()


@app.register("foo")
def func(*args, **kwargs):
    d = Gtk.Dialog(default_width=300, default_height=300)
    d.add_buttons("Close", Gtk.ResponseType.CLOSE)
    d.get_content_area().add(Gtk.Label(label=repr(args)))
    d.show_all()
    d.run()
    d.destroy()
    return [1,2,3]


if __name__ == "__main__":
    app.start()
