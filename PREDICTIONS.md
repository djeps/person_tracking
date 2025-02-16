[Home](README.md)

# Taking the optimized model for a 'test drive'

To start making prdictions using the optimized model, let's first create a folder where we will store
the results:

```shell
cd ~/sandbox/yolo/runs
mkdir run_02
cd run_02
```

Let us now make the first prediction with the optimized model and evaluate the boost:

```shell
time yolo predict model=../../weights/yolov8n.engine source=../../images/image01.jpg > image01_predictions.txt
time yolo predict model=../../weights/yolov8n.engine source=../../images/image02.jpg > image02_predictions.txt
time yolo predict model=../../weights/yolov8n.engine source=../../images/image03.jpg > image03_predictions.txt
time yolo predict model=../../weights/yolov8n.engine source=../../images/image04.jpg > image04_predictions.txt
time yolo predict model=../../weights/yolov8n.engine source=../../images/image05.jpg > image05_predictions.txt
```

The execution time result...

```
real	0m44,655s
user	0m24,712s
sys	    0m8,372s
```

The inference or prediction results...

```shell
cat image01_predictions.txt
```

```
...
image 1/1 /home/jetson/sandbox/yolo/run_02/../images/image01.jpg: 640x640 3 persons, 4 cars, 1 truck, 199.4ms
Speed: 413.1ms preprocess, 199.4ms inference, 342.6ms postprocess per image at shape (1, 3, 640, 640)
```

Disapointing to say the least, because this certainly isn't any performance boost!

But after making some further research, turns out there may be some logical explanation behind.

There's something that's referred a *warmup period*... a situation where 'the first few inference calls can be
slower as the model initializes'.

There's also what's called *memory transfer overhead*... where 'frequent data transfers between CPU and GPU memory'
could impair the performance benefits of TensorRT.

The suggested approach is to 'minimize data transfers between CPU and GPU' and 'keep as much of the pipeline on the
GPU as possible' or 'running multiple inferences and measure the average time after the initial calls'.

In other words, load the model once and make predictions.

First I tried executing the same command a few times one after the other:

```shell
time yolo predict model=../../weights/yolov8n.engine source=../../images/image01.jpg > image01_predictions.txt
```

... and already noticed noticeable improvements but still not near the performance results when running the same
command with `model=../weights/yolov8n.pt`. Furthermore, we are still reloading the model each time we run the
command.

Therefore, as an experiment, I have created a `temp` folder inside my `~/sandbox/yolo/images` folder and copied the
same image 10 time and ran a `yolo predict` command on the entire folder (while monitoring what's happening on the
Jetson Nano with the `jtop` utility):

```shell
mkdir ~/sandbox/yolo/images/temp
cp ~/sandbox/yolo/images/image01.jpg ~/sandbox/yolo/images/temp/image01-01.jpg
cp ~/sandbox/yolo/images/image01.jpg ~/sandbox/yolo/images/temp/image01-02.jpg
cp ~/sandbox/yolo/images/image01.jpg ~/sandbox/yolo/images/temp/image01-03.jpg
...
cp ~/sandbox/yolo/images/image01.jpg ~/sandbox/yolo/images/temp/image01-10.jpg
```

```shell
mkdir ~/sandbox/yolo/runs/avg_run
cd ~/sandbox/yolo/runs/avg_run
time yolo predict model=../../weights/yolov8n.engine source=../../images/temp > image_engine-predictions.txt
```

This way - however pointless to do any predictions on the same image - at least I load the model only once!

The execution time result...

```
real	0m55,404s
user	0m26,720s
sys	    0m8,740s
```

The inference or prediction results...

```
...
... 640x640 3 persons, 4 cars, 1 truck, ...
Speed: 69.0ms preprocess, 83.4ms inference, 56.4ms postprocess per image at shape (1, 3, 640, 640)
```

Let's repeat the same, but this time using the YOLO v8n model instead:

```shell
time yolo predict model=../../weights/yolov8n.pt source=../../images/temp > image_pt-predictions.txt
```

The execution time result...

```
real	0m45,086s
user	0m25,888s
sys	    0m7,308s
```

The inference or prediction results...

```
...
... 384x640 3 persons, 4 cars, 1 truck, ...
Speed: 13.3ms preprocess, 63.7ms inference, 7.6ms postprocess per image at shape (1, 3, 384, 640)
```

Conclusion? Did we get any performance boost by using the 'optimized' TensorRT model? It doesn't
seem that way, but then when you open up the `image_engine-predictions.txt` and `image_pt-predictions.txt`
files, you will quickly notice that the original image was differently resized between the two
tests... Suggesting that YOLO might be internally handling the two models differently or...

... or TensorRT expects the input image to be of a certain size (640x640) and doesn't handle well the aspect ratio.

In other words, any direct comparisson at this stage would be unfair until we run the tests under
the exact same conditions.

> Note: You can use the [Neutron Application](https://netron.app/) to view different models, e.g. the `PyTorch (*.pt)`
  and `ONNX` models bud sadly not the `TensorRT` one (probably because it's not open source?). Nevertheless, still a
  very useful tool.

[Home](README.md)