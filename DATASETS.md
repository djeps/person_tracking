[Home](README.md)

# Notes on obtaining the referenced datasets

## Downloading the Waymo Open Dataset

As the dataset itself is hosted on Google Cloud, we will need to setup some tools in advance.

First of all, we have download and install [the Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk).

The process is pretty straightforward and documented on the same page where you  download it from, but
in a nutshell, what we need to do (if you're on any Linux  flavor or Mac OS) is to:

- Download the arhchive package for your your architecture
- Unpack it
- Execute the shell provided script and follow the instructions
    - which if you just follow the instruction, should be `./google-cloud-sdk/install.sh`
- While you're inside the terminal, setup a folder structure in a similar way the *Waymo Open Dataset* is organized
- On the [Waymo Open Dataset page](https://waymo.com/open/download/), select the  dataset you wish to download
- You will have to provide your login credentials (I used my Google account to do so and used the same inside the terminal to download the data from Google Cloud)
    - For example, I went with [the V 2.0.1 modular dataset without maps ](https://console.cloud.google.com/storage/browser/waymo_open_dataset_v_2_0_1)
    - Select the parts of the dataset you're interested in downloading
    - From there, I selected the `camera_image` content from each sub-folder (`testing_location`, `testing`, `training`, `validation`)
        - It makes no practical sense to try and download everything
            - First of all, you won't be needing it
            - Second of all, more than likely - especially f you're an independent researcher or a student - you don't and you won't have the infrastructure to use all of it
    - Click the Download button and you will get a CLI command you need to execute
    - But before you do that, execute `gcloud auth login` inside the terminal to first log in
    - Then paste in and execute the CLI command that was generated one step prior
    - As the there's a lot of data available and it's separated into pages, you might need to repeat the above step a few times
    
## Downloading the KITTI dataset

YOLO was trained with the MS COCO dataset and as it turns out, should we want to train it from the beginning
with a different dataset or use it for fine tuning, it accepts certain formats and the WOD (*Waymo Open Dataset*)
is not one of them - in neither of the two versions.

There are a couple of intermediary steps which are involved:

- Convert the WOD dataset to a KITTI format
- From there, convert the KITTI dataset to a YOLO 'approved' format

This seems like an unneccessary overhead for the purposes of this effort, so we are going to abandon it for the moment.
It would be better, if e.g. Ultralytics or Waymo provide this in a form of a Python script out-of-the box. This especially
makes sense when both the model (YOLO) and the dataset (WOD) are so popular in an  academic research context.

The [KITTI dataset](https://www.cvlibs.net/datasets/kitti/), a project funded by the *Karlsruhe Institute of Technology*
(KIT) and the *Toyota Technological Institute at Chicago* (TTI-C) is another well respected and used option. Using it 
with YOLO is not as involving as is the case with the WOD but we still need to make few preparation steps.

The data itself could be used almost as is, albeit formatted and structured for use with YOLO (e.g. convert the KITTI
annotations to a YOLO format).

We could download it directly, or thorugh a Python script. We are going to utilze the second approach because such a script
(`get_dataset.py`) will give us the flexibility to programatically download other datasets as well.

## Downloading the JAAD and Udacity datasets

These two were simply downloaded directly from Kaggle, but I suppose there are Python API-supported ways of obtaining them,
as it was the case with the aforementioned ones.

- [The JAAD dataset](https://www.kaggle.com/datasets/charvik/jaad-frames-dataset-10-v1-yolo-format)
- [The Udacity self-driving car dataset](https://www.kaggle.com/datasets/evilspirit05/cocococo-dataset)

## Downloading (and managing!) datasets with FiftyOne

[FiftyOne](https://docs.voxel51.com/) turned out to be a very interesting tool.  It offers a lot, and among some of
its functionalities, it works with predefined datasets - giving you the option to download them, convert from one to
a different format and much more.

To install it, it's pretty straightforward. All you have to do is execute: `pip install fiftyone` in your terminal.
You can download both the COCO and the KITTI datasets using this tool.

For the KITTI dataset, type: `fiftyone zoo datasets load kitti --split None --dataset-name kitti-dataset-no-split` in
your terminal. Technically, this should download both the `train` and `test` splits and you should be able to load it
for viewing by executing: `fiftyone app launch kitti-dataset-no-split`.

A better option is to download and name each split individually. That way, viewing them for further annotation would be
clearly separated.

For example: `fiftyone zoo datasets load kitti --split train --dataset-name kitti-dataset-train-split` and from there:
`fiftyone app launch kitti-dataset-train-split`.

To convert from the KITTI model format to the YOLO format (for the train split), we need to execute the following:

```shell
fiftyone convert \
    --input-dir /mnt/data/outliers/jepson/datasets/fiftyone/kitti/train \
    --input-type fiftyone.types.KITTIDetectionDataset \
    --output-dir /mnt/data/outliers/jepson/datasets/fiftyone/yolov11/train \
    --output-type fiftyone.types.YOLOv5Dataset \
    --output-kwargs classes_file=/mnt/data/outliers/jepson/datasets/fiftyone/kitti/classes.txt
```

...where the `classes.txt` file is our input to the conversion process and contains all the defined classes in the KITTI
dataset, one class name per line.

While there might certainly be other tools such as this one outthere, it would be brilliant if FiftyOne supports the
*Waymo Open Dataset* natively!

[Home](README.md)