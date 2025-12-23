import streamlit as st
import subprocess
import os
import sys
from PIL import Image

# =========================
# KONFIGURASI PATH
# =========================
YOLO_PATH = r"D:\DeteksiBrandMinyakGoreng\yolov9"
WEIGHTS = "runs/train/exp/weights/best.pt"

IMAGE_INPUT_DIR = os.path.join(YOLO_PATH, "data", "images")
VIDEO_INPUT_DIR = os.path.join(YOLO_PATH, "data", "videos")
OUTPUT_DIR = os.path.join(YOLO_PATH, "data", "outputs_streamlit")

os.makedirs(IMAGE_INPUT_DIR, exist_ok=True)
os.makedirs(VIDEO_INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# UI
# =========================
st.set_page_config(
    page_title="Deteksi Brand Minyak Goreng (YOLOv9)",
    layout="wide"
    
)

st.title("Deteksi Brand Minyak Goreng (YOLOv9)")
st.caption("Inference dijalankan di server menggunakan YOLOv9")

menu = st.sidebar.selectbox(
    "Pilih Mode Deteksi",
    ["Gambar", "Video"]
)

# =========================
# FUNGSI BANTU
# =========================
def find_result_video(folder):
    for f in os.listdir(folder):
        if f.lower().endswith(".mp4"):
            return os.path.join(folder, f)
    return None


def convert_to_web_mp4(input_video, output_video):
    """Convert video YOLO ke MP4 H.264 agar bisa diputar di browser"""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_video
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# =========================
# DETEKSI GAMBAR
# =========================
if menu == "Gambar":
    uploaded_file = st.file_uploader(
        "Upload Gambar",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file:
        input_path = os.path.join(IMAGE_INPUT_DIR, uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        st.image(Image.open(input_path), caption="Gambar Input", use_container_width=True)

        if st.button("Deteksi Gambar"):
            with st.spinner("🔍 Mendeteksi gambar..."):
                result_dir = os.path.join(OUTPUT_DIR, "images")

                cmd = [
                    sys.executable, "detect.py",
                    "--weights", WEIGHTS,
                    "--source", input_path,
                    "--img", "640",
                    "--conf", "0.5",
                    "--device", "0",
                    "--project", result_dir,
                    "--name", "result",
                    "--exist-ok"
                ]

                subprocess.run(cmd, cwd=YOLO_PATH)

            output_img = os.path.join(result_dir, "result", uploaded_file.name)

            if os.path.exists(output_img):
                st.success("Deteksi selesai")
                st.image(output_img, caption="Hasil Deteksi", use_container_width=True)
            else:
                st.error("Hasil gambar tidak ditemukan.")

# =========================
# DETEKSI VIDEO
# =========================
elif menu == "Video":
    uploaded_video = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov"]
    )

    if uploaded_video:
        input_path = os.path.join(VIDEO_INPUT_DIR, uploaded_video.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_video.read())

        st.subheader("Video Input")
        st.video(input_path)

        if st.button("Deteksi Video"):
            with st.spinner("Mendeteksi video (proses ini memakan waktu)..."):
                result_dir = os.path.join(OUTPUT_DIR, "videos")

                cmd = [
                    sys.executable, "detect.py",
                    "--weights", WEIGHTS,
                    "--source", input_path,
                    "--img", "640",
                    "--conf", "0.5",
                    "--device", "0",
                    "--project", result_dir,
                    "--name", "result",
                    "--exist-ok"
                ]

                subprocess.run(cmd, cwd=YOLO_PATH)

                raw_video = find_result_video(os.path.join(result_dir, "result"))
                web_video = os.path.join(result_dir, "result", "web_result.mp4")

                if raw_video:
                    convert_to_web_mp4(raw_video, web_video)

            if os.path.exists(web_video):
                st.success("Deteksi video selesai")
                st.video(web_video)
            else:
                st.error("Video hasil deteksi tidak ditemukan.")
