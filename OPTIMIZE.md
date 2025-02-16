[Home](README.md)

# Optimizing the YOLO model with TensorRT

To optimize the YOLO v8n model with TensorRT, we need to execute the following command - on the device
itself:

```shell
yolo export model=~/sandbox/yolo/weights/yolov8n.pt format=engine
```

Executing it for the first time will most likely fail and throw the following error message:

```
ImportError: /usr/lib/aarch64-linux-gnu/libGLdispatch.so.0: cannot allocate memory in static TLS block
```

To solve this, one of the things we could try is to add the following line to the `~/.bashrc` file:

```shell
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libGLdispatch.so.0:$LD_PRELOAD >> ~/.bashrc
```

... and reload the `~/.bashrc`:

```shell
source ~/.bashrc
```

[Home](README.md)