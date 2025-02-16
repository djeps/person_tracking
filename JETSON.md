[Home](README.md)

# Setting up the Jetson Nano with Ubuntu 20.4

Simply download the SD card image as per the instructions on
[Qengineering's repository](https://github.com/Qengineering/Jetson-Nano-Ubuntu-20-image/tree/main) repository,
and use whatever program you like.

Qengineering suggests [Raspberry Pi's Imager](https://www.raspberrypi.com/software/) or
[balenaEtcher](https://etcher.balena.io/).

I simply used the `dd` command from CLI.

Navigate to the folder where the SD card image is located and (on Linux at least) execute:

```shell
sudo dd if=JetsonNanoUb20_3b.img of=/dev/sdb bs=4M status=progress
```

> Note: Careful! Yor SD card may not be `/dev/sdb`. Therefore, use `lsblk` first to determine yours.

> Note: Qengineering suggest a 32GB (minimum!) SD card. I would say that's more like a minimum of 64GB but I opted for
  a 128GB SD card as it gives me plenty of space to expand my root partion to.

> Note: I used [GParted](https://gparted.org/) on the laptop where I 'burned' the image to my SD card to and expanded
  the SD card's root partion to the maximum available space. But, whatever you do, **don't delete** the other 'strange'
  partitions. They are there for a reason! 

A few extra notes...

- I will not be pushing into my repo all the files that I've generated during the experiments but only the text ones as
  I don't have the space to do so on my free GitHub account.
- I will not be creating any Dockerfile and thus a possibility to replicate this inside a pre-made Docker container because
  I lack the time to do it
- For anyone who might be interested (for whatever reason) in trying all of this out by themselves but lack the patience
  to go through the steps, I can provide a copy of my SD card's image on request until a find a way how to permanently
  host it somewhere. 

[Home](README.md)