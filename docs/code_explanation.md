
# **Everyday Studio**

### **Code Structure:**

Here's the code structure, and small explanation of what every module contains and what it does:

    📦dev_ws
    ┣ 📂configs
    ┃ ┣ 📜env_vars.sh
    ┃ ┗ 📜predictor_landmarks.dat
    ┣ 📂export
    ┃ ┗ 📜every_day.mp4
    ┣ 📂media
    ┃ ┣ 📂images
    ┃ ┗ 📂sound
    ┃ ┃ ┗ 📜track_1.mp3
    ┗ 📂src
    ┃ ┗ 📂everyday_studio
    ┃ ┃ ┣ 📂utils
    ┃ ┃ ┃ ┣ 📜errors.py
    ┃ ┃ ┃ ┗ 📜utils.py
    ┃ ┃ ┣ 📜capture.py
    ┃ ┃ ┣ 📜every_day_maker.py
    ┃ ┃ ┣ 📜face.py
    ┃ ┃ ┗ 📜file_utils.py

**📂 dev_ws**: root code folder containing all the scripts, utils, modules for the everyday studio. 

**📂 [configs](https://github.com/JohnBetaCode/Face-every-day-maker/tree/main/dev_ws/configs)**: Where the config files are located, here you find:
* **📜 [env_vars.sh](https://github.com/JohnBetaCode/Face-every-day-maker/blob/main/dev_ws/configs/env_vars.sh)**: bash script with environment variables defined in the runtime for change everyday studio visuals or export settings.
* **📜 predictor_landmarks.dat**: when you run [make_video.sh](https://github.com/JohnBetaCode/Face-every-day-maker/blob/main/make_video.sh) for the first time this file will appear, and are the weights for the face detection model/process.

**📂 [media](https://github.com/JohnBetaCode/Face-every-day-maker/tree/main/dev_ws/media)**: contain all resources and media files for the project:
* 📂 images: here all images or dataset images should be allocated.
* 📂 [sound](https://github.com/JohnBetaCode/Face-every-day-maker/tree/main/dev_ws/media/sound): audio files to chose when exporting a video.

**📂 [src/everyday_studio](https://github.com/JohnBetaCode/Face-every-day-maker/tree/main/dev_ws/src/everyday_studio)**: folder containing source code of the everyday studio: modules, utils, scripts, functions, and so on. in src folder, also git sub-modules are located.


### **Code Explanation:**

Let's first explore how the everyday studio source code is composed: 

    ┗ 📂everyday_studio
    ┃ ┣ 📂utils
    ┃ ┃ ┣ 📜errors.py
    ┃ ┃ ┗ 📜utils.py
    ┃ ┣ 📜capture.py
    ┃ ┣ 📜every_day_maker.py
    ┃ ┣ 📜face.py
    ┃ ┗ 📜file_utils.py

that's almost everything. When the bash script [make_video.sh](https://github.com/JohnBetaCode/Face-every-day-maker/blob/main/make_video.sh) is executed, the `main()` function of [every_day_maker.py](https://github.com/JohnBetaCode/Face-every-day-maker/blob/main/dev_ws/src/everyday_studio/every_day_maker.py) is compiled, and what is done here is create and instance of the class `Studio` and execute its method `run()`.

An instance of the class `Studio`will load some environment variables, and create 3 instances of other important classes: 
* [DataSet](https://github.com/JohnBetaCode/Face-every-day-maker/blob/main/dev_ws/src/everyday_studio/every_day_maker.py) loads and handles the dataset specified through environment variable.
* [FaceDetector](https://github.com/JohnBetaCode/Face-every-day-maker/blob/main/dev_ws/src/everyday_studio/file_utils.py) loads and handles the face detector model and visuals
* [VideoWriter](https://github.com/JohnBetaCode/Face-every-day-maker/blob/main/dev_ws/src/everyday_studio/capture.py) handles the everyday video exportation 

In the `run()` method there's an no end-loop with a while method, here is display the last image by default in the dataset loaded, if any error occurs during the visualization of a image in the dataset or an error in this last one, a black image will be shown. Here. the a OpenCV window waits for an user input, to display and show help, press the key `H`.

Maybe the most important method in the `Studio` instance is `export_video`, when you press the Key `C` the exportation process is started and then the dataset will be taken from its first element o the last one, and every image from it is passed to the `VideoWriter` instance to export the video, when the process is completed the idx dataset returns to the previous one, and the `Studio` instance will display this index. 

To see all logs in the pre-visualization or exportation process set the environment variable `DEBUG_LEVEL`=0.