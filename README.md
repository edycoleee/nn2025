
### SERVER UBUNTU
```txt

```
### GITHUB

```txt
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edycoleee/nn2025.git
git push -u origin main
```

### REQUIREMENT
```py
# 1. Membuat Virtual Environtment
python3 -m venv venv
source venv/bin/activate  #Linux / Macbook
venv\Scripts\activate # Windows

#2. Install library
pip install matplotlib numpy
pip install seaborn
pip install scikit-learn
pip install tensorflow
pip install flask
```

# RAPBERYY PI 5

```py
sudo apt update
sudo apt upgrade -y

sudo apt install -y build-essential libssl-dev zlib1g-dev \
libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev \
tk-dev libffi-dev wget

cd /usr/src
sudo wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
sudo tar xzf Python-3.10.14.tgz
cd Python-3.10.14
sudo ./configure --enable-optimizations
sudo make -j4
sudo make altinstall

python3.10 --version

python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip

pip install tensorflow==2.13.0


python3 -c "import tensorflow as tf; print(tf.__version__)"
```

# GPU RTX 2060 Anda di laptop Asus ROG

install python versi 3.10

```
Cara Menginstal cuDNN (Zip Method)
Asumsi: Anda telah menginstal CUDA Toolkit 11.2 di lokasi default Windows, yaitu:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\
Langkah 1: Ekstrak File ZIP cuDNN
Temukan file ZIP cuDNN yang baru saja Anda unduh (misalnya, cudnn-windows-x86_64-8.1.0.27_cuda11.2-archive.zip).
Klik kanan pada file ZIP tersebut, lalu pilih Extract All... atau gunakan software seperti 7-Zip/WinRAR untuk mengekstrak isinya.
Setelah diekstrak, Anda akan mendapatkan sebuah folder baru dengan nama yang sama, dan di dalamnya terdapat tiga sub-folder utama:
- bin
- include
- lib
Langkah 2: Salin File ke Direktori CUDA
Sekarang, Anda perlu menyalin konten dari folder yang diekstrak tadi ke folder instalasi CUDA Anda.
Buka folder hasil ekstraksi cuDNN tadi.
Buka jendela File Explorer baru, dan navigasikan ke lokasi instalasi CUDA:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\
Salin konten:
Buka folder bin di folder cuDNN yang diekstrak. Salin semua file DLL di dalamnya.
Rekatkan (Paste) file-file tersebut ke dalam folder bin di direktori CUDA (C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin).
Lakukan hal yang sama untuk folder include dan lib.
Singkatnya, Anda memastikan bahwa file-file berikut berada di tempat yang benar:
File cuDNN	Lokasi Tujuan
...ekstrak...\bin\*.*	C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin
...ekstrak...\include\*.*	C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\include
...ekstrak...\lib\*.*	C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\lib
```
```cmd
py -3.10 --version

py -3.10 -m venv tf_gpu_env

.\tf_gpu_env\Scripts\activate
python --version 

python.exe -m pip install --upgrade pip
pip install tensorflow==2.10.0
pip install "numpy<2"
```
```
1. Verifikasi Ulang Pengaturan Path
Tekan tombol Windows + S, ketik "environment variables", dan buka "Edit the system environment variables".
Klik Environment Variables....
Di bagian System variables (bukan User variables), cari dan pilih Path, lalu klik Edit....
Pastikan dua jalur (path) berikut persis ada di daftar tersebut:

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\libnvvp

Restart Komputer Anda
```

```py
import tensorflow as tf
print(tf.__version__)
print(tf.test.is_gpu_available())


import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

```

```py
import tensorflow as tf

# Pastikan TensorFlow menggunakan GPU secara default
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please check your GPU setup, the default device is not set.")

# Contoh sederhana operasi di GPU
with tf.device('/GPU:0'):
    a = tf.constant([1.0, 2.0, 3.0], shape=[3], name='a')
    b = tf.constant([4.0, 5.0, 6.0], shape=[3], name='b')
    c = a + b

print(c)
```

### CIFAR

Dataset CIFAR adalah kumpulan gambar berwarna berukuran 32x32 piksel yang umum digunakan untuk melatih model deep learning klasifikasi gambar. Versi yang paling populer adalah CIFAR-10, yang berisi 60.000 gambar dalam 10 kelas objek yang berbeda (pesawat, mobil, burung, kucing, rusa, anjing, katak, kuda, kapal, dan truk). Versi lain, CIFAR-100, memiliki 100 kelas objek. 

Install REACT VITE

- 🔹Pakai nvm (Node Version Manager)
- Node 18 tetap ada, tapi kamu bisa switch ke Node 20 atau 22 saat butuh.

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# Install Node.js versi 20 LTS
nvm install 20
nvm use 20

# Cek versi aktif
node -v

#Kalau mau default ke Node 20:
nvm alias default 20

```

- Step-by-step React + Vite sederhana

Buat project baru dengan Vite

```bash
npm create vite@latest my-app
```
Pilih framework: React

Pilih variant: JavaScript atau TypeScript sesuai kebutuhan.

Masuk ke folder project
```bash
cd my-app
```
Install dependencies
```bash
npm install
```
Jalankan server development
```bash
npm run dev
```
Default akan jalan di http://localhost:5173


- 📂 Struktur Project dengan Docker
```
cifar-project/
│
├── backend/
│   ├── app.py
│   ├── utils/preprocess.py
│   ├── model/cifar_model.h5
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/...
│   ├── package.json
│   └── Dockerfile
│
└── docker-compose.yml
```