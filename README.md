<h1 align="center"> Tugas Besar 1 IF2211 Strategi Algoritma</h1>
<h1 align="center">  Pemanfaatan Algoritma Greedy dalam Pembuatan Bot Permainan Diamonds </h1>

## Identitas Pengembang Program
### **Kelompok 7:  TheYuds**
|   NIM    |                  Nama                  |
| :------: | :------------------------------------: |
| 13522045 |            Elbert Chailes             |
| 13522115 |            Derwin Rustanly             |
| 10023634 |            Yudi Kurniawan             |

## Deskripsi Program
Diamonds merupakan suatu programming challenge yang mempertandingkan bot yang anda buat dengan bot dari para pemain lainnya. Setiap pemain akan memiliki sebuah bot dimana tujuan dari bot ini adalah mengumpulkan diamond sebanyak-banyaknya. Cara mengumpulkan diamond tersebut tidak akan sesederhana itu, tentunya akan terdapat berbagai rintangan yang akan membuat permainan ini menjadi lebih seru dan kompleks. Untuk memenangkan pertandingan, setiap pemain harus mengimplementasikan strategi tertentu pada masing-masing bot-nya.


Repositori ini berisi implementasi algoritma ***greedy by highest density*** dalam pembuatan bot permainan diamonds. ***Greedy by Highest Density*** adalah strategi greedy yang mengutamakan densitas tertinggi dari hasil pembagian poin yang didapatkan dari sebuah diamond dibagikan dengan perpindahan yang harus ditempuh untuk mendapatkan diamond tersebut.


## Requirements Program
1. **Game Engine**

    Requirement yang harus di-install: 

    - Node.js (https://nodejs.org/en) 
    - Docker desktop (https://www.docker.com/products/docker-desktop/) 
    - Yarn

        ```bash
        npm install --global yarn
        ```

2. **Bot Starter Pack**

    Requirement yang harus di-install
    - Python (https://www.python.org/downloads/) 


## Set Up dan Build Program
1. Jalankan game engine dengan cara mengunduh starter pack game engine dalam bentuk file .zip yang terdapat pada tautan berikut https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0

    a. Setelah melakukan instalasi, lakukan ekstraksi file .zip tersebut lalu masuk ke root folder dari hasil ekstraksi file tersebut kemudian jalankan terminal

    b. Jalankan perintah berikut pada terminal untuk masuk ke root directory dari game engine
    ```bash
    cd tubes1-IF2110-game-engine-1.1.0
    ```


    c. Lakukan instalasi dependencies dengan menggunakan yarn. 
    ``` bash
    yarn
    ```


    d. Lakukan setup environment variable dengan menjalankan script berikut untuk OS Windows
    ```bash
    ./scripts/copy-env.bat
    ```

	Untuk Linux / (possibly) macOS
    ```bash
    chmod +x ./scripts/copy-env.sh
    ./scripts/copy-env.sh
    ```    



    e. Lakukan setup local database dengan membuka aplikasi docker desktop terlebih dahulu kemudian jalankan perintah berikut di terminal
    ```bash
    docker compose up -d database
    ```

    f. Kemudian jalankan script berikut. Untuk Windows
    ```bash
    ./scripts/setup-db-prisma.bat
    ```

    Untuk Linux / (possibly) macOS
    ```bash
    chmod +x ./scripts/setup-db-prisma.sh
    ./scripts/setup-db-prisma.sh
    ```

    g. Jalankan perintah berikut untuk melakukan build frontend dari game-engine
    ```bash
    npm run build
    ```

    h. Jalankan perintah berikut untuk memulai game-engine
    ```bash
    npm run start
    ```

    i. Jika berhasil, tampilan terminal akan terlihat seperti gambar di bawah ini.
    ![gameenginesuccess](img/enginesuccess.png)


2. Jalankan bot starter pack dengan cara mengunduh kit dengan ekstensi .zip yang terdapat pada tautan berikut

     https://github.com/haziqam/tubes1-IF2211-bot-starter-pack/releases/tag/v1.0.1 

    a. Lakukan ekstraksi file zip tersebut, kemudian masuk ke folder hasil ekstrak tersebut dan buka terminal
    b. Jalankan perintah berikut untuk masuk ke root directory dari project
    ```bash
    cd tubes1-IF2110-bot-starter-pack-1.0.1
    ```
    c. Jalankan perintah berikut untuk menginstall dependencies dengan menggunakan pip
    ```bash
    pip install -r requirements.txt
    ```


    d. Jalankan program dengan cara menjalankan perintah berikuts. 
    ``` bash
    python main.py --logic HighestDensity --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```

    e. Anda juga bisa menjalankan satu bot saja atau beberapa bot menggunakan .bat atau .sh script.
    Untuk windows
    ```
    ./run-bots.bat
    ```

    Untuk Linux / (possibly) macOS
    ```
    ./run-bots.sh
    ```

## Dokumentasi Program
![ss1](img/ss1.png)
![ss2](img/ss2.png)

