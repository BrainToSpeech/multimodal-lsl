# Multimodal LSL Mini-Suite

Minimal examples for streaming **microphone** and **webcam** to **Lab Streaming Layer (LSL)** and for quickly validating recorded **XDF** files.

## Repository Layout
.  
├─ mic_to_lsl.py         # Microphone → LSL (Audio)  
├─ webcam_to_lsl.py      # Webcam → LSL (Video)  
├─ paradigm_session_marker.py  # Marker → LSL  
├─ read_xdf_check.py     # Quick sanity check for XDF files  
└─ requirements.txt      # Dependencies  

## Stream Specs (Defaults)

- **Microphone**  
  `type="Audio"`, `channel_count=1` (sampling rate depends on OS/device)
- **Webcam_External**  
  `type="Video"`, `channel_count=1` (frame rate depends on device/codec)
- **BCI_Markers** *(optional, from a paradigm app)*  
  `type="Markers"`, single string channel (codes sent as strings)

When recording with **LabRecorder**, you’ll typically see:  
BCI_Markers (Markers), Webcam_External (Video), Microphone (Audio)

## Installation
```bash
python -m venv .venv
```
pip install -r requirements.txt

## Usage

### 1) Stream microphone to LSL
```bash
python mic_to_lsl.py
```
- Logs device info and sampling rate.  
- Stream name: `Microphone`, type: `Audio`.

### 2) Stream webcam to LSL
```bash
python webcam_to_lsl.py
```
- Sends frames from the default camera.  
- Stream name: `Webcam_External`, type: `Video`.

> If multiple devices are present, edit `device_index` / `camera_index` at the top of each script.

### 3) Record with LabRecorder
1. Open LabRecorder → **Refresh** → select the streams (include markers if available)  
2. Click **Start** to record → **Stop** to save `*.xdf`

### 4) Inspect the recorded XDF
```bash
python read_xdf_check.py path/to/recording.xdf
```
Example output:
```bash
Stream 0: BCI_Markers (Markers)  
samples: 9  
channels: 1  
Stream 1: Webcam_External (Video)  
samples: 711  
channels: 1  
Stream 2: Microphone (Audio)  
samples: 3131379  
channels: 1  
```
