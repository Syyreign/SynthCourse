# Assignment 4 Water Droplet Synthesis

Paper used http://persianney.com/kvdoelcsubc/publications/prep04.pdf

## **1**
As the paper describes, water on its own does not create a large noise. The sound we hear from water droplets and bubbles come from the trapping of air under the waters surface. When this pocket of air collapses, it produces a sinosoidal sound. Its explained that volume pulsation is the main idea behind a bubble noise, with the bubble being a compressible region within the water which is itself incompressible. We can model this interaction using a spring mass system.

## **2**
Using the bubble noise simulator found from question 1, a more complex water noise simulation can be created. This simulation can handle sounds from waterfalls to rain. By creating a program where differently sized bubbles can be produced, and played based on a weighting, a complex water sound can be created. In the paper this was handled using sliders for a variety of bubble sizes, and the statistical properties of how rain sounds. By using the frequency of a bubble with a certain radii taken from the data, we can create a distribtion of how frequently each bubble radii will play. By playing these all together, we can create complex water sound.

## **3**
[droplet.mp3](droplet.mp3) is the sound of me dropping a bit of water into a coffee cup from roughly 50cm in the air. The drop was particularly large, giving it a low frequency.

Time plot of the droplet
![Coffee Cup Spectra 1](https://raw.githubusercontent.com/Syyreign/SynthCourse/main/Assignment4/DropletTimePlot.png)

## **4**

Droplet Magnitude Spectrum
![Coffee Cup Spectra 1](https://raw.githubusercontent.com/Syyreign/SynthCourse/main/Assignment4/DropletMagnitudeSpectrumDb.png)

Droplet Spectrogram
![Coffee Cup Spectra 1](https://raw.githubusercontent.com/Syyreign/SynthCourse/main/Assignment4/DropletSpectrogram.png)

Droplet Linear Spectrogram
![Coffee Cup Spectra 1](https://raw.githubusercontent.com/Syyreign/SynthCourse/main/Assignment4/DropletSpectrogramLinear.png)

## **5,6,7**
These 3 can be found in [droplet.ipynb](droplet.ipynb). Plots relating to each has also been included
