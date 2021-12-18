# AI_elevator
This is the last year project. Combined with three recognizer ( face, speech and hand )

## How it works
The system is triggered by the infrared sensor. 
here is the flow chart : 
![Image](https://github.com/Todoorno/AI_elevator/blob/master/footprint/image/flowchart.PNG)

### Face recognition
The face recognition mainly created by Dlib ,Imutils and OpenCV .
Dlib is to detect 68 facial feature points.
Calculate the Euclidean distance between the output vector and the feature vector in the database. If the distance is less than 0.4, it will be judged as the same person.

### Hand recognition
It's mainly developed by using Opencv, Keras and Tensorflow. 
For training data : the image is converted into a two-dimensional grayscale image (size of the picture is already revised) . 
The real-time image is converted into a gray-scale image and also using the Gaussian blur to denoising , the background image is updated by cumulative weighting, and the difference between two consecutive frames is taken as the absolute value using cv2.absdiff to separate the foreground and the background.

Model architecture:

*Convolutional layer -> Convolutional layer -> Pooling layer -> Drop -> Convolutional layer -> Convolutional layer -> Pooling layer -> Fully connected layer -> Drop -> Fully connected layer (Convolution + ReLU, Fully connected + ReLU / Sigmoid, optimizer RSMprop)

![Image](https://github.com/Todoorno/AI_elevator/blob/master/footprint/image/model.PNG)

 
### Speech recognition
Speech recognition uses Google API to convert the audio into text.
The translation part is using gTTS and translator in Google API. After the audio is translated into other languages, it will start to broadcast.


### Control sensor and elevator model
The control sensor is using Arduino Leonardo combined with the HC-SR501 human infrared sensor module to simulate the function of the keyboard, and automatically control the computer. 

