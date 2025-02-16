#!/bin/bash

OPENCV_VER=$(python3 -c "import cv2 as ocv; print(ocv.__version__)" | grep 4.8.0)
echo "OpenCV=${OPENCV_VER}"

TENSORFLOW_VER=$(python3 -c "import tensorflow as tf; print(tf.__version__)" | grep 2.4.1)
echo "TensorFlow=${TENSORFLOW_VER}"

TORCH_VER=$(python3 -c "import torch as t; print(t.__version__)" | grep 1.13.0)
echo "Torch=${TORCH_VER}"

TORCHVISION_VER=$(python3 -c "import torchvision as tv; print(tv.__version__)" | grep 0.14.0)
echo "TorchVision=${TORCHVISION_VER}"

TENSORRT_VER=$(python3 -c "import tensorrt as trt; print(trt.__version__)" | grep 8.0.1.6)
echo "TensorRT=${TENSORRT_VER}"