# Traveler Ship Company

Bu proje **Gezgin Gemi Şirketi** ile ilgili verileri yönetmek için bir **Veritabanı Yönetim Sistemi (DBMS)** geliştirmeyi amaçlamaktadır. Sistem, gemiler, seferler, kaptanlar, mürettebat ve limanlarla ilgili bilgileri depolamak ve yönetmek için bir **SQL Server veritabanı** kullanmaktadır. Kullanıcılar, verileri bir **grafiksel kullanıcı arayüzü (GUI)** üzerinden ekleyebilir, silebilir ve güncelleyebilir.
- **Yapılış Tarihi:** 5 Mayıs 2024  
- **Son Güncelleme:** 7 Şubat 2025  

---

## 📌 Proje Özellikleri
- **Gemilerin Yönetimi** 🛳️
- **Kaptanların Yönetimi** 🧑‍✈️
- **Mürettebatın Yönetimi** 👨‍👩‍👦‍👦
- **Limanların Yönetimi** ⚓
- **Seferlerin Yönetimi** ⛴️
- **Veritabanı Yönetimi** 📊

---

## 📂 Kullanılan Teknolojiler
- **Python** 🐍 
- **Tkinter** 🎨 (GUI oluşturmak için)
- **Pyodbc** 🔗 (SQL Server bağlantısı için)
- **SQL Server** 🗃️ (Veritabanı yönetimi için)
- **Datetime Modülü** 🕒 (Sefer ve mürettebat yönetimi için)

---

## 🔧 Kurulum
### 1️⃣ Gereksinimler
Projenin çalıştırılabilmesi için aşağıdaki bileşenlerin sisteminizde yüklü olması gerekmektedir:
- ```Python 3.x```
- ```SQL Server```
- Gerekli Python modülleri:
  ```bash
  pip install pyodbc
  ```

### 2️⃣ Veritabanı Bağlantısını Ayarlama
1. SQL Server'da **GezginGemiDB** adlı bir veritabanı oluşturun.
2. **Veritabanı tablolarını oluşturmak için** ilgili **SQL dosyasını(Traveler_Ship_Company_DB)** çalıştırın.
3. `baglan()` fonksiyonundaki **veritabanı bağlantı bilgilerini** kendi sisteminize göre güncelleyin.

### 3️⃣ Projeyi Çalıştırma
Aşağıdaki komutu terminalde çalıştırarak GUI uygulamasını başlatabilirsiniz:
```bash
python main.py
```

---

## 🎮 Kullanım
- **Gemiler Menüsü**: Gemileri ekleme, düzenleme, silme.
- **Kaptanlar Menüsü**: Kaptan bilgilerini yönetme.
- **Mürettebatlar Menüsü**: Mürettebat ekleme ve silme.
- **Limanlar Menüsü**: Limanlarla ilgili bilgileri görüntüleme ve düzenleme.
- **Seferler Menüsü**: Yeni sefer oluşturma, düzenleme, silme.

## 🖥️ Proje Arayüzü

### Gemiler Menüsü
![Image](https://github.com/user-attachments/assets/b8207e02-83e2-4bf2-8d25-f4747a3c3ca4)

### Kaptanlar Menüsü
![Image](https://github.com/user-attachments/assets/ec119814-3b4e-4e7f-a546-f6e5e44abe2e)

### Mürettebatlar Menüsü
![Image](https://github.com/user-attachments/assets/5bfd0ef1-a5d4-4f2a-8be4-98550adc24af)

### Limanlar Menüsü
![Image](https://github.com/user-attachments/assets/2c739bec-f0b0-406f-826d-71628a18663f)

### Seferler Menüsü
![Image](https://github.com/user-attachments/assets/487758a3-2dd6-466f-b969-79cc763c7dd9)
