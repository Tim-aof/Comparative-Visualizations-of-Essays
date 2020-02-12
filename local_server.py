from tornado.ioloop import IOLoop

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.server.server import Server

# Launch the server and connect to it.
def main():
    print("Preparing a bokeh application.")
    io_loop = IOLoop.current()
    bokeh_app = Application(FunctionHandler(modify_doc))

    server = Server({"/": bokeh_app}, io_loop=io_loop)
    server.start()
    print("Opening Bokeh application on http://localhost:5006/")

    io_loop.add_callback(server.show, "/")
    io_loop.start()

main()
