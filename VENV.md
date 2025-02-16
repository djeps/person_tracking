[Home](README.md)

# Create a Python virtual environment (`venv`)

The reason why we should be doing this, is because we want to keep our base environment clean, and work
in a sort of an *isolated environment*:

Once we are logged into our `jetson` account on the Jetson Nano, we open up a terminal and type in the
following:

```shell
mkdir ~/venv
python3 -m venv --system-site-packages ~/venv/boxmot-venv
```

With the first command we are creating a `venv` folder under our home directory, and this is where we
sould create and keep all of our future virtual environments, should we need to.

The second command actually creates the `boxmot-venv` where we bring all of our system or base packages
in, with the `--system-site-packages` command.

To activate it:

```shell
source ~/venv/boxmot-venv/bin/activate
```

To list all currently available packages to us (which at this point are all the system ones):

```shell
pip3 list
```

> Note: From this point onwards, everything we do inside the `boxmot-venv` will not affect the system packages!

> Note: Should we ever need to get out of any `venv`, we execute `deactivate` inside the terminal.

> Note: But in principle, everything we do from now on, we do it inside the `boxmot-venv`!

> Note: the `pip3` command from above will not list anything *opencv related* because OpenCV isn't installed as a
  `pip package` but rather built from source.

## Confirming the most important system (or base) packages that come with the Qengineering's image

The packages we want to make sure are acessible to us from Python are:

- `OpenCV` (4.8.0)
- `TensorFlow` (2.4.1)
- `Torch` (1.13)
- `TorchVision` (0.14)
- `TensorRT` (8.0.1.6)

To do that, we could execute the `check_packages.sh` script:

```shell
~/scripts/check_packages.sh
```

> Note: The `check_packages.sh` script is part of the SD card image I provide, so that you don't have to
  do any of this.

> Note: Oterwise, if you plan on following and executing each command from the beginning yourself, you
  have to create that file yourself.

If at any stage of the process, you wish to look at the all the available info provided by `pip` about a
certain package (which was installed with `pip`!):

```shell
pip3 show tensorrt
```

This will provide the following output:

```
Name: tensorrt
Version: 8.0.1.6
Summary: A high performance deep learning inference library
Home-page: UNKNOWN
Author: NVIDIA
Author-email: None
License: Proprietary
Location: /home/jetson/.local/lib/python3.8/site-packages
Requires:
Required-by:
```

We can see among other things, the version and the author, but more importantly, we see that this package
doesn't depend on other packages (*Requires*) nor it affects others (*Required-by*)

> Note: Each time we will reboot the target or open a new terminal session, that Python `venv` will not be active
  and therefore, best practice would be to edit the `~/.bashrc` file and add `source ~/venv/boxmot-venv/bin/activate`
  at the end of the file. This way, each time we reboot, log out, log in or open a new terminal session, the
  Python `venv` will always be active! 

[Home](README.md)