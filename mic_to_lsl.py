# mic_to_lsl.py / 실행: python mic_to_lsl.py
import argparse, time
import sounddevice as sd
from pylsl import StreamInfo, StreamOutlet, local_clock

def main(dev=1, fs=44100, ch=1, block=256, name="Microphone", source_id=None):
    sd.query_devices()

    if source_id is None:
        source_id = f"mic_{int(time.time())}"

    info = StreamInfo(name, "Audio", ch, fs, "float32", source_id)
    outlet = StreamOutlet(info)  # 안정성↑: chunk_size 지정 안 함

    print(f"[START] dev={dev} fs={fs} ch={ch} block={block} sid='{source_id}'")

    def cb(indata, frames, time_info, status):
        if status:
            print("Audio status:", status)
        # 기준 타임스탬프 한 번만 읽고, 샘플마다 1/fs씩 증가
        ts = local_clock()
        if ch == 1:
            for v in indata[:, 0]:
                outlet.push_sample([float(v)], ts)
                ts += 1.0/fs
        else:
            for row in indata:
                outlet.push_sample(row.tolist(), ts)
                ts += 1.0/fs

    sd.check_input_settings(device=dev, channels=ch, samplerate=fs, dtype="float32")
    with sd.InputStream(device=dev, samplerate=fs, channels=ch, dtype="float32",
                        blocksize=block, callback=cb):
        try:
            print("streaming... Ctrl+C to stop")
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            print("\n[STOP]")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", type=int, default=1)
    ap.add_argument("--samplerate", type=int, default=44100)
    ap.add_argument("--channels", type=int, default=1)
    ap.add_argument("--blocksize", type=int, default=256)
    ap.add_argument("--name", type=str, default="Microphone")
    ap.add_argument("--source_id", type=str, default=None)  # 미지정 시 고유값 생성
    a = ap.parse_args()
    main(a.device, a.samplerate, a.channels, a.blocksize, a.name, a.source_id)
