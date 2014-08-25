import os

from pypui import Application
from pgi.repository import Gtk


class MyApp(Application):
    pass


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    index = os.path.join(cur_dir, "index.html")

    app = MyApp("myapp", index)
    app.set_title("Some Title")

    @app.register("foo")
    def func(*args, **kwargs):
        d = Gtk.Dialog(default_width=300, default_height=300)
        d.add_buttons("Close", Gtk.ResponseType.CLOSE)
        d.get_content_area().add(Gtk.Label(label=repr(args)))
        d.show_all()
        d.run()
        d.destroy()

        return [1,2,3]

    app.start()
