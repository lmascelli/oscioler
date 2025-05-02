import numpy as np
import matplotlib.pyplot as plt

frequency = 2  # Hz
amplitude = 1
duration = 5  # seconds
sampling_rate = 100  # samples per second
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# 2. Generate the clean sinusoid
clean_sinusoid = amplitude * np.sin(2 * np.pi * frequency * t)

# 3. Define the noise parameters
noise_amplitude = 0.5

# 4. Generate the random noise
noise = noise_amplitude * np.random.randn(len(clean_sinusoid))

rms = np.sqrt(np.mean(clean_sinusoid ** 2))

new_sin = np.sin(2 * np.pi * frequency * t) * rms * np.sqrt(2)

plt.plot(t, clean_sinusoid+noise)
plt.plot(t, new_sin)
plt.show()
