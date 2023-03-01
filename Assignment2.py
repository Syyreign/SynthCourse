import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import math
import mido
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF

def main():

    #print(complex_multiply((6, 8), 2))
    ##amplitude_estimation()
    complex_plot()
    ##equal_temperaments()
    ##midi_arpeggiator((60, 62, 67, 60), 100, 2)


## The first value of the list is the real number with the second
## being the imaginary
## Ex. 2 + j represented as [2, 1]
## Ex. -5j + 4 represented as [4, -5]
def complex_multiply(complex_number, complex_multiplier):
    print("multiplying: ", complex_number," by ", complex_multiplier)
    return(complex_number[1] * complex_multiplier * -1, complex_number[0] * complex_multiplier)

def amplitude_estimation():
    p = pyaudio.PyAudio()

    fs = 44100
    duration = 1.0

    ## The scalar for the samples
    r0_scalar = random.random()
    r1_scalar = random.random()
    r2_scalar = random.random()

    ## The wave phase shift
    r0_phase = random.uniform(0.0, 44100.0)
    r1_phase = random.uniform(0.0, 44100.0)
    r2_phase = random.uniform(0.0, 44100.0)

    samples0 = (np.sin((2 * np.pi * np.arange(fs * duration) * 100.0 / fs) - r0_phase)).astype(np.float32) * r0_scalar
    samples1 = (np.sin((2 * np.pi * np.arange(fs * duration) * 200.0 / fs) - r1_phase)).astype(np.float32) * r1_scalar
    samples2 = (np.sin((2 * np.pi * np.arange(fs * duration) * 300.0 / fs) - r2_phase)).astype(np.float32) * r2_scalar

    ## The standard amplitude of this frequency
    samples_amp = (np.sin((2 * np.pi * np.arange(fs * duration) * 100.0 / fs) - r0_phase)).astype(np.float32)
    amp_est0 = (np.dot(samples0, samples_amp) * 2)/fs
    samples_amp = (np.sin((2 * np.pi * np.arange(fs * duration) * 200.0 / fs) - r1_phase)).astype(np.float32)
    amp_est1 = (np.dot(samples1, samples_amp) * 2)/fs
    samples_amp = (np.sin((2 * np.pi * np.arange(fs * duration) * 300.0 / fs) - r2_phase)).astype(np.float32)
    amp_est2 = (np.dot(samples2, samples_amp) * 2)/fs

    phase_est0 = get_phase_est_brute(samples0, fs, 1.0, 100)
    phase_est1 = get_phase_est_brute(samples1, fs, 1.0, 200)
    phase_est2 = get_phase_est_brute(samples2, fs, 1.0, 300)

    combined_samples = 0.3333 * np.add(np.add(samples0, samples1), samples2)

    output_bytes = combined_samples.tobytes()

    ## Opens a stream to play the audio
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    stream.write(output_bytes)

    stream.stop_stream()
    stream.close()

    p.terminate()

    plot_samples = 500

    plot_sample(samples0[:plot_samples], samples1[:plot_samples], samples2[:plot_samples], combined_samples[:plot_samples], plot_samples, amp_est0, amp_est1, amp_est2, phase_est0, phase_est1, phase_est2)

## The brute force to find the phase shift by checking each do product
def get_phase_est_brute(samples, fs: float, duration: float, frequency: float):
    highest_dot = -1
    dot_index = 0

    period = (fs/frequency)
    print(period)

    for i in range(int(period)):
        basis_samples = (np.sin((2 * np.pi * np.arange(fs * duration) * frequency / fs) - i)).astype(np.float32)

        current_dot = np.dot(samples, basis_samples)
        if(current_dot > highest_dot):
            highest_dot = current_dot
            dot_index = i
        
    return dot_index


def get_phase_est(samples, fs: float, duration: float, frequency: float):
    sin_samples = (np.sin((2 * np.pi * np.arange(fs * duration) * frequency / fs))).astype(np.float32)
    cos_samples = (np.cos((2 * np.pi * np.arange(fs * duration) * frequency / fs))).astype(np.float32)

    print(np.dot(samples, sin_samples), ", ", np.dot(samples, cos_samples))
        

## Plot the samples
def plot_sample(samples0, samples1, samples2, combined_samples, plot_samples, est0, est1, est2, p_est0, p_est1, p_est2):

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(np.arange(plot_samples), samples0, label="Est Amplitude: " + str(round(est0,3)) + " Est Phase: "+ str(p_est0))
    ax.plot(np.arange(plot_samples), samples1, label="Est Amplitude: " + str(round(est1,3)) + " Est Phase: "+ str(p_est1))
    ax.plot(np.arange(plot_samples), samples2, label="Est Amplitude: " + str(round(est2,3)) + " Est Phase: "+ str(p_est2))
    ax.plot(np.arange(plot_samples), combined_samples)
    ax.legend(loc="upper left")
    ax.set_ylim(-1.5, 1.5)
    plt.show()

