
# **Runing the Everyday Studio**

If it's the first time do not forget run: 

      git submodule update --init

This will download a git sub-module where is located the weights to inference with the face detector (also is executed by the bash script `make_video.sh`, so no worries after all).

Then to start the visual studio is just simple as running in the root of the project:

    bash make_video.sh

This script will do:

1. source the environment variables located in the configs folders
2. Download associated git sub-modules.
3. copy and rename the file of the weight of the face detector downloaded by the git sub-module into the configs folder.
4. download a example dataset if the env-var `DOWNLOAD_EXAMPLE_DATASET` is specified in `env_vars.sh`
5. run the python script of the every day-studio.

And thats all, you should see a window displaying the last image in the data set.


Check and read the environment variables specified in `env_vars.sh` for more configs and parameters in the pre-visualization and exporting process, also here you setup the video exportation parameters and other face features related to it, for example here you can change the size of the visualization window, the size of the video to export, if you want the final video in gray scale or with the face detection, and so on, just check the variables and play with them.


<br />

### **Possible error running the stack**

when running the stack is possible to get this error:

    (every_day_studio_FACE_CORRECTION:1899): Gdk-ERROR **: 13:12:10.769: The program 'every_day_studio_FACE_CORRECTION' received an X Window System error.
    This probably reflects a bug in the program.
    The error was 'BadAccess (attempt to access private resource denied)'.
    (Details: serial 370 error_code 10 request_code 130 (MIT-SHM) minor_code 1)
    (Note to programmers: normally, X errors are reported asynchronously;
    that is, you will receive the error a while after causing it.
    To debug your program, run it with the GDK_SYNCHRONIZE environment
    variable to change this behavior. You can then get a meaningful
    backtrace from your debugger if you break on the gdk_x_error() function.)
    make_video.sh: line 22:  1899 Trace/breakpoint trap   (core dumped) python3 "${PWD%}/dev_ws/src/everyday_studio/every_day_maker.py"

if you get it just run again until works, it's not usual to happen but this is a common error associated to the communication of interfaces with dev-environment and the host machine.

<br />

### **Using Your Own Dataset**

To use your dataset is so simply as coping your images of your ugly face in the subfolder images located in the `media` folder in the `dev_ws`(work space) path.

The recommendation is using a folder for every year of your pictures as is shown below: 

keep in mind that the stack only will takes the images in format `png`, `jpg`. If other formats are used go to the code and add the new one, and make a PR, but these are the most used formats by phones (never use raw, too heavy).

<br />

### **Using the Studio**

You 


<br />

### **Exporting videos**

<br />
<br />

