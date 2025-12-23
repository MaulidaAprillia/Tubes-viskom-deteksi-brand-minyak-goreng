Deteksi Brand Minyak Goreng Menggunakan YOLOv9
Link Presentasi di Youtube : https://youtu.be/6Zd9K7qnAzk 

Link Full Source Code Project (ZIP) berukuran 3.30GB di GDrive : https://drive.google.com/file/d/1KX_whFvwsmp1LTBCRgmOhF1RBukEahCo/view?usp=sharing 

Link File best.pt di Google Drive : https://drive.google.com/drive/folders/1kwQXT6pDLOb7fJ2Hs8Bhs2jRuCJ30Y43?usp=drive_link 

dataset/Deteksi Brand Minyak Goreng.v2i.yolov9/  <br>
Folder ini berisi dataset custom yang dibuat dan dilabeli/dianotasikan menggunakan Roboflow. <br>
Link Roboflow nya : https://app.roboflow.com/deteksi-minyak-goreng/deteksi-brand-minyak-goreng/models/deteksi-brand-minyak-goreng/2 

================Training Model===================== <br>
Framework: YOLOv9 (WongKinYiu) <br>
Metode: Transfer Learning <br>
File gelan-c.pt digunakan sebagai pretrained weight untuk transfer learning saat training. <br>
Output model: best.pt <br>
Contoh perintah training di jalankan di terminal vscode (dicatat di folder docs/): <br>
    python train.py --img 640 --batch 8 --epochs 30 --device 0 --data data.yaml --weights gelan-c.pt

==============Implementasi Deteksi Objek============= <br>
Model hasil training (best.pt) dapat digunakan untuk:<br>
Deteksi gambar <br>
Deteksi video <br>
Deteksi Webcam <br>
Script utama: 
train.py -> training model (bawaan YOLOv9 Wongkinyiu)
detect.py -> inference/deteksi (bawaan YOLOv9 Wongkinyiu)
Contoh perintah deteksi di jalankan di terminal vscode (dicatat di folder docs/):
1. Deteksi dengan Gambar :
python detect.py --weights runs/train/exp/weights/best.pt --source data/images/minyakbimo.jpeg --img 640 --conf 0.5 --device 0 --project data/image_hasil_deteksi_brand_minyak_goreng

2. Deteksi dengan video :
python detect.py --weights runs/train/exp/weights/best.pt --source data/videos/video6185831720420384357.mp4 --img 640 --conf 0.5 --device 0 --project data/video_hasil_deteksi_brand_minyak_goreng

3. Deteksi Webcam :
python detect.py --weights runs/train/exp/weights/best.pt --source 0 --img 640 --conf 0.5 --device 0 --project data/webcam_hasil_deteksi_brand_minyak_goreng


==============Aplikasi Web (Streamlit)=============== <br>
Aplikasi Streamlit dibuat untuk menjalankan inference melalui antarmuka web. <br>
Fitur: <br>
Upload gambar -> deteksi -> tampilkan hasil <br>
Upload video -> deteksi -> tampilkan hasil video <br>
Inference dijalankan di server (YOLOv9) <br>
script : app.py 

================Catatan========================== <br>
Folder docs/ <br>
Berisi catatan command yang dijalankan di terminal, sebagai bukti proses: 
- Training
- Testing / inference

File train.py, detect.py, dan val.py merupakan script bawaan YOLOv9 (WongKinYiu) dan digunakan tanpa modifikasi signifikan.
Proyek ini dijalankan secara lokal

file requirements.txt (bawaan WongKinYiu)

Daftar library Python yang dibutuhkan untuk menjalankan proyek



