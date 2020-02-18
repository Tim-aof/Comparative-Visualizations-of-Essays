Comparative-Visualizations-of-Essays

The application provided in this repository aims for a more objective basis for
evaluation of AES scored essays. This README will also be available in the folder
after you pulled it. Simply follow the instructions in order to start the application.

Thank you for your interest in this work!

This readme shall help you to install all necessary packages to start the application from this folder.

1. Install Python

The Python version 3.7.4 is used at this point. You can get it here:

https://www.python.org/downloads/release/python-374/

Personally, I use the "Windows x86-64 executable installer", which should work for
most people. But be aware that if your CPU does not support 64-bit or you have an
Apple computer, then you have to choose the appropriate installer file. After the download,
simply follow the installation instruction. Make sure to install "pip" by clicking
on the check box provided. This is the package installer for Python and set the environment
variable in order for Python to work properly. You have to do this BEFORE installation in the setup.
Additionally, after the installation before closing the setup you should click "Disable the path length limit".
After this you can close the setup.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Install packages

Since Bokeh is not a part of the standard library of Python, the package has to installed beforehand.
Open the command prompt or PowerShell. If you are not on Windows the command prompt will be called differently.
Open bash (for Linux) or Terminal (for macOS) in this case. Use the following commands one by one
to install the necessary packages. In order for Bokeh to work properly additional packages will be
installed when calling the command "pip install bokeh" (e.g. Jinja and NumPy). Therefore it could take
some time before the installation is done. You will see a progress bar and the command prompt will
display the appropriate message if the installation was successful. After that, install the pandas package the same way.

> pip install bokeh 
> pip install pandas

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3. Starting the Application

Once again you will need the command prompt in order to start the application.

IMPORTANT: At this point make sure you run the command prompt from the application folder!
Otherwise it will not be able to find the application. Switch to the folder with the command:

> cd \filepath

You can also open the folder manually and then press Shift + right mouse button (into some empty space not on a file!)
to open the context menu. This way you will find a new in the context menu called "Open PowerShell window here" or similar.
This depends of course on the language of the operating system. If you are running your system on German the point
will also be written in German language. If you are in the appropriate folder type one of the following commands into the command prompt:

> bokeh serve --show main.py
> python main.py

Info: The second command would not start the application by default. It only works
since the first command is embedded into the source code.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Infomation:

If you are closing the application and want to start it again make sure to close the command prompt as well. As long as the 
command prompt is running the port will be blocked even if the application itself is closed. In this case you will get the following error:

> Cannot start Bokeh server, port 5006 is already in use
