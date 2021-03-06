## Setup:

0. Initialize all the dependency repos, run `git submodule update --init --recursive`
- `git submodule update --recursive` if its **not** the first time and you need to update repos to the latest changes.

1. Obtain the model. In this project's root directory, run: 
```
wget http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
tar -xzvf ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
```
- Or find other pre-trained models at
 `https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md`
 `https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md`

2. Make sure v4l2 drivers are installed on the RPi. Check camera device works: `v4l2-ctl --device /dev/video0 --set-fmt-video=width=1280,height=720,pixelformat=MJPG --stream-mmap --stream-to=frame.jpg --stream-count=1`
- For troubleshooting/more info run `v4l2-ctl --device /dev/video0 --list-formats-ext`

3. Convert `*_label_map.pbtxt` file to Python dictionary. Load `string_int_label_map.proto` file and compile it using `protoc`:
- `cd detector_receiver/models/research && protoc object_detection/protos/*.proto --python_out=.`

### Quickstart

#### Raspberry Pi (Camera sender) 
1. `cd camera_sender`
2. `pipenv install`
2. `pipenv run python pi_camera_sender.py`

#### Edge Computer (Dectector receiver)
1. `cd detector_receiver`
3. `pipenv install`
2. `pipenv run python pest_detector.py`