## A midi arpeggiator.
## notes: a list of notes to run through
## tempo: the beats per minute
## mode: an int representing the mode of the arpeggiator
## 0: Up, 1: Down, 2: Up/Down 
def midi_arpeggiator(notes, tempo, mode):

    msg_on = mido.Message('note_on', note=60)
    msg_off = mido.Message('note_off', note=60)
    ##port = mido.open_input('Bus 1')
    print(mido.get_output_names())
    port = mido.open_output(mido.get_output_names()[1])


    if mode == 0:
        i = 0
        while(True):

            port.send(mido.Message('note_on', note=notes[i]))
            time.sleep(60/tempo)
            port.send(mido.Message('note_off', note=notes[i]))  
            
            i = (i+1) % (len(notes))
    elif mode == 1:
        i = len(notes) - 1
        while(True):
            if(i < 0):
                i = len(notes) - 1

            port.send(mido.Message('note_on', note=notes[i]))
            time.sleep(60/tempo)
            port.send(mido.Message('note_off', note=notes[i]))  
            
            i -= 1

    elif mode == 2:

        while(True):
            i = random.randrange(len(notes))

            port.send(mido.Message('note_on', note=notes[i]))
            time.sleep(60/tempo)
            port.send(mido.Message('note_off', note=notes[i]))  


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

def play_note(stream, duration, frequency, fs):
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)
    adsr(samples, fs)

    output_bytes = samples.tobytes()
    stream.write(output_bytes)

## Create a adsr for the arpeggiator
def adsr(samples, fs):

    ## Hardcoded adsr values
    a = 0.15
    d = 0.2
    s = 0.45
    r = 0.2
    v = 0.5

    samples_len = len(samples)

    a_len = int(samples_len * a)
    d_len = int(samples_len * (a+d))
    s_len = int(samples_len * (a+d+s))
    r_len = samples_len

    a_arange = np.arange(0, a_len, 1)
    a_samples = a_arange / (fs * a)

    d_arange = np.arange(a_len, d_len, 1)
    d_samples = (((d_arange/fs - a - d) * (d_arange/fs - a - d)) * ((1-v)/(d*d))) + v

    s_arange = np.full(s_len - d_len, 1)
    s_samples = v * s_arange

    r_arange = np.arange(s_len, r_len, 1)
    r_samples = ((r_arange/fs - a - d - s - r) * (r_arange/fs - a - d - s - r)) * (v / (r * r))

    adsr = np.concatenate((a_samples, d_samples, s_samples, r_samples), axis=0)

    np.multiply(samples, adsr, samples)

## Plot the 3 imaginary circles
def complex_plot():
    
    ## Time entered to show on the clock. Values are unchecked, so could cause crashing
    time = input("Enter a time (Ex: 4:15): \n")
    split_time = time.split(":")
    split_time = int(split_time[0]),int(split_time[1])

    fig, axes = plt.subplots(1, 3)

    for ax in axes:
        circ = plt.Circle((0, 0), 1.0, color='r')
        ax.set_aspect( 1 )
        ax.set_aspect( 1 )
        ax.set_ylim(-1.0, 1.0)
        ax.set_xlim(-1.0, 1.0)
        ax.add_artist( circ )

    ## Create a clock for the input time
    axes[0].clear()
    circ = plt.Circle((0, 0), 1.0, color='r')
    axes[0].set_ylim(-1.0, 1.0)
    axes[0].set_xlim(-1.0, 1.0)
    axes[0].add_artist( circ )
    hour_hand = rotate_vector((1,0), (-30 * split_time[0] + 90))
    axes[0].plot((0,hour_hand[0]), (0,hour_hand[1] * 0.75), marker = 'o')
    seconds_hand = rotate_vector((1,0), (-6 * split_time[1] + 90))
    axes[0].plot((0,seconds_hand[0] * 0.75), (0,seconds_hand[1]), marker = 'o')

    ## Animate the forward and backward clock
    def animate(i):
        axes[1].clear()
        circ = plt.Circle((0, 0), 1.0, color='r')
        axes[1].set_ylim(-1.0, 1.0)
        axes[1].set_xlim(-1.0, 1.0)
        axes[1].add_artist( circ )
        rotated_vector = rotate_vector((1,0), 6*i)
        axes[1].plot((0,rotated_vector[0]), (0,rotated_vector[1]), marker = 'o')

        axes[2].clear()
        circ = plt.Circle((0, 0), 1.0, color='r')
        axes[2].set_ylim(-1.0, 1.0)
        axes[2].set_xlim(-1.0, 1.0)
        axes[2].add_artist( circ )
        rotated_vector = rotate_vector((1,0), -6*i)
        axes[2].plot((0,rotated_vector[0]), (0,rotated_vector[1]), marker = 'o')
        

        return 

    animation = FuncAnimation(fig, animate, frames=1000, interval=1000)
    plt.show()

def multiply_complex(complex_multiplicand, complex_multiplier):
    x = (complex_multiplicand[0] * complex_multiplier[0]) + (complex_multiplicand[1] * -complex_multiplier[1])
    i = (complex_multiplicand[0] * complex_multiplier[1]) + (complex_multiplicand[1] *  complex_multiplier[0])

    complex_num = (x, i)
    complex_num = normalize_vector((x, i))
    return(complex_num)

def normalize_vector(vector):
    magnitude = get_vector_magnitude(vector)
    return (vector[0] / magnitude, vector[1] / magnitude) 

def get_vector_magnitude(vector):
    return math.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))

def rotate_vector(vector, degree):
    degree = -degree * (math.pi / 180)
    x = (vector[0] * math.cos(degree)) + (vector[1] * math.sin(degree))
    y = (-vector[0] * math.sin(degree)) + (vector[1] * math.cos(degree))
    return(x,y)


if __name__ == "__main__":
    main()