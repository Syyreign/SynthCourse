# Assignment 2

## Overview
Assignment 2. Assignment2.py generally covers question 1 to question 8. I do want to return to this assignment at a later date, and do the retro game question since that seems fun. I also would like to fix some of my bad coding in here, but times limited.

## **MIDI to MIDI communication**
For the MIDI to MIDI communication it took some time to get the sound to play through a device. At first I was trying to plug the Roland keyboard directly into a small device powered Arpeggiator. For some reason this device was not able to play audio out.

Later, some other people and I decided to try and get the keytar to work. To get this to play, we plugged the keytar into another keyboard found in front of the Mac. This keyboard could be used as a connection from the keytar to the speaker under the desk.

## **Complex Number Multiplication**
```
## The first value of the list is the real number with the second
## being the imaginary
## Ex. 2 + j represented as [2, 1]
## Ex. -5j + 4 represented as [4, -5]

def complex_multiply(complex_number, complex_multiplier):
	print("multiplying: ", complex_number," by ", complex_multiplier)
	return(complex_number[1] * complex_multiplier * -1, complex_number[0] * complex_multiplier)
```

## **MIDI to Computer**

I connected the Roland Keyboard to my computer using a MIDI to USB splitter. It took a while to get audio playing through the computer. For some reason the notes were not being received by my computer. I ended up downloading CSound, which had more diagnostic tools, and was able to receive a set of key inputs.

## **Amplitude and Phase Estimation in Mixture**
![enter image description here](https://raw.githubusercontent.com/Syyreign/DSP-MIDI/main/Waves.png)
A picture with amplitude and phase estimation.


## **Arpeggiator**
https://youtu.be/11XbuDg0sz0

## **EQUAL TEMPERAMENTS**
```
def equal_temperaments():
	p = pyaudio.PyAudio()
	fs = 44100
	stream = p.open(format=pyaudio.paFloat32,
		channels=1,
		rate=fs,
		output=True)
	duration = 1.0
	reference_freq = 110

	for i in range(3, 13):
		frequency_ratio = pow(2, (1/i))
		for j in range(0, i):
			play_note(stream, duration, reference_freq * pow(frequency_ratio, j), fs)

	stream.stop_stream()
	stream.close()
```
By using the frequency ratio, and the reference frequency of 110, I am able to play equal temperaments.

Interestingly, when playing the drone in the background, it almost sounds like the sine waves have a Moiré pattern. Since the waves don't have a period that is a multiple of each other, it creates a warbly effect.

## **Complex Number Plotting**

https://youtu.be/BOrnHDpJgvg

