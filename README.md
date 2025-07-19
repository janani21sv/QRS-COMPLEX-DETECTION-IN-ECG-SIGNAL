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


<img width="174" height="464" alt="image" src="https://github.com/user-attachments/assets/838c0068-572e-458b-b14b-fe13c792aa3e" />


RESULT AND DISCUSSION: 
The MIT-BIH Arrhythmia Database stands as a monumental archive, housing 48 half-hour snippets of two- channel ambulatory ECG recordings. The recordings, originating between 1975 and 1979, showcase the collaborative efforts of the BIH Arrhythmia Laboratory, delving into the cardiac intricacies of 47 subjects. Notably, 23 recordings were serendipitously selected from a vast pool of 4000 24-hour ambulatory ECG recordings, drawn from a diverse cohort of inpatients (60%) and outpatients (40%) at Boston's Beth Israel Hospital. Complementing this, an additional 25 recordings were intentionally chosen to spotlight less common yet clinically significant arrhythmias, adding a unique dimension to the dataset.The digitization process, executed at 360 samples per second per channel with 11-bit resolution, ensures a meticulous capture of ECG signals, providing a high-fidelity representation of cardiac dynamics. The dataset's robustness is further accentuated by the involvement of two or more cardiologists independently annotating each record, culminating in a rich repository of approximately 110,000 reference annotations for each beat.

This comprehensive MIT-BIH Arrhythmia Database, in its entirety, has been accessible since PhysioNet's inception in September 1999. The release of the remaining 23 signal files,previously exclusive to the MIT-BIH Arrhythmia Database CD- ROM, in February 2005, marked a significant stride in open access to this invaluable resource. For deeper insights, researchers can explore the extensive MIT-BIH Arrhythmia Database Directory, providing a wealth of supplementary information. This repository not only chronicles cardiac nuances but also stands as a testament to collaborative research, fostering advancements in the understanding and treatment of cardiac rhythm disorders.

SAMPLE OUTPUTS:
<img width="552" height="155" alt="image" src="https://github.com/user-attachments/assets/639c6aa2-d758-478c-989e-5ca85adc0c0d" />
<img width="552" height="155" alt="image" src="https://github.com/user-attachments/assets/b2badb67-56b5-4cfb-85ca-cca289ecdca4" />
<img width="552" height="155" alt="image" src="https://github.com/user-attachments/assets/336e6307-3f71-40de-9379-9ba8bb0821fb" />
<img width="552" height="115" alt="image" src="https://github.com/user-attachments/assets/a7267192-42fa-47a4-b86d-f52d7cafecaa" />
<img width="552" height="155" alt="image" src="https://github.com/user-attachments/assets/ab705f2d-9672-4027-882d-5b743ce81472" />
<img width="552" height="155" alt="image" src="https://github.com/user-attachments/assets/0d863467-a72a-42f8-844a-31b213fa691a" />
<img width="552" height="155" alt="image" src="https://github.com/user-attachments/assets/94085f33-c7a0-4458-b725-8d79f32b2573" />
<img width="552" height="155" alt="image" src="https://github.com/user-attachments/assets/60ba57bb-3f6f-48a6-87fa-3a90e940d0d4" />
