[Home](README.md)

# Further performance testing

To make the comparisson fair, I have created a copy of the `temp` folder within itself and replaced the 10 images:

- I took the same image from the parent `temp` folder
- Downscaled it to 640x360
- Copied it's content
- Pasted it into a new image which was 640x640 and
- Filled the rest of the area with black color (effectively marking it as a 'dead' zone) a.k.a. `padding`

Then I ran two consecutive predictions on the entire sets, specifying the size of the set with the  `imgsz` argument:

```shell
cd ~/sandbox/yolo/runs/avg_run
time yolo predict model=../../weights/yolov8n.engine source=../../images/temp/temp imgsz=640 > image_imgsize-engine-predictions.txt
```

The execution time result for the first run (TensortRT model)...

```
real	0m50,145s
user	0m25,648s
sys	    0m8,828s
```

The inference results from the first run (TensorRT model)...

```
...
... 640x640 3 persons, 6 cars, ...
Speed: 55.3ms preprocess, 89.5ms inference, 83.9ms postprocess per image at shape (1, 3, 640, 640)
```

Same experiment but with the `PyTorch` model (`YOLO v8n`):

```shell
time yolo predict model=../../weights/yolov8n.pt source=../../images/temp/temp imgsz=640 > image_imgsize-pt-predictions.txt
```

The execution time result for the second run (YOLO v8n model)...

```
real	0m42,923s
user	0m23,584s
sys	    0m7,088s
```

The inference results from the second run (YOLO v8n model)...

```
...
... 640x640 3 persons, 6 cars, ...
Speed: 6.0ms preprocess, 88.3ms inference, 10.4ms postprocess per image at shape (1, 3, 640, 640)
```

The difference in the overall execution time could always be explained by the extra output that's printed
on the console with the first command. Plus the size of the `TensorRT` model is bigger so the loading takes
longer:

```shell
cd ~/sandbox/yolo/weights
ls -lh yolov8n.engine

-rw-rw-r-- 1 jetson jetson 30M feb 14 14:30 yolov8n.engine
```

```shell
ls -lh yolov8n.pt

-rw------- 1 jetson jetson 6,3M feb 13 07:32 yolov8n.pt
```

We could open up the text files and have a look inside:

```shell
cat image_imgsize-engine-predictions.txt
cat image_imgsize-pt-predictions.txt
```

... but the overall concluion would that inference wise, the performane of both models is comparable, whereas
the `PyTorch` model performs much better in pre- and post- processing so doesn't seem like there's any improvement.

## Lowering the floating point precision

There's one more thing we could try - and that's lowering the floating point precision by half, and generate
a new `*.engine` file (`TensorRT` model) and run the same tests:

```shell
yolo export model=~/sandbox/yolo/weights/yolov8n.pt format=engine half=True
```

The argument `half=True` tells `YOLO` to drop the precision from `FP32` to `FP16` when making the conversion.

So what can we expect from this?

Let's run the first exeperiment (`TensorRT` model):

The execution time result for the first run (TensortRT model)...

```
real	0m56,328s
user	0m25,892s
sys	    0m9,036s
```

The inference results from the first run (TensorRT model)...

```
...
... 640x640 3 persons, 6 cars, ...
Speed: 66.8ms preprocess, 106.6ms inference, 75.3ms postprocess per image at shape (1, 3, 640, 640)
```

```shell
cd ~/sandbox/yolo/runs/avg_run
time yolo predict model=../../weights/yolov8n.engine source=../../images/temp/temp imgsz=640 > image_imgsize-engine-predictions2.txt
```

Let's run the second experiment (`PyTorch/YOLO v8n` model):

```shell
time yolo predict model=../../weights/yolov8n.pt source=../../images/temp/temp imgsz=640 > image_imgsize-pt-predictions2.txt
```

The execution time result for the first run (`PyTorch` model)...

```
real	0m43,497s
user	0m24,072s
sys	    0m6,824s
```

The inference results from the first run (`PyTorch` model)...

```
...
... 640x640 3 persons, 6 cars, ...
Speed: 5.8ms preprocess, 94.8ms inference, 10.4ms postprocess per image at shape (1, 3, 640, 640)
```

Let's have a look at the size of the new TensorRT model with FP16:

```shell
cd ~/sandbox/yolo/weights
ls -lh yolov8n.engine

-rw-rw-r-- 1 jetson jetson 16M feb 14 15:09 yolov8n.engine
```

We could literally make the same argument as before i.e. **little to no performance gain** from converting
the original `PyTorch` model to a `TensorRT` model.

In other words, the `YOLO v8n` model performs equally if not better - without the need for any pre-processing,
padding and such - even if drop the floating point precission from FP32 to FP16 (thus theoretically sacrificing
precision over performance).

It's either that, I have done something terribly wrong in executing and interpreting the results...

## Running predictions/inference on the test subsets from the COCO, KITTI and JAAD datasets

```shell
mkdir ~/sandbox/yolo/runs/run_03
cd ~/sandbox/yolo/runs/run_03
```

```shell
```

## Ad-hoc test on the precision of the `PyTorch` model

> Note: It's interesting to note what happens when using the `yolo predict` command on the images in the `temp` folder
  without actually resizing them!

I executed the command this way:

```shell
time yolo predict model=../../weights/yolov8n.pt source=../../images/temp imgsz=1080,1920
```

The inference speed was increased by a factor of 4-5 but almost all of the objects were correctly
detected (an exception was the `street light` which was identified as a 'flying kite') without increasing
the default confidence level.

[Home](README.md)