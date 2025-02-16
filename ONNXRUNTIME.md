[Home](README.md)

# Building ONNX Runtime

> Spoiler alert! Building the ONNX Runtime failed mid-way through the process and jsut got tired
  of trying and fixing one error after another just to get it started. I left the description of the
  the process I took, I eventually - I ended up pip installing it, and exeperienced some unexpected
  behavior.

As part of the build process of `onnxruntime`, the `build.sh` script performs PEP8 conformance checks
of the Python scripts. This is the reason why we need the `flake8` package... so the build system can
validate the internal Python scripts.

To install it, we need to execute:

```shell
pip3 install flake8
```

We could pass an argument to the `build.sh` script to skip any tests, but I found that merely passing the
`--skip-tests flag`, is not enough so we have to edit the `.flake8` file (or create it should it not exist)
and add a couple of lines:

```shell
cd cd ~/repos/onnxruntime/
echo "ignore = E,W,F" >> .flake8
echo "exclude = .git,__pycache__,.venv,.eggs,*.egg" >> .flake8
```

> Note: I am not so sure the second line is needed needed or if it makes any difference. The first one though,
  is clear: ignore all errors and warnings! Probably not the best idea to skip the tests, but I'm cloning from
  an official repo and trust the peopler who have build the software have tested and validated their software.

> Note: In principle, we shouldn't be dealing with this at all

> Note: If the file doesn't already exist, edit and add `[flake8]` at the top before the two lines we just added.

`TensorRT Myelin` is *an important component of NVIDIA's TensorRT optimization toolkit for deep learning inference*
and it's used as *a graph compilation and execution backend integrated into TensorRT*.

However, when building the `onnxruntime` from source, the `build.sh` script reports that this library isn't found.
One alternative would be to build it from source, but we've already done too much of it, so we could disable it
from the build process as I believe (hope!) it won't make any difference for what we want to use `TensorRT`, which
is to optimize the YOLO model for peformance on the Jetson Nano. If it doesn't work for some reason, we could
always try and go that route.

To disable it, we have to first identify what `CMakeLists.txt` file has any reference of the environment variable
`TENSORRT_LIBRARY_MYELIN` the build process complains about:

```shell
find . -name CMakeLists.txt | xargs grep TENSORRT_LIBRARY_MYELIN 
```

This would list all the files where there's a reference to `TENSORRT_LIBRARY_MYELIN` in them:

```
./cmake/external/onnx-tensorrt/CMakeLists.txt:  find_library(TENSORRT_LIBRARY_MYELIN myelin64_1
./cmake/external/onnx-tensorrt/CMakeLists.txt:  find_library(TENSORRT_LIBRARY_MYELIN myelin
./cmake/external/onnx-tensorrt/CMakeLists.txt:set(TENSORRT_LIBRARY ${TENSORRT_LIBRARY_INFER} ${TENSORRT_LIBRARY_INFER_PLUGIN} ${TENSORRT_LIBRARY_MYELIN})
```

Next we have to edit the file:

```shell
nano ./cmake/external/onnx-tensorrt/CMakeLists.txt
```

... search for all references of `TENSORRT_LIBRARY_MYELIN` and comment them out. Luckily, the are all one after
the other, so the entire block where the environment variable appears, should look something like this:

```shell
if(WIN32)
  find_library(TENSORRT_LIBRARY_MYELIN myelin64_1
    HINTS  ${TENSORRT_ROOT} ${TENSORRT_BUILD} ${CUDA_TOOLKIT_ROOT_DIR}
    PATH_SUFFIXES lib lib64 lib/x64)
#else()
#  find_library(TENSORRT_LIBRARY_MYELIN myelin
#    HINTS  ${TENSORRT_ROOT} ${TENSORRT_BUILD} ${CUDA_TOOLKIT_ROOT_DIR}
#    PATH_SUFFIXES lib lib64 lib/x64)
endif()
#set(TENSORRT_LIBRARY ${TENSORRT_LIBRARY_INFER} ${TENSORRT_LIBRARY_INFER_PLUGIN} ${TENSORRT_LIBRARY_MYELIN})
set(TENSORRT_LIBRARY ${TENSORRT_LIBRARY_INFER} ${TENSORRT_LIBRARY_INFER_PLUGIN})
```

> Note: Since the project is versioned with `git`, we could just as well delete all commented lines.

After this, we can start the build process by executing:

