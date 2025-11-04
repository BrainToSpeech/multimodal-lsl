# webcam_to_lsl.py / 실행: python webcam_to_lsl.py --index 0 --width 1280 --height 720 --fps 30 --name Webcam_External
import cv2, time, base64, argparse
from pylsl import StreamInfo, StreamOutlet, local_clock

def main(cam_index=0, width=640, height=480, fps=30, name='Webcam', source_id='webcam_01'):
    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)  # Windows에선 CAP_DSHOW가 카메라 선택 안정적
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS,          fps)

    if not cap.isOpened():
        raise RuntimeError(f"카메라를 열 수 없습니다 (index={cam_index}). 다른 인덱스를 시도해보세요.")

    # LSL 스트림 정보 (Video, 1채널, 문자열 전송)
    info = StreamInfo(name=name, type='Video', channel_count=1,
                      nominal_srate=fps, channel_format='string', source_id=source_id)
    outlet = StreamOutlet(info, chunk_size=1, max_buffered=360)

    print(f"[LSL] Video stream started → name='{name}', type='Video', fps={fps}, size={width}x{height}")
    print("종료: 창 포커스에서 'q' 키")

    # 송출 루프
    t_frame = time.time()
    interval = 1.0 / max(1, fps)
    while True:
        ok, frame = cap.read()
        if not ok:
            print("프레임을 읽지 못했습니다. 계속 시도합니다...")
            time.sleep(0.01)
            continue

        # JPEG 압축 (품질 80 정도)
        ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            continue

        # Base64로 문자열화 → LSL string 채널에 태움
        b64 = base64.b64encode(buf.tobytes()).decode('ascii')
        outlet.push_sample([b64], timestamp=local_clock())

        # 미리보기(옵션)
        cv2.imshow("Webcam Preview (LSL out)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # FPS 간격 맞추기(간단한 슬립)
        t_frame += interval
        sleep = t_frame - time.time()
        if sleep > 0:
            time.sleep(sleep)
        else:
            t_frame = time.time()

    cap.release()
    cv2.destroyAllWindows()
    print("[LSL] Video stream stopped.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=int, default=0, help="웹캠 장치 인덱스 (0,1,2...)")
    ap.add_argument("--width", type=int, default=640)
    ap.add_argument("--height", type=int, default=480)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--name", type=str, default="Webcam")
    ap.add_argument("--source_id", type=str, default="webcam_01")
    args = ap.parse_args()
    main(args.index, args.width, args.height, args.fps, args.name, args.source_id)
