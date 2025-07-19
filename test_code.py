import wfdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

class Pan_Tompkins_QRS:
    def __init__(self, fs):
        self.fs = fs
        self.THRESHOLDI1 = 0
        self.THRESHOLDF1 = 0
        self.THRESHOLDI2 = 0
        self.THRESHOLDF2 = 0

    def low_pass_filter(self, signal):
        low_pass_signal = signal.copy()
        for time in range(len(signal)):
            curr = signal[time]
            if time >= 1:
                curr += 2 * low_pass_signal[time - 1]
            if time >= 2:
                curr -= low_pass_signal[time - 2]
            if time >= 6:
                curr -= 2 * signal[time - 6]
            if time >= 12:
                curr += signal[time - 12]
            low_pass_signal[time] = curr
        low_pass_signal = low_pass_signal / max(abs(low_pass_signal))
        return low_pass_signal

    def high_pass_filter(self, signal):
        high_pass_signal = signal.copy()
        for time in range(len(signal)):
            curr = -1 * signal[time]
            if time >= 16:
                curr += 32 * signal[time - 16]
            if time >= 1:
                curr -= high_pass_signal[time - 1]
            if time >= 32:
                curr += signal[time - 32]
            high_pass_signal[time] = curr
        high_pass_signal = high_pass_signal / max(abs(high_pass_signal))
        return high_pass_signal

    def band_pass_filter(self, signal):
        low_pass_signal = self.low_pass_filter(signal)
        band_pass_signal = self.high_pass_filter(low_pass_signal)
        return band_pass_signal

    def derivative(self, signal):
        T = 1 / self.fs
        derivative_signal = signal.copy()
        for time in range(len(signal)):
            curr = 0
            if time >= 2:
                curr -= signal[time - 2]
            if time >= 1:
                curr -= 2 * signal[time - 1]
            if time < len(signal) - 1:
                curr += 2 * signal[time + 1]
            if time < len(signal) - 2:
                curr += signal[time + 2]
            derivative_signal[time] = (curr / (8 * T))
        return derivative_signal

    def squaring(self, signal):
        return np.square(signal)

    def moving_window_integration(self, signal):
        window_size = int(0.15 * self.fs)
        moving_window_signal = signal.copy()
        for time in range(len(signal)):
            curr = 0
            for index in range(window_size):
                if time - index < 0:
                    break
                curr += signal[time - index]
            moving_window_signal[time] = curr / (index + 1)
        return moving_window_signal

    def solve(self, signal):
        band_pass_signal = self.band_pass_filter(signal.copy())
        derivative_signal = self.derivative(band_pass_signal.copy())
        square_signal = self.squaring(derivative_signal.copy())
        moving_window_avg_signal = self.moving_window_integration(square_signal.copy())
        return moving_window_avg_signal, band_pass_signal, derivative_signal, square_signal

    def detect_peaks(self, ecg_signal):
        from scipy.signal import find_peaks
        filtered, *_ = self.solve(ecg_signal)
        peaks, _ = find_peaks(filtered, distance=int(0.2 * self.fs))
        return peaks

    def plot_filter_response(self, signal, filtered_signal, filter_name):
        plt.figure(figsize=(20, 4))
        plt.plot(signal, label='Original Signal')
        plt.plot(filtered_signal, label=f'{filter_name} Filtered Signal', linestyle='dashed')
        plt.title(f'{filter_name} Filtered ECG Signal')
        plt.xlabel('Time (samples)')
        plt.ylabel('ECG Signal Amplitude')
        plt.legend()
        plt.show()

# Main program
signal_number = int(input("Enter the signal number (0 to 24): "))
filename = f'C:/Users/Janani/Desktop/mit-bih-arrhythmia-database-1.0.0/mit-bih-arrhythmia-database-1.0.0/{str(100 + signal_number)}'

record = wfdb.rdrecord(filename, sampfrom=180, sampto=4000)
annotation = wfdb.rdann(filename, 'atr', sampfrom=180, sampto=4000, shift_samps=True)

ecg = pd.DataFrame(np.array([list(range(len(record.adc()))), record.adc()[:, 0]]).T, columns=['TimeStamp', 'ecg'])
ecg_signal = ecg.iloc[:, 1].to_numpy()
time_stamp = ecg.TimeStamp
fs = annotation.fs

QRS_detector = Pan_Tompkins_QRS(fs)
integration_signal, band_pass_signal, derivative_signal, square_signal = QRS_detector.solve(ecg_signal.copy())

plt.figure(figsize=(20, 4))
plt.plot(time_stamp, ecg_signal)
plt.title("Raw ECG Signal")
plt.xlabel('Time (ms)')
plt.ylabel('ECG Signal Amplitude')
plt.show()

r_peaks = QRS_detector.detect_peaks(ecg_signal)

QRS_detector.plot_filter_response(ecg_signal, QRS_detector.low_pass_filter(ecg_signal.copy()), 'Low Pass')
QRS_detector.plot_filter_response(ecg_signal, QRS_detector.high_pass_filter(ecg_signal.copy()), 'High Pass')

plt.figure(figsize=(20, 4))
plt.plot(time_stamp[30:], band_pass_signal[30:])
plt.title("Band Pass Filtered ECG Signal")
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.show()

plt.figure(figsize=(20, 4))
plt.plot(time_stamp[30:len(time_stamp) - 10], derivative_signal[30:len(time_stamp) - 10])
plt.title("Derivative ECG Signal")
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.show()

plt.figure(figsize=(20, 4))
plt.plot(time_stamp[30:len(time_stamp) - 10], square_signal[30:len(time_stamp) - 10])
plt.title("Squared ECG Signal")
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.show()

plt.figure(figsize=(20, 4))
plt.plot(time_stamp[80:len(time_stamp) - 10], integration_signal[80:len(time_stamp) - 10])
plt.title("Moving window averaged ECG Signal")
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.show()

plt.figure(figsize=(20, 4))
plt.plot(time_stamp, ecg_signal)
plt.scatter(r_peaks, ecg_signal[r_peaks], c='r', label='Detected R-peaks')
plt.title("Raw ECG Signal with Detected R-Peaks")
plt.xlabel('Time (ms)')
plt.ylabel('ECG Signal Amplitude')
plt.legend()
plt.show()

rr_intervals = np.diff(r_peaks) / fs
heart_rate = (60 / np.mean(rr_intervals))
print(f"Heart Rate: {heart_rate:.2f} beats per minute")
