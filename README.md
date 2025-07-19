# QRS-COMPLEX-DETECTION-IN-ECG-SIGNAL
KEYWORDS: QRS complex Detection algorithms ,  Electrocardiography , Databases , Band pass filters , derivative  Filtering , squaring , Noise reduction , integration.

OVERVIEW:
The primary objective of this project is to accurately detect QRS complexes in ECG signals using the Pan-Tompkins Algorithm. Originally proposed by Pan and Tompkins in 1985, this algorithm has become a cornerstone in real-time ECG beat detection due to its high efficiency and accuracy. The algorithm follows a structured pipeline beginning with pre-processing steps such as bandpass filtering, which combines low-pass and high-pass filters to isolate the desired frequency band and eliminate baseline wander and muscle noise. This is followed by a derivative filter that emphasizes the slope information of the QRS complex. Subsequently, a squaring function is applied to enhance the dominance of the QRS peaks while suppressing the influence of T-waves. A moving window integration step then averages the signal over a specified window to better represent the QRS complex morphology. Post-processing stages include the application of adaptive thresholds, identification of fiducial marks, search for missed beats, and T-wave discrimination to avoid false detections. The Pan-Tompkins Algorithm proves to be highly effective for real-time QRS detection and holds significant potential in enhancing cardiac diagnostics and continuous monitoring in clinical settings.

METHODOLOGY:
A) Noise and Artifact Handling:
   -ECG signals often contain noise from:
      1)Motion Artifacts (body movements)
      2)Baseline Wander (low-frequency drift)
      3)4_Muscle Noise (EMG)
      Power Line Interference (50/60 Hz)
-Pre-processing eliminates these using filters to enhance signal quality.

B) Dataset: MIT-BIH Arrhythmia Database:
      1)Publicly available dataset from PhysioNet
      2)Annotated ECG signals with various arrhythmia types
      3)Used for training and validating the QRS detection algorithm

C) Pan-Tompkins Algorithm:
STEP 1: Pre-processing :
1. Bandpass Filtering (5–15 Hz):
   -Combines:
      1)Low-pass filter: Removes high-frequency noise
      2)High-pass filter: Removes baseline wander
2. Derivative Filter:
      1)Highlights steep slopes of QRS complex.
      2)Emphasizes rapid amplitude changes.
3. Squaring Function:
      1)Amplifies high-frequency components
      2)Makes QRS peaks more prominent
      3)Formula: y(nT) = [x(nT)]²
4. Moving Window Integration (0.15s window):
      1)Smooths the signal
      2)Helps in identifying width and energy of QRS
      3)Running average of squared signal
   
STEP 2: Post-processing:
1. Fiducial Marking:
   -Identifies local maxima in the integrated signal.
      -200ms refractory period applied after each detection
2. Adaptive Thresholding:
   -Two dynamic thresholds (high and low) are calculated and updated based on:
      -Signal peak (SPK)
      -Noise peak (NPK)
   -If no QRS detected → search-back using lower threshold
3. T-Wave Discrimination:
      -T-waves often follow QRS
      -Compared slope of candidate vs. previous QRS
   -If slope < 50%, reject as T-wave
4. Heart Rate (HR) Calculation:
   -Using RR-intervals between detected R-peaks:
      -HR (bpm) = 60 / RR_interval(s)
5. Heartbeat Regularity Checks:
      -Uses RR averages and limits
      -Detects irregular heartbeats & missed QRS complexes
