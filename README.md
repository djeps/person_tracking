# Person detection and tracking with YOLO on a Jetson Nano board

To complete the task of deploying YOLO and BoxMOT on a Jetson Nano, please follow each topic
in the order they're presented:

- [Introduction](INTRO.md)
- [Downloading datasets](DATASETS.md)
- [Setting up the Jetson Nano with Ubuntu 20.4](JETSON.md)
- [Creating a Python virtual environment](VENV.md)
- [Cloning the neccessary repositories](REPOS.md)
- [Building BoxMOT](BOXMOT.md)
- [Installing Ultralytics YOLO](ULTRALYTICS.md)
- [Installing ONNX](ONNX.md)
- [Building ONNX Runtime](ONNXRUNTIME.md)
- [Optimizing the YOLO model with TensorRT](OPTIMIZE.md)
- [Taking the optimized model for a 'test drive'](PREDICTIONS.md)
- [Further performance testing](PTEST.md)
- [Running predictions on the KITTI and JAAD datasets (w/o model fine tuning)](FPTEST.md)
- [Person detection and tracking](DETECTNTRACK.md)

# Conclusion

My personal experience from all of these experiments showed me that there's little to no
performance improvement from converting the `YOLO v8n (PyTorch)` to a `TensorRT` one.

In fact, precision put aside (because it's pretty much the same in both cases) you're better
off using the `YOLO v8n (nano)` model directly on the Jetson Nano as it's slightly better
in the inference speed but much better in the pre- and post- processing phase.

Unless I've conducting my tests completely wrong...

There's one experiment that's referenced in the last couple of sections which seems to
suggest that if we take the largest of the `YOLO v8` models and optimize it with TensortRT,
there are significant performance improvements but that entire experiment wasn't performed
on a resource 'constrained' target such as the Jetson Nano where just using the smallest
of v8 family models makes more sense.
