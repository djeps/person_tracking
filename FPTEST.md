[Home](README.md)

# Running predictions/inference on the test subsets from the KITTI and JAAD datasets

For this last experiment, we would run predictions against the KITTI and JADD datasets, specifically the
test subset.

Since we are not going to be making any finetuning, this is quite acceptable. In fact, it makes no
difference what so ever!

But instead of predicting all classes, we're just going to take the person class and run the predicitons
two times for each dataset: 1-with the `YOLO v8n` (`PyTorch`) model and 2-once more with the downsized (`FP16`)
`TensorRT` model.

## JAAD test subset

The JAAD test subset consists of: 525 images.

First we need to 'prepare' our environment:

```shell
cd ~/sandbox/yolo/runs/
mkdir run_03
cd run_03
```

Then make the predictions on the subset using the two different models.

### YOLO v8n (PyTorch) model

Execution time results:

```shell
time yolo predict model=../../weights/yolov8n.pt source=../../datasets/jaad/train/ classes=0 > jaad_pt-predictions.txt
```

```
real	4m41,247s
user	3m29,004s
sys	    0m20,492s
```

Inference performance results:

```shell
cat jaad_pt-predictions.txt
```

```
...
Speed: 13.5ms preprocess, 57.1ms inference, 7.8ms postprocess per image at shape (1, 3, 384, 640)
...
```

### TensorRT (FP16) model

Execution time results:

```shell
time yolo predict model=../../weights/yolov8n.engine source=../../datasets/jaad/train/ classes=0 > jaad_trt-predictions.txt
```

```
real	4m54,285s
user	2m58,200s
sys	    0m18,820s
```

Inference performance results:

```shell
cat jaad_trt-predictions.txt
```

```
...
Speed: 15.0ms preprocess, 55.9ms inference, 10.2ms postprocess per image at shape (1, 3, 640, 640)
...
```

## KITTI test subset

The JAAD test subset consists of: 7518 images.

First we need to 'prepare' our environment:

```shell
cd ~/sandbox/yolo/runs
mkdir run_04
cd run_04
```

Then make the predictions on the subset using the two different models.

### YOLO v8n (PyTorch) model

Execution time results:

```shell
time yolo predict model=../../weights/yolov8n.pt source=../../datasets/kitti/test/ classes=0 > kitti_pt-predictions.txt
```

```
real	20m52,547s
user	17m0,404s
sys	    1m20,316s
```

Inference performance results:

```
...
Speed: 7.8ms preprocess, 41.5ms inference, 5.1ms postprocess per image at shape (1, 3, 224, 640)
...
```

### TensorRT (FP16) model

Execution time results:

```shell
time yolo predict model=../../weights/yolov8n.engine source=../../datasets/kitti/test/ classes=0 > kitti_trt-predictions.txt
```

```
real	23m15,804s
user	14m14,904s
sys	    1m2,900s
```

Inference performance results:

```
...
Speed: 10.6ms preprocess, 56.0ms inference, 7.8ms postprocess per image at shape (1, 3, 640, 640)
...
```

## Results

I would say the results are indicative (I cautiously avoid using the word *conclusive*) that there's little to no
performance improvement of optimizing the `YOLO v8n` model (or any *nano* model for that matter I would assume)
to a TensorRT.

As far as accuracy goes, I did a quick diff on the `*.txt` files and I found out that in some cases the optimized
model detects more objects of the 'person' class - and vice versa, yet in some of those case, it sometimes turns out
those predictions are false positives or hallucinations! Of course, if we scale-up the confidence level, we might get
results which are more on par.

Last final test I would like to perform, is the calculation of the `mAP` metric (*mean Average Precision*) for the two models:

```shell
cd ~/sandbox/yolo/runs
mkdir run_05
cd run_05
```

### YOLO v8n (PyTorch) model

```shell
yolo detect val model=../../weights/yolov8n.pt data=../../datasets/coco/coco128.yaml iou=0.5 imgsz=640 name=yolov8n-pt > yolov8n-pt.txt
cat yolov8n-pt.txt
```

```
 Class     Images  Instances      Box(P          R      mAP50  mAP50-95)
   all        128        929      0.658      0.543      0.616      0.443
person         61        254       0.82      0.681      0.776      0.532
...
```

### TensorRT (FP16) model

```shell
yolo detect val model=../../weights/yolov8n.engine data=../../datasets/coco/coco128.yaml iou=0.5 imgsz=640 name=yolov8n-trt > yolov8n-trt.txt
cat yolov8n-trt.txt
```

```
 Class     Images  Instances      Box(P          R      mAP50  mAP50-95)
   all        128        929      0.679      0.542      0.618      0.449
person         61        254      0.829      0.666      0.771      0.534
...
```

> Note: the `mAP50` uses a `50% IoU` (that's *Intersection over Union* and not *I owe you* :)) threshold for considering
  a detection as correct.

> Conclusion: Practically no difference between the two models. Slightly better overall detection for the `TensorRT` model
(`@FP16!`) but on the other hand, slightly better person class detection for the `YOLOv8n` (`PyTorch`) model!

# Comments

There are some online tutorials ([How To Speed Up YOLOv8 2x using TensorRT](https://www.youtube.com/watch?v=-qPGdGoh9Wg))
that imply that by additionally installing the `tensorrt_lean` and `tensorrt_dispatch` packages on top of the base package
`tensorrt` will additionally improve performance.

As plausible this might be, I cannot test it on my setup because there are no suitable version candidates for `TensorRT`
version `8.0.1.6`. If I want to go that road, I have to yet spend time on building them from source!

Furthermore, 1-the entire experiment the author makes, doesn't seem as if it's targetting 'resource constrained devices'
such as the Jetson Nano and 2-he's optimizing the largest `YOLO v8x` model so no wonder he's getting a performance boost.

Finally, his mAP50 scores are `0.827` and `0.87` for the *overall* i.e. *person* score respectively for the `YOLO v8x` model,
while `0.818` and `0.862` for the *overall* i.e. *person* score respectively for the optimized `TensorRT` model.

This almost `10%` improved `mAP` score for e.g. the *person* class is due to the fact his using the largest of the `YOLO v8`
models, but frankly not that tempting so that we try and follow the same route.

What is tempting though, is the impovement in the *inference speed*: he's achieving an inference speed of almost `x2` less
than in our experiments (at roughly `25ms`!).

[Home](README.md)
