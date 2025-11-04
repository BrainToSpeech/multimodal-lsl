import pyxdf
from matplotlib import pyplot as plt
import base64, numpy as np, cv2
import sounddevice as sd

data, header = pyxdf.load_xdf("C:/Users/SeungHanKim/Documents/CurrentStudy/20251027_001.xdf")

print("Number of streams:", len(data))
for idx, stream in enumerate(data):
    name = stream['info']['name'][0]
    stype = stream['info']['type'][0]
    ts = stream['time_series']
    print(f"Stream {idx}: {name} ({stype})")
    print("  samples:", len(ts))
    if len(ts) > 0:
        print("  channels:", len(ts[0]))
    else:
        print("  channels: 0")

# ------------------ Check EEG data by plotting
eeg_stream = [s for s in data if s['info']['type'][0] == 'EEG'][0]

eeg_data = eeg_stream['time_series'].T
print(eeg_data.shape)
eeg_data_0 = eeg_data[0]
plt.plot(eeg_data_0[:30])
plt.show()

# ------------------ Check video data by reconsting into image
video_stream = [s for s in data if s['info']['type'][0] == 'Video'][0]

sample0 = video_stream['time_series'][0]
frame_str = sample0[0] if isinstance(sample0, (list, tuple)) else sample0

def _decode_bytes(s: str) -> bytes: # 1) 문자열 → 바이너리 복원 (base64 우선, 실패 시 hex로 시도)
    try:
        return base64.b64decode(s, validate=True)
    except Exception:
        return bytes.fromhex(s)

buf = _decode_bytes(frame_str)

arr = np.frombuffer(buf, dtype=np.uint8) # 2) 바이트 → numpy → OpenCV 이미지
img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
if img is None:
    raise ValueError("프레임 디코딩 실패: 전송 형식(base64/hex) 또는 프레임 내용 확인")

cv2.imshow("first frame", img) # 3) 화면에 보여주기
cv2.waitKey(0)
cv2.destroyAllWindows()

# ------------------ Check audio data by playing
audio_stream = [s for s in data if s['info']['type'][0] == 'Audio'][0]

audio_data = np.array(audio_stream['time_series'])
samplerate = int(float(audio_stream['info']['nominal_srate'][0]))

# 2초치 샘플만 추출
num_samples = samplerate * 2
snippet = audio_data[:num_samples]

print(f"재생할 데이터 shape: {snippet.shape}, samplerate: {samplerate}")

# 재생
sd.play(snippet, samplerate=samplerate)
sd.wait()