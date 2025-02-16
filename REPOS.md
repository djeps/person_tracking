[Home](README.md)

# Required repositories

In total, we would need to clone 3 repositories:

- [BoxMOT](https://github.com/mikel-brostrom/boxmot.git)
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics.git)
- [ONNX runtime](https://github.com/microsoft/onnxruntime.git)

Well, technically, we will only need two: the `BoxMOT` and the `ONNX Runtime`. Turns out, that building `Ultralytics YOLO`
from source will introduce more 'package interdependencies challenges' we will need to sort out, while installing it
through `pip` with the right version number is way easier.

We cannot just install everything with pip because we are limited by several factors:

- the HW limits the CUDA version
- the CUDA version limits the OS version
- the OS version limits the package management
- the package management system limits the package versions

> Note: Neither Nvidia nor Ubuntu nor 3rd party vendors deal with maintaining 'legacy' systems so we are
  kind of force to work our way backwards. 

> Note: Everything we do - we do so in our Python virtual environment!

## Cloning the BoxMOT repository

The version of BoxMOT I had identified that satisfies the versions of all our base packages, was with tag release
10.0.52. Later on, I realized while installing `ONNX` and `ONNX Runtime` to the last supported version of the `CUDA`
library for my Jetson Nano (`10.2`) - which was version `1.6.0`, depends on `NumPy 1.23.4` while `BoxMOT 10.0.52` depends
on `NumPy 1.24.4`. At the same time, the first release tag of `BoxMOT` that doesn't depend on `NumPy 1.24.4` is `BoxMOT 10.0.43`
and it depends on `NumPy 1.23.1`.

So what I decided was to checkout the `10.0.43` release and modify the `requirements.txt` file, to that it depends on `NumPy 1.23.4`.
In theory at least, this should work but without amy tests, we would know:

The process is as follows:

```shell
cd ~/repos
git clone https://github.com/mikel-brostrom/boxmot.git
cd ~/repos/boxmot
git checkout tags/v10.0.43 -b release-v10.0.43
git branch
```
> Note: The first `git` command checks-out the release with tag number `10.0.43`, creates a new branch and switches to the new branch.
> Note: The second `git` command confirms we are on the new branch `release-v10.0.43`.

We edit the `requirements.txt` file and update the line where it displays `numpy==1.23.1` to `numpy==1.23.4`.

## Cloning the Ultralytics YOLO repository

Similarly, I have found that version 8.2.81 has all package requirements in-line with our base system packages while
at the same time being compatible with `ONNX` and `ONNX Runtime` - both with version `1.6.0`.

> Note: I've already mentioned that building from source, will cause more challenges to deal with, and although
  under the current circumstances perhaps the safest bet, I've also managed to install it trough `pip`, but you're
  welcome to try.

The process is as follwos:

```shell
cd ~/repos
git clone https://github.com/ultralytics/ultralytics.git
cd ~/repos/ultralytics
git checkout tags/v8.2.81 -b release-v8.2.81
git branch
```

## Cloning the ONNX Runtime repository

The process is as follwos:

```bash
cd ~/repos
git clone --recursive https://github.com/microsoft/onnxruntime.git
cd ~/repos/onnxruntime
git checkout tags/v1.6.0 -b release-v1.6.0

```

We could also checkout with:

```shell
git checkout rel-1.6.0
```

... as there's already a branch at that tag release.

Whichever one we choose to use, we only need to confirm we're on the right branch:

``` shell
git branch
```

[Home](README.md)