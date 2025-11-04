# Multimodal LSL Mini-Suite

Minimal examples for streaming **microphone** and **webcam** to **Lab Streaming Layer (LSL)** and for quickly validating recorded **XDF** files.

## Repository Layout
.
├─ mic_to_lsl.py         # Microphone → LSL (Audio)
├─ webcam_to_lsl.py      # Webcam → LSL (Video)
├─ read_xdf_check.py     # Quick sanity check for XDF files
└─ requirements.txt      # Dependencies

## Stream Specs (Defaults)

- **Microphone**  
  `type="Audio"`, `channel_count=1` (sampling rate depends on OS/device)
- **Webcam_External**  
  `type="Video"`, `channel_count=1` (frame rate depends on device/codec)
- **BCI_Markers** *(optional, from a paradigm app)*  
  `type="Markers"`, single string channel (codes sent as strings)