```shell
./build.sh --config Release \
    --use_cuda \
    --cuda_home /usr/local/cuda \
    --cudnn_home /usr/lib/aarch64-linux-gnu \
    --use_tensorrt \
    --tensorrt_home /usr/lib/aarch64-linux-gnu \
    --build_shared_lib \
    --parallel 1 \
    --enable_pybind \
    --build_wheel \
    --cmake_extra_defines CMAKE_CUDA_ARCHITECTURES=53 \
    --skip_tests
```

Be patient. It takes some time to build the software, hopefully without any errors!

If all goes well, (and it didn't... see the note at the begining of this section), you should have a wheel
file built in:

```shell
ls build/Linux/Release/dist
```

Go ahead and install the weel file with `pip`:

```shell
pip3 build/Linux/Release/dist/onnxruntime-1.6.0-cp38-cp38-linux_aarch64.whl
pip3 show onnxruntime
```

... and verify the version and check if it's correctly installed:

```shell
python3 -c "import onnxruntime; print(onnxruntime.__version__)"
```

# Installing ONNX Runtime with `pip`

The only pre-built wheel I found that was (reportedly) built for the Jetson Nano with `CUDA 10.2` and `Python 3.8`,
was version `1.17.0`. According to my previous research, this shouldn't work.

I got two contradictory approaches, but since I was out of ideas, I decided to give the wheel a try.

First yopu need to download it:

```shell
wget https://nvidia.box.com/shared/static/zostg6agm00fb6t5uisw51qi6kpcuwzd.whl -O onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl
```

Then go ahead and install it by executing:

```shell
pip3 install onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl
```

Finally, remove the wheel file as there's no point to take up space on your SD card:

```shell
rm onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl
```

After the install, you will see the following errors:

```
ERROR: ultralytics 8.2.81 requires opencv-python>=4.6.0, which is not installed.
ERROR: boxmot 10.0.42 requires opencv-python>=4.6.0, which is not installed.
ERROR: boxmot 10.0.42 has requirement numpy==1.23.4, but you'll have numpy 1.24.4 which is incompatible.
ERROR: tensorflow 2.4.1 has requirement numpy~=1.19.2, but you'll have numpy 1.24.4 which is incompatible.
ERROR: tensorflow 2.4.1 has requirement wheel~=0.35, but you'll have wheel 0.34.2 which is incompatible.
```

The last two errors we have already explained why it's safe to ignore them. Please refere to one of the previous
sections. The same applies to the first two.

So the only one that deserves our attention is the third one. Again was the NumPy package updated and we
would like to avoid that and put it back to the version we want to keep:

```shell
pip3 uninstall numpy
pip3 install numpy==1.23.4
```

> Note: I finally figured out that I could prevent other packages from being upgraded when installing one with `pip`.
  The trick is to use the `--no-deps` argument. So if we apply this to the `onnxruntime` package, it would be something
  like this: `pip3 install --no-deps onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl`

Again, we will have some error messages - actually pretty much the same as above, with the exception of the 3rd one, which
now is:

```
ERROR: onnxruntime-gpu 1.17.0 has requirement numpy>=1.24.4, but you'll have numpy 1.23.4 which is incompatible.
```

There's nothing we could do but ignore it and hope for the best.

If we now try the python command to check if the install was successful:

```shell
python3 -c "import onnxruntime; print(onnxruntime.__version__)"
```

... we would be greeted with yet another error message:

```
ImportError: /usr/lib/aarch64-linux-gnu/libstdc++.so.6: version `GLIBCXX_3.4.29` not found'
```

If we execute the following command:

```shell
strings /usr/lib/aarch64-linux-gnu/libstdc++.so.6 | grep GLIBCXX
```

... we would indeed see that the the string `GLIBCXX_3.4.29` doesn't appear to exist.

## Updating `g++`

What we need to do next is update the g++ version to something more recent:

```shell
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt upgrade
sudo apt install g++-11
```

After this step, we could setup all the different g++ alternatives like so:

```shell
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 110
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 90
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 80
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 70
```

Then we can switch between the different g++ versions - one to be used by default - by simply executing:

```shell
sudo update-alternatives --config g++
```

Then if we simply execute the above `string` command, we will see the string `GLIBCXX_3.4.29` (and more!),
thus confirming our `libstdc++.so.6` library has been updated.

Re-executing the python command from above, will indeed that we now have version `1.17.0` of the `onnxruntime-`gpu
package installed on our system.

[Home](README.md)
