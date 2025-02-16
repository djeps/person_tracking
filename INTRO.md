[Home](README.md)

# Introduction
The initial idea behind this project was to use YOLO for object detection -  specifically for pederstrian detection.

First of all, *why YOLO*? YOLO, or *You Only Look Once*, is a SOTA (*State Of The Art*) object detection algorithm
introduced back in 2015. seems to offer the best balance between speed, accuracy and performance and it has found
its way into robotics and autonomous vehicles, as well among several other applications.

Out interest in - my interest in it! - is its application in *autonomous  vehciles* for pedestrian detection.

While we are on the topic of pedestrian detection, I would like to make a few observations of my own.

First of all, YOLO was trained against the COCO dataset for general object  detection. There are several classes
for which it was trained to detect, one of  them being the `person` class, internally represented in the dataset
with a class id of 0.

There is **a disctinct difference** in my opinion beween *a person* and *a  pedestrian*. Think of a 'person' as
the parent or the super class, and the 'pedestrian' as the child class. In other words, a pedestrian is always a
person, but every person is not always a pedestrian.

For example, a person sitting on a  bench, reading a book - that's a person. Someone who's just about to cross the 
street - that's a pedestrian. If we go further, a pedestrian is a person with an intent to engage in traffic!

To me, that's the bottom line, and in that sense and in the context of autonomous vehicles, we should be differentiating
between the two - just as we, when driving a vehicle, differentiate between someone causally walking along the
sidewalk, and someone who's just about to cross the street. We are much more alert of the latter one!

That to me, is the key difference.

But back to our topic and the idea behind this exploratory project. To further elaborate on the intent behind this
project, I would like to add the following...

The intent wasn't to simply use YOLO. For object detection (in this case pedestrians) - yes, but then use the SORT
algorithm (or one of its variants) for object tracking because computationally speaking, *tracking* is cheaper than
*detection*!

... and this is where the BoxMOT project comes into play.

BoxMOX natively uses YOLO for the detection part and several possible variations of the SORT algortihm for tracking.
We then deploy everything on an embedded target HW - device with 'modest' resources - like the Nvidia Jetson Nano
(albeit the use of the word 'modest' here is debatable ), export the YOLO model to an optimized TF model (as in
*Tensor Flow*) using TensorRT (Nvidia's framework for optimizing TF NNs or *neural networks* so that the model works
in the most optimized and efficient way possible on the Nvidia HW) and run the inference and the tracking on the
Jetson Nano and evaluate - *what* if *any* performance we get in doing so.

To make it absolutely clear, we intent on using the `YOLO v8n` (nano) model: 1-it might not be the latest and greatest
but 2-it's well tested, 3-available in the nano variant (less parameters, 'lightweight') and 4-therefore suitable
for deployment on the Jetson Nano.

> Spoiler alert! Using the utility/wrapper scripts from the `BoxMOT` project (for the version I had to settle with!)
  did not go as planned or hoped for. Although technically possible, certainly not without code pruning and updates
  which will become apparent in the last couple of sections. Let's be clear, I an NOT implying there's anything wrong
  with the BoxMOT scripts. I am sure they're well tested. But applied to the Jetson Nano, some quirks apply, and
  because of those quirks, certain code changes were required. At the end, I went with a wrapper script of my own
  based on YOLO and BoxMOT just to test its performance.

# On datasets and model finetuning

With regards to the perfomance of the YOLO model (in principle, regardless of the variant I would say) and its
performance - because of the fact that it was trained on a generalized set with many different classes, my idea was
to fine-tune it for pederstrian detection.

> Spoiler alert! At the end, I opted out of the idea for fine-tuning for reasons which will become apparent
  later on.

Initially, I was going to use [the Waymo Open Dataset (WOD)](https://waymo.com/open/download/)) but I soon realized
two things: 1-it's very (very!) big and therefore any attempt on model training or fine-tuning with it would take me
ages (well, a long time) and 2-neither the current nor (especially!) the latest version is in any format that YOLO works
with directly.

Furthermore, converting it to a YOLO format turned out to be at least a 2-stage process i.e. converting from WOD to
an intermediary (KITTI) format and then from this intermediary format to a YOLO format.

Because of this, I abandoned that idea but left the notes on how I proceeded with obtaining the dataset for reference only.

I then looked into [the KITTI dataset](https://www.cvlibs.net/datasets/kitti/)) - a much smaller model in size but highly
recommended and used frequently, especially in academic circles, conducting research on autonomous driving. This model
as well, couldn't be used directly by YOLO but at least the process of converting it was esentailly a 1-step process.

Then I stumbled upon these 2 datasets on Kaggle:

- [The JAAD dataset](https://www.kaggle.com/datasets/charvik/jaad-frames-dataset-10-v1-yolo-format)
  targeted especially around people and pedestrian detection
- [The Udacity self-driving car dataset](https://www.kaggle.com/datasets/evilspirit05/cocococo-dataset)

At first, my (perhaps) naive approach was going to perform the finetuning in several stages, using each of the datasets
outlined above. From there, I quickly found my self exploring - trying to understand how any finetuning should be done with
care if I want to prevent what's known as *catastrophic forgetting* - the outcome of which a previosly trained model 'looses'
its ability to detect the classes it was initially trained to detect while focusing on finetuning it to detect a
specific class. There are ways of mitigating this, but more on it in one subsequent sections.

Then a colleague of mine had suggested that it's probably better (and thus wiser!) to merge all datasets in one - including
the original dataset YOLO was trained against, and proceed with the finetuning the model to (hopefully) better detect
pedestrians.

.. and this is when I was again reminded of the fact that there's a difference between 'a person' and 'a pedestrian' and that
if we are to achieve best results, we would have to annotate all images with people in them based on the context they are
placed in, and mark them as either one or the other - which esentailly implied I would need to retrain the model to begin with.

... or perhaps not really, I'll have to re-visit this at some stage.

My point is, I side-lined that implication for the purposes of this project, and decided to focus on improving person detection
in general - regardless if they are *active traffic participants* (i.e. 'pedestrians') or simply visitors in a mall. Naturally,
I would like to avoid the effects of *catastrophic forgetting* - if I can, but even if I fail to do so, for the purposes of
this project, it would be completely acceptable.

[Home](README.md)