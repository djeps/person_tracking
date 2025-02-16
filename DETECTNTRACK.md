[Home](README.md)

# Person detection and tracking

## Detection

### Pre-recorded video stream

https://www.pexels.com/search/videos/people%20walking/

```shell
cd ~/sandbox/yolo/runs
mkdir run_06
cd run_06
```

#### `YOLO v8n (PyTorch)` model, `vide04.mp4`

```shell
time yolo detect predict model=../../weights/yolov8n.pt source=../../videos/video04.mp4 classes=0 save=True
```

Execution time:

```
real	5m43,593s
user	5m32,532s
sys	    0m13,884s
```

#### `TensorRT` model, `video04.mp4`

```shell
time yolo detect predict model=../../weights/yolov8n.engine source=../../videos/video04.mp4 classes=0 save=True
```

Execution time:

```
real	6m40,181s
user	5m21,040s
sys	    0m43,280s
```

```shell
cd ~/sandbox/yolo/runs
mkdir run_07
cd run_07
```

#### `YOLO v8n (PyTorch)` model, `video06.mp4`

```shell
time yolo detect predict model=../../weights/yolov8n.pt source=../../videos/video06.mp4 classes=0 save=True > video_pt-people_detect.txt
```

Execution time:

```
real	9m43,527s
user	9m12,220s
sys	    0m26,036s
```

#### `TensorRT` model, `video06.mp4`
```shell
time yolo detect predict model=../../weights/yolov8n.engine source=../../videos/video06.mp4 classes=0 save=True > video_trt-people_detect.txt
```

Execution time:

```
real	10m7,546s
user	9m1,944s
sys	    0m31,664s
```

### Live video stream

## Tracking

### Tracking with BoxMOT

#### Attemting to track with BoxMOT

If we attempt to use the BoxMOT's sample tracking script on a live camera feed:

```shell
cd ~/repos/boxmot
python3 examples/track.py --source 0 --yolo-model ../../sandbox/yolo/weights/yolov8n.pt --tracking-method bytetrack --classes 0 
```

... on its first run, it will throw an error message:

```
libgomp-d22c30c5.so.1.0.0: cannot allocate memory in static TLS block
```

A quick search on the Internet will suggest that it's a known issue on the Jetson Nano in the sense that ibrary cannot
allocate memory in the static *Thread Local Storage* (TLS) block and that the first fix we should be trying is to
pre-load the library (we already did something like it):

```shell
echo "export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1:$LD_PRELOAD" >> ~/.bashrc
```

So the end of the the `~/.bashrc` file should now look like this:

```shell
# Preloading libraries
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libGLdispatch.so.0:$LD_PRELOAD
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1:$LD_PRELOAD
```

Then we simply need to log out and log back in again or reload the `~/.bashrc` file in our current session:

```shell
source ~/.bashrc
```

Sadly, this will not be enough - we will still experience the error.

One of the very first important notes taken when going over [Qengineering's repository](https://github.com/Qengineering/Jetson-Nano-Ubuntu-20-image/tree/main)
related specifically to this type of an error, is that the order in which we load the modules in our Python scripts - matter,
i.e. we need to load the OpenCV module first.

So, we made a couple of changes to the `~/repos/boxmot/examples/track.py` script, i.e. we put the `import cv2` at
the very top and replaced `from boxmot import TRACKERS` with `from boxmot import BYTETracker` and introduced another
error: `NameError: name `TRACKERS` is not defined`. We need to prune the script and make all of the neccessary changes
before attempting to run it again.

I made a few more modifications to the original `track.py` script from `BoxMOT` just to get it to start, but after a
few successful detections, it crashes, throwing exceptions because it can't see the video stream no longer. At this
point, I wasn't sure if it's something related to the USB type web camera I am using, or further code pruning is needed.

Therefore, I've opted for the quicker approach - write a simple script.

> Note: Actually, the `~/sandbox/yolo/tracker/tracker.py` script is 95% AI generated!

But if we run it:

```shell
cd ~/sandbox/yolo/tracker
python3 tracker.py
```

... we will see it in action and how it detects and that tracks objects of `person` class!

### Tracking with YOLO and ByteTrack

Turns out, YOLO comes pre-shipped with tracking capabilities - even more importantly - with the
`ByteTrack` algorithm which seems to be the suggested on when tracking on a resource constrained HW
such as the Jetson Nano.

To execute the tracking feature on two sample videos:

```shell
time yolo track model=../../weights/yolov8n.pt source=../../videos/video04.mp4 tracker="bytetrack.yaml" save=True > video04_pt-people_track.txt
```

Execution time:

```
real	4m44,620s
user	4m20,912s
sys	    0m15,760s
```

```shell
time yolo track model=../../weights/yolov8n.pt source=../../videos/video06.mp4 tracker="bytetrack.yaml" save=True > video06_pt-people_track.txt
```

Execution time:

```
real	7m52,661s
user	7m23,708s
sys	    0m30,792s
```

If you look at the execution time alone, and compare it with the previous experiments (detection only!) for the
same selected videos, you would notice there's a visible improvement.

This shows that indeed - tracking is computationally a cheaper alternative than detecting 100% of the time, because
what we essentially do is detect (once!) and track an object until it goes out of the frame.

Of course, the accuracy drops but *how much* and *whether it's acceptable or not* - that's a topic for
a different discussion. 

To execute the tracking feature on a live/camera video feed:

```shell
yolo track=../../weights/yolov8n.pt source=0 classes=0 tracker="bytetrack.yaml" show=True save=False conf=0.35
```

> Note: Passing in the argument `save=False` explicitly instructs YOLO not to save the output video with the predictions
  it made while showing it live with `show=True`.

[Home](README.md)
