import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import scipy.signal

def main():
    CoffeeMugs()
    pass


def CoffeeMugs():
    p = pyaudio.PyAudio()

    srate = 44100 
    freq = 150

    duration = 3.0

    p1 = sinusoid(200 * 1.0, dur=duration)
    s1 = [(0.3, 50, 0), (0.1, 100, 0), (0.0, 200, 200)]
    partial(p1, s1, srate, duration)
        
    p2 = sinusoid(freq * 10.01, dur=duration)
    s2 = [(0.5, 50, 0), (0.2, 100, 0), (0.0, 200, 200)]
    partial(p2, s2, srate, duration)

    p3 = sinusoid(freq * 20.1, dur=duration)
    s3 = [(1.0, 50, 0), (0.45, 100, 0), (0.0, 200, 200)]
    partial(p3, s3, srate, duration)

    p4 = sinusoid(freq * 89.1, dur=duration)
    s4 = [(1.0, 50, 0), (0.35, 100, 0), (0.0, 200, 200)]
    partial(p4, s4, srate, duration)

    coffee_cup1 = (p1+p2+p3+p4)*0.25 
    cup1_bytes = coffee_cup1.tobytes()

    p5 = sinusoid(800 * 1.0, dur=duration)
    s5 = [(0.1, 50, 0), (0.01, 100, 0), (0.0, 200, 200)]
    partial(p5, s5, srate, duration)
        
    p6 = sinusoid(freq * 2.75, dur=duration)
    s6 = [(1.0, 40, 0), (0.1, 75, 0), (0.0, 200, 200)]
    partial(p6, s6, srate, duration)

    p7 = sinusoid(freq * 6.4, dur=duration)
    s7 = [(0.5, 50, 0), (0.15, 100, 0), (0.0, 200, 200)]
    partial(p7, s7, srate, duration)

    p8 = sinusoid(freq * 22.4, dur=duration)
    s8 = [(1.0, 50, 0), (0.35, 100, 0), (0.0, 200, 200)]
    partial(p8, s8, srate, duration)

    coffee_cup2 = (p5+p6+p7+p8)*0.25 
    cup2_bytes = coffee_cup2.tobytes()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=srate,
                    frames_per_buffer=1000,
                    output=True)

    stream.write(cup1_bytes)
    stream.write(cup2_bytes)
    stream.stop_stream()
    stream.close()

    p.terminate()


## Modified from Additive Synthesis by G. Tzanetakis, University of Victoria
## https://github.com/gtzan/synthesizers_cs_perspective/blob/main/src/notebooks/additive_synthcsp.ipynb
def partial(samples, env_tuple, srate, duration):
    nsamples = int(srate*duration)
    data = np.zeros(nsamples)
    env = envelope(data, env_tuple, 
                       srate, duration)
    #plt.plot(env)
    #plt.show()

    np.multiply(samples, env, samples)

## Taken from Additive Synthesis by G. Tzanetakis, University of Victoria
## https://github.com/gtzan/synthesizers_cs_perspective/blob/main/src/notebooks/additive_synthcsp.ipynb
def envelope(data, segments,srate,duration): 
    nsamples = int(srate*duration)
    value = 0.0
    segment_index = 0 
    segment_sample = 0 
    prev_target = 0.0

    for i in np.arange(nsamples): 
        if (segment_index < len(segments)): 
            target = segments[segment_index][0]
            ramp_time = segments[segment_index][1]
            delay_time = segments[segment_index][2]
            
            ramp_samples = (ramp_time / 1000.0) * srate 
            delay_samples = (delay_time / 1000.0) * srate
            
            if i < segment_sample + ramp_samples: 
                incr = (target-prev_target) / ramp_samples 
            elif i < segment_sample + ramp_samples + delay_samples: 
                incr = 0.0 
            else: 
                if ramp_samples != 0.0: 
                    incr = (target-prev_target) / ramp_samples 
                else: 
                    incr = 0.0 
                segment_sample = i 
                segment_index = segment_index+1 
                prev_target = target 
            value = value + incr 
        data[i] = value
    return data

def sinusoid(freq, dur, srate=44100, amp=1.0): 

    data = amp * (np.sin(2 * np.pi * np.arange(srate * dur) * freq / srate)).astype(np.float32)

    return data

    
if __name__ == "__main__":
    main()