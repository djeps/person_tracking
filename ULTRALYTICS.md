[Home](README.md)

# Installing Ultralytics YOLO

As I've already mentioned in th previous sections, we are not going to be building from source,
as it creates more interdependency challenges.

But if you're willing to try and see for yourself, the procedure is as follows:

```shell
cd ~/repos/ultralytics
python3 -m venv --system-site-packages ~/venv/ultralytics-venv
pip install -v .
```
For some reason, we can't be building in 'editable mode` due to the `setup.py` missing, hence we omit
the `-e` flag.

## Installing YOLO as a package

```shell
pip3 install ultralytics==8.2.81
```

This installs the `opencv-python` package as well (`4.11.0.86`) but for similar reasons as with
`BoxMOT`, we can safely remove it and rely on the base package which already satisfies the requirement
for this version of `Ultralytics` i.e. `opencv-python>=4.6.0`.

```shell
pip3 uninstall opencv-python
```

... and check once more if all important packages are unchanged with:

```shell
~/scripts/check_packages.sh
```

If everything is OK, we can check the YOLO version by executing:

```shell
yolo version
```

... which should indeed print out `8.2.81`.

## Downloading the YOLO v8n model

We will work with YOLO v8, specifically the 'nano' version of it as it's most suitable for
running on smaller 'embedded' devices such as the Jetson Nano.

If you want, you could download the `sandbox` folder and copy it over to the `home` folder of
the Jetson Nano, and in it you will already find the so called weights file for the specific
version of YOLO:

```shell
ls ~/sandbox/yolo/weights
```

.. or you can download it yourself:

```shell
mkdir -p ~/sandbox/yolo/weights
cd ~/sandbox/yolo/weights
wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt
ls -l yolov8n.pt
```

> Note: I will assume that you have downloaded the `sandbox` folder and copied it into the `home` folder.

## Running a few sample predictions

When you want to make some predictions with YOLO from the CLI (*Command Line Interface*) and you want to
specifically set the minimum confidence level, you can do so by executing:

```shell
yolo predict model=yolov8n.pt source=image01.jpg conf=0.50
```

> Note: make sure you're inside the `~/sandbox/yolo` folder (`cd ~/sandbox/yolo`)

When you specify yor own confidence level and increase it, you're effectively lowering the number of false
positives at the expense of sensitivity.

But we are not going to do that. Instead, we are going to run predictions without specifying any extra
parameters, on some sample images from
[the JAAD dataset](https://www.kaggle.com/datasets/charvik/jaad-frames-dataset-10-v1-yolo-format):

```shell
cd ~/sandbox/yolo/
mkdir runs
cd runs
mkdir run_01
cd run_01
time yolo predict model=../weights/yolov8n.pt source=../images/image01.jpg > image01_predictions.txt
time yolo predict model=../weights/yolov8n.pt source=../images/image02.jpg > image02_predictions.txt
time yolo predict model=../weights/yolov8n.pt source=../images/image03.jpg > image03_predictions.txt
time yolo predict model=../weights/yolov8n.pt source=../images/image04.jpg > image04_predictions.txt
time yolo predict model=../weights/yolov8n.pt source=../images/image05.jpg > image05_predictions.txt
```

> Note: YOLO will display some inference performance metrics but we specifically want to `time` the overall
  execution of the `yolo predict` command and pipe everythong to a file for each sample prediction.

The results of the execution time for the first command are:

```shell
real	0m42,707s
user	0m23,092s
sys	    0m6,928s
```

The inference or prediction results...

```shell
cat image01_predictions.txt
```

```shell
...
image 1/1 /home/jetson/sandbox/yolo/run_01/../images/image01.jpg: 384x640 3 persons, 4 cars, 1 truck, 72.0ms
Speed: 69.0ms preprocess, 72.0ms inference, 151.3ms postprocess per image at shape (1, 3, 384, 640)
```

We will take this as the comparison reference later on, once we are able to optimize the model for executing
on the Jetson Nano with TensorRT. For now we will put them aside and forget about them.

[Home](README.md)