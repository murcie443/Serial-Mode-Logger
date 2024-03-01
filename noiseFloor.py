from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from collections import deque
from matplotlib.animation import FuncAnimation

datastore = './Dataset/noise shorting.txt'

#export the current mode
currentmode=np.loadtxt(datastore, dtype='str', max_rows=1)[-1]

#export the k value
k_value=float(np.loadtxt(datastore, dtype='float', usecols=(1), skiprows=1,max_rows=1))

#export the offset
offset=np.loadtxt(datastore, dtype='float', usecols=(1), skiprows=2, max_rows=1)

#export the data rate
data_rate=int(np.loadtxt(datastore, dtype='int', usecols=(4), skiprows=3, max_rows=1))

#export the conversion factor
factor=1

#export the timestamp
timestamp = np.loadtxt(datastore, dtype='str', usecols=(0), skiprows=6)

#export the dataset(reversed) without the 1st array for a problem
data_matrix = np.loadtxt(datastore, dtype='int', skiprows=6, usecols=np.arange(1, data_rate+1),max_rows=len(timestamp)-1)

# Remove the first column from matrix (various errors)
data_matrix = data_matrix[5:]

#create a 1D array from the matrix
data_array = np.concatenate(data_matrix)

#apply the conversion factor
gain=k_value*factor
data_matrix = np.dot(data_matrix,gain)-offset

# Flatten the matrix
data_array = data_matrix.flatten()

# Calculate the FFT of the data
fft_result = np.fft.fft(data_array)

# Calculate the amplitude of the FFT in decibels
fft_amplitude = 20 * np.log10(np.abs(fft_result))

# Create the frequency array
freqs = np.fft.fftfreq(data_array.size, 1/data_rate)

# Plot the FFT showing only the positive frequencies
fig, ax = plt.subplots()
ax.plot(freqs[:data_array.size//2], fft_amplitude[:data_array.size//2])
plt.show()
# Extract the maximum frequency and amplitude
max_amplitude = np.max(fft_amplitude)

# Extract the frequency at the maximum amplitude
max_freq = freqs[np.argmax(fft_amplitude)]

# Print the results
print(f'\n\n\n\nMaximum amplitude: {max_amplitude} dB')
print(f'Frequency at maximum amplitude: {max_freq} Hz')

# Calculate the ENOB of the signal
enob = (max_amplitude - 1.76) / 6.02

# Print the ENOB
print(f'ENOB: {enob:.2f} bits')

# Calculate the SNR of the signal
snr = (6.02 * enob) - 1.76

# Print the SNR
print(f'SNR: {snr:.2f} dB')

# Calculate the SINAD of the signal
sinad = 1.76 + (6.02 * enob)

# Print the SINAD
print(f'SINAD: {sinad:.2f} dB')