# AI_elevator
This is the college project. Combined with three recognizer ( face, speech, hand )

## Introduction
This system is mainly used in places that require personnel control, such as hospitals, residences, and so on. In response to the epidemic occurs , the footprints system stored the data in the database that can be used to know who has entered (also the number of the floor who entry). In addition, it can activated the elevator without touching which is able to stay away from the virus. On the other hand, the high-density entry and exit of the building makes it difficult to control , with the help of the system which can also improve the safety and security .

## How it works
In the beginning, the infrared sensor is used to start the execution of the entire system. After turning on the camera imbedded in the computer, it would check whether the stream matches the image in the database. If not, it will be introduced to the registration website. Using OpenCV to assist us in face and hand recognition . On the other hand , there is part of the speech recognition uses the built-in microphone embedded in the computer to obtain the sound, and uses the Google API to convert the audio into text. After getting  the number, it will send the information to the Arduino via selenium, which starts the elevator operation. 


### Face recognition
The face recognition model mainly uses image-related third-party libraries such as Dlib and Imutils, combined with OpenCV and text files to create a complete model.
Dlib's face detector model is used for face detection. The advantage of this model is that it runs extremely fast on the CPU and can achieve real-time recognition.
Then, use the face correction model of Imutils to correct the previously detected face, and then perform face detection again, and use the Dlib model to detect 68 facial feature points, and compare the corrected face with 68 facial features Click to join the 34-layer Resnet model pre-trained by Dlib, and output 128-dimensional face feature vectors.
Finally, calculate the Euclidean distance between the output face feature vector and the face feature vector already in the database. If the distance is less than 0.4, it will be judged as the same person.

### Hand recognition
It's mainly developed by using Opencv, Keras and Tensorflow. 
At the beginning, the pre-processing of the picture is carried out, the captured picture is converted into a two-dimensional grayscale image, and the size of the picture is adjusted.  In actual recognition, the real-time image is converted into a gray-scale image and Gaussian blur is performed, the background image is updated by cumulative weighting, and the difference between two consecutive frames is taken as the absolute value using cv2.absdiff to achieve the effect of separating the foreground and the background.

Model architecture:

*Convolutional layer -> Convolutional layer -> Pooling layer -> Drop -> Convolutional layer -> Convolutional layer -> Pooling layer -> Fully connected layer -> Drop -> Fully connected layer (Convolution + ReLU, Fully connected + ReLU / Sigmoid, optimizer RSMprop)

![Image](https://github.com/Todoorno/AI_elevator/blob/master/footprint/image/model.PNG)

 
### Speech recognition
Speech recognition uses Google API to convert the audio into text, using different text segmentation modes according to the differences between Chinese and English, and then compares with the modes displayed in regular expressions, so that users can access the positioning numbers.
The translation part is using gTTS and translator in Google API. After the audio is translated into other languages, it will start to broadcast.


### Control sensor and elevator model
The control sensor is using Arduino Leonardo combined with the HC-SR501 human infrared sensor module to simulate the function of the keyboard, and automatically control the computer. It can turn on the system and perform recognition after sensing the human body approach. Open the web page through selenium, and transfer the numbers from the computer to the Arduino Mega2560 module through Arduino ESP8266 chip version via wifi . Through the Arduino Mega2560 module, the received numbers can be controlled by the stepper motor drive module L298N chip to control the movement of the model elevator.

* Flow chart 
![Image](https://github.com/Todoorno/AI_elevator/blob/master/footprint/image/flowchart.PNG)

