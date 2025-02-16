[Home](README.md)

# Installing ONNX

## Checking if ONNX is already present

To check if ONNX is already present in your Python `venv`, execute the following:

```shell
python3 -c "import onnx; print(onnx.__version__)"
```

If that doesn't yield any result, you might want to check if it was installed as a system library:

```shell
ls /usr/local/lib/python3.8/dist-packages/onnx*
```

We also need ProtoBuf, so we need to check if it's already present:

```shell
protoc --version
```

This will either return the version number (minimum required is `3.6.1`) or it will return an error
message `Command 'protoc' not found`.

If the later, you can install `protobuf` with:

```shell
sudo apt install protobuf-compiler libprotobuf-dev
```

To actually install `ONNX`, we need to do so keeping in mind in needs to be at the last supported version
for the the Jetson Nano with `CUDA 10.2`:

```shell
pip3 install onnx==1.6.0
```

Once we do this, we should have `ONNX` installed without any package updates in our venv and we can again
confirm it by executing the `python` command from above.

There are two more packages we need to install which are needed when optimizing the YOLO model with TensorRT.

One of them is `onnxslim` and the other one is `onnxruntime`. The procedure for the 2nd one is a bit more involving,
so I've placed in an entirely separate sectin.

The first one we can install by executing:

```shell
pip3 install onnxslim
```

... which will pull the latest version available (`0.1.48`) and install a couple of extra packages it depends on
(`mpmath` and `sympy`).

[Home](README.md)