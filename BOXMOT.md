[Home](README.md)

# Building BoxMOT

Through some pip listings and looking at the package interdependency, I made the following changes to the `requirements.txt` file:

- (new) `filelock>=3.12.2`
- (updated) `gdown>=5.1.0`
- (new) `ftfy>=6.1.1`
- (new) `scipy>=1.5.0`
- (updated) `tensorboard==2.6.0`
- (disabled) `# torch>=1.7.0`
- (disabled) `# torchvision>=0.8.1`

> Note: Strangely enough, the NumPy package requirement was already at the version I wanted to update it to: `numpy==1.23.4`.

To build the BoxMOT project from source:

```shell
cd ~/repos/boxmot
pip install -v -e .
```

First of all, this will inevitably update some of the base or system packages, but as long as it works, we don't care.
And it won't break anything as long as we remain in the Python `venv`.

The build process should finish up, with only two errors:

```
ERROR: tensorflow 2.4.1 has requirement numpy~=1.19.2, but you'll have numpy 1.23.4 which is incompatible.
ERROR: tensorflow 2.4.1 has requirement wheel~=0.35, but you'll have wheel 0.34.2 which is incompatible.
```

The second one we can address by updating the `wheel` package by executing: `pip3 install wheel==0.35` and re-build.
But we are not going to that (for now at least and if we absolutely need it), because both errors are related to the
specific version of `TensorFlow` we inherited from our base system which we don't want to touch.

Furthermore, neither `BoxMOT` nor `Ultralytics YOLO` are built on top of `TensorFlow` but on top of `PyTorch`.
Hence, we are not going to do anything for now and just leave it be!

What we are going to do is remove the installed OpenCV version, which after the build is finished, we can lsit with:

```shell
pip3 show opencv-python
```

... and see it's at version `4.11.0.86`.

Now, as the requirement inside the `requirements.txt` file was: `opencv-python>=4.6.0` and we already have this installed
from source from the base system at version `4.6.0` and not as a `pip` package, we can remove it:

```shell
pip3 uninstall opencv-python
```

... and check once more if all important packages are unchanged with:

```shell
~/scripts/check_packages.sh
```

[Home](README.md)