import pyodbc
import tkinter as tk
from tkinter import ttk
from datetime import datetime


# Veritabanına bağlanma fonksiyonu
def baglan():
    server = 'DESKTOP-5QE6TBQ\SQLEXPRESS'
    database = 'GezginGemiSirketi'
    driver= '{SQL Server}'

    # Bağlantıyı kur
    conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database)
    return conn

class Gemi:
    def __init__(self, adi, agirlik, yapim_yili, tip, kapasite, maksimum_agirlik):
        self.id = id
        self.adi = adi
        self.agirlik = agirlik
        self.yapim_yili = yapim_yili
        self.tip = tip
        self.kapasite = kapasite
        self.maksimum_agirlik = maksimum_agirlik

    def veritabanina_ekle(self):
        conn = baglan()
        cursor = conn.cursor() 

        # Gemi tipine göre ilgili sütunu belirle
        if self.tip == "Yolcu Gemisi":
            sutun = "YolcuKapasitesi"
        elif self.tip == "Petrol Tankeri":
            sutun = "PetrolKapasitesi"
        elif self.tip == "Konteyner Gemisi":
            sutun = "KonteynerSayısı"
        else:
            sutun = None

        if sutun:
            # Gemi tablosuna yeni kayıt ekle
            cursor.execute("INSERT INTO Gemiler (Adı, Ağırlık, YapımYılı, Tip, {}, MaksimumAğırlık) VALUES (?, ?, ?, ?, ?, ?)".format(sutun),(self.adi, self.agirlik, self.yapim_yili, self.tip, self.kapasite, self.maksimum_agirlik))
            conn.commit()
        else:
            print("Geçersiz gemi tipi.")

        conn.close()   #Veritabanı bağlantısını keser

class Kaptan:
    def __init__(self, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans):
        self.ad = ad
        self.soyad = soyad
        self.adres = adres
        self.vatandaslik = vatandaslik
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi
        self.lisans = lisans

    def veritabanina_ekle(self):
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Kaptanlar (Ad, Soyad, Adres, Vatandaşlık, DoğumTarihi, İşeGirişTarihi, Lisans) VALUES (?, ?, ?, ?, ?, ?, ?)",(self.ad, self.soyad, self.adres, self.vatandaslik, self.dogum_tarihi, self.ise_giris_tarihi, self.lisans))
        conn.commit()
        conn.close()

class Mürettebat:
    def __init__(self, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, gorev):
        self.ad = ad
        self.soyad = soyad
        self.adres = adres
        self.vatandaslik = vatandaslik
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi
        self.gorev = gorev

    def veritabanina_ekle(self):
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Mürettebatlar (Ad, Soyad, Adres, Vatandaşlık, DoğumTarihi, İşeGirişTarihi, Görev) VALUES (?, ?, ?, ?, ?, ?, ?)",(self.ad, self.soyad, self.adres, self.vatandaslik, self.dogum_tarihi, self.ise_giris_tarihi, self.gorev))
        conn.commit()   #Veritabanında yapılan değişiklikleri kalıcı hale getirmek için kullanılır. 
        conn.close()

class Liman:
    def __init__(self, adi, ulke, nufus, pasaport_gerekli, demirleme_ucreti, ziyaret_edildi):
        self.adi = adi
        self.ulke = ulke
        self.nufus = nufus
        self.pasaport_gerekli = pasaport_gerekli
        self.demirleme_ucreti = demirleme_ucreti
        self.ziyaret_edildi = ziyaret_edildi

    def veritabanina_ekle(self):
        conn = baglan()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Limanlar (LimanAdı, Ülke, Nüfus, PasaportGerekli, DemirlemeÜcreti, ZiyaretEdildi) VALUES (?, ?, ?, ?, ?, ?)",(self.adi, self.ulke, self.nufus, self.pasaport_gerekli, self.demirleme_ucreti, self.ziyaret_edildi))
        conn.commit()
        conn.close()

class Sefer:
    def __init__(self, gemi_id, kaptan_ids, murettebat_id, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani, limanlar):
        self.gemi_id = gemi_id
        self.kaptan_ids = kaptan_ids
        self.murettebat_id = murettebat_id
        self.yola_cikis_tarihi = yola_cikis_tarihi
        self.donus_tarihi = donus_tarihi
        self.yola_cikis_limani = yola_cikis_limani
        self.limanlar = limanlar

    def sefer_turunu_al(self):
        bugun = datetime.today().date()
        yola_cikis_tarihi_datetime = datetime.strptime(self.yola_cikis_tarihi, "%Y-%m-%d").date()

        if yola_cikis_tarihi_datetime < bugun:
            return "Geçmiş Sefer"
        elif yola_cikis_tarihi_datetime > bugun:
            return "Gelecek Sefer"
        else:
            return "Olası Sefer"

    def veritabanina_ekle(self, sefer_id, kaptan_ids, sefer_turu):
        conn = baglan()
        cursor = conn.cursor()

        # SeferID parametresini kullanarak Seferler tablosuna değerleri ekle
        cursor.execute(
            "INSERT INTO Seferler (SeferID, GemiID, MürettebatID, YolaÇıkışTarihi, DönüşTarihi, YolaÇıkışLimanı, Limanlar, SeferTürü) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (sefer_id, self.gemi_id, self.murettebat_id, self.yola_cikis_tarihi, self.donus_tarihi, self.yola_cikis_limani, self.limanlar, sefer_turu))

        # Sefer-Kaptan ilişkilerini eklemek için her bir kaptan ID'si için ayrı bir kayıt ekle
        for kaptan_id in kaptan_ids:
            cursor.execute("INSERT INTO Sefer_Kaptan (SeferID, KaptanID) VALUES (?, ?)", (sefer_id, kaptan_id))

        conn.commit()
        conn.close()



# Gemiler sekmesi içeriği oluşturma fonksiyonu
def gemiler_formu(tab):
    # Gemiler sekmesi içeriği
    gemiler_frame = ttk.Frame(tab)  
    gemiler_frame.pack(fill="both", expand=True)  

    # Gemiler form alanları
    gemi_adi_label = ttk.Label(gemiler_frame, text="Gemi Adı:")
    gemi_adi_label.grid(column=0, row=0, pady=(15,0))
    gemi_adi_entry = ttk.Entry(gemiler_frame)
    gemi_adi_entry.grid(column=1, row=0, padx=(0, 50), pady=(15,0))

    gemi_agirlik_label = ttk.Label(gemiler_frame, text="Ağırlık:")
    gemi_agirlik_label.grid(column=0, row=1)  
    gemi_agirlik_entry = ttk.Entry(gemiler_frame)  
    gemi_agirlik_entry.grid(column=1, row=1, padx=(0, 50)) 

    gemi_yapim_yili_label = ttk.Label(gemiler_frame, text="Yapım Yılı:")
    gemi_yapim_yili_label.grid(column=0, row=2)
    gemi_yapim_yili_entry = ttk.Entry(gemiler_frame)
    gemi_yapim_yili_entry.grid(column=1, row=2, padx=(0, 50))

    gemi_tip_label = ttk.Label(gemiler_frame, text="Tip:")
    gemi_tip_label.grid(column=0, row=3)
    gemi_tip_combobox = ttk.Combobox(gemiler_frame, values=["Yolcu Gemisi", "Petrol Tankeri", "Konteyner Gemisi"])  
    gemi_tip_combobox.grid(column=1, row=3, padx=(0, 50))  

    gemi_kapasite_label = ttk.Label(gemiler_frame, text="Kapasite:")
    gemi_kapasite_label.grid(column=0, row=4)
    gemi_kapasite_entry = ttk.Entry(gemiler_frame)
    gemi_kapasite_entry.grid(column=1, row=4, padx=(0, 50))

    gemi_maksimum_agirlik_label = ttk.Label(gemiler_frame, text="Maksimum Ağırlık:")
    gemi_maksimum_agirlik_label.grid(column=0, row=5, padx=(30,30))
    gemi_maksimum_agirlik_entry = ttk.Entry(gemiler_frame)
    gemi_maksimum_agirlik_entry.grid(column=1, row=5, padx=(0, 50))

    gemi_id_label = ttk.Label(gemiler_frame, text="Gemi ID:")
    gemi_id_label.grid(column=2, row=1)
    gemi_id_entry = ttk.Entry(gemiler_frame)
    gemi_id_entry.grid(column=3, row=1, padx=(0, 50))

    gemi_adi2_label = ttk.Label(gemiler_frame, text="Gemi Adı:")
    gemi_adi2_label.grid(column=2, row=2)
    gemi_adi2_entry = ttk.Entry(gemiler_frame)
    gemi_adi2_entry.grid(column=3, row=2, padx=(0, 50))

    gemi_id2_label = ttk.Label(gemiler_frame, text="Gemi ID:")
    gemi_id2_label.grid(column=4, row=1)
    gemi_id2_entry = ttk.Entry(gemiler_frame)
    gemi_id2_entry.grid(column=5, row=1, padx=(0, 50))

    sutun_adi_label = ttk.Label(gemiler_frame, text="Düzenlenecek Sütun:")
    sutun_adi_label.grid(column=4, row=2)
    sutun_adi_entry = ttk.Entry(gemiler_frame)
    sutun_adi_entry.grid(column=5, row=2, padx=(0, 50))

    yeni_veri_label = ttk.Label(gemiler_frame, text="Yeni Veri:")
    yeni_veri_label.grid(column=4, row=3)
    yeni_veri_entry = ttk.Entry(gemiler_frame)
    yeni_veri_entry.grid(column=5, row=3, padx=(0, 50))


    def tip_secildi(event):
        secilen_tip = gemi_tip_combobox.get()
        if secilen_tip == "Yolcu Gemisi":
            gemi_kapasite_label.config(text="Yolcu Kapasitesi:")  #config() yöntemi, bir Tkinter bileşeninin (widget) özelliklerini (örneğin, metin, renk, boyut, vs.) güncellemek için kullanılır. 
        elif secilen_tip == "Petrol Tankeri":
            gemi_kapasite_label.config(text="Petrol Kapasitesi:")
        elif secilen_tip == "Konteyner Gemisi":
            gemi_kapasite_label.config(text="Konteyner Sayısı:")

    gemi_tip_combobox.bind("<<ComboboxSelected>>", tip_secildi)  

    def yeni_gemi_ekle():
        gemi_adi = gemi_adi_entry.get()
        gemi_agirlik = gemi_agirlik_entry.get()
        gemi_yapim_yili = gemi_yapim_yili_entry.get()
        gemi_tip = gemi_tip_combobox.get()
        gemi_kapasite = gemi_kapasite_entry.get()
        gemi_maksimum_agirlik = gemi_maksimum_agirlik_entry.get()

        if gemi_adi and gemi_agirlik and gemi_yapim_yili and gemi_tip and gemi_kapasite and gemi_maksimum_agirlik:
            gemi = Gemi(gemi_adi, gemi_agirlik, gemi_yapim_yili, gemi_tip, gemi_kapasite, gemi_maksimum_agirlik)
            gemi.veritabanina_ekle()
            print("Yeni gemi eklendi:", gemi_adi)
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(gemiler_frame, text="Yeni Gemi Ekle", command=yeni_gemi_ekle)
    ekle_button.grid(column=0, row=6, columnspan=2)


    def gemi_verisini_sil():
        gemi_id = gemi_id_entry.get()
        gemi_adi = gemi_adi2_entry.get()

        if gemi_id and gemi_adi:
            conn = baglan()
            cursor = conn.cursor()

            # Geminin varlığını kontrol et
            cursor.execute("SELECT COUNT(*) FROM Gemiler WHERE ID = ?", (gemi_id,))
            gemi_count = cursor.fetchone()[0]

            if gemi_count == 1:
                # Gemi adını kontrol et
                cursor.execute("SELECT Adı FROM Gemiler WHERE ID = ?", (gemi_id,))
                gemi_adi_veri = cursor.fetchone()[0]

                if gemi_adi_veri == gemi_adi:
                    # Kullanıcıdan gelen veriyi kullanarak sorguyu oluştur
                    sorgu = "DELETE FROM Gemiler WHERE ID = ?"
                    # Gemi verisini sil
                    cursor.execute(sorgu, (gemi_id,))
                    # Değişiklikleri kaydet
                    conn.commit()
                    # İşlem başarılı mesajını yazdır
                    print(f"{gemi_adi} isimli gemi başarıyla silindi.")
                else:
                    print("Girilen ad ile tablodaki ad verisi uyuşmuyor!")
            else:
                print("Belirtilen gemi bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")


    ekle_button = ttk.Button(gemiler_frame, text="Gemi Verisini Sil", command=gemi_verisini_sil)
    ekle_button.grid(column=1, row=3, columnspan=4)


    def gemi_verisini_duzenle():
        gemi_id2 = gemi_id2_entry.get()
        sutun_adi = sutun_adi_entry.get()
        yeni_veri = yeni_veri_entry.get()

        if gemi_id2 and sutun_adi and yeni_veri:
            conn = baglan()
            cursor = conn.cursor()

            # Geminin varlığını kontrol et
            cursor.execute("SELECT COUNT(*) FROM Gemiler WHERE ID = ?", (gemi_id2,))
            gemi_count = cursor.fetchone()[0]

            if gemi_count == 1:
                # Sorguyu oluştur ve veriyi güncelle
                sorgu = f"UPDATE Gemiler SET {sutun_adi} = ? WHERE ID = ?"
                cursor.execute(sorgu, (yeni_veri, gemi_id2))
                conn.commit()
                print(f"Gemi verisi başarıyla güncellendi.")
            else:
                print("Belirtilen gemi bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(gemiler_frame, text="Gemi Verisini Düzenle", command=gemi_verisini_duzenle)
    ekle_button.grid(column=4, row=4, columnspan=4)


def kaptan_formu(tab):
    # Kaptanlar sekmesi içeriği
    kaptanlar_frame = ttk.Frame(tab)
    kaptanlar_frame.pack(fill="both", expand=True)

    # Kaptanlar form alanları
    kaptan_adi_label = ttk.Label(kaptanlar_frame, text="Adı:")
    kaptan_adi_label.grid(column=0, row=0, pady=(15,0))
    kaptan_adi_entry = ttk.Entry(kaptanlar_frame)
    kaptan_adi_entry.grid(column=1, row=0, padx=(0, 50), pady=(15,0))

    kaptan_soyadi_label = ttk.Label(kaptanlar_frame, text="Soyadı:")
    kaptan_soyadi_label.grid(column=0, row=1)
    kaptan_soyadi_entry = ttk.Entry(kaptanlar_frame)
    kaptan_soyadi_entry.grid(column=1, row=1, padx=(0, 50))

    kaptan_adresi_label = ttk.Label(kaptanlar_frame, text="Adres:")
    kaptan_adresi_label.grid(column=0, row=2)
    kaptan_adresi_entry = ttk.Entry(kaptanlar_frame)
    kaptan_adresi_entry.grid(column=1, row=2, padx=(0, 50))

    kaptan_vatandaslik_label = ttk.Label(kaptanlar_frame, text="Vatandaşlık:")
    kaptan_vatandaslik_label.grid(column=0, row=3)
    kaptan_vatandaslik_entry = ttk.Entry(kaptanlar_frame)
    kaptan_vatandaslik_entry.grid(column=1, row=3, padx=(0, 50))

    kaptan_dogum_tarihi_label = ttk.Label(kaptanlar_frame, text="Doğum Tarihi (YYYY-MM-DD):")
    kaptan_dogum_tarihi_label.grid(column=0, row=4, padx=(30,30))
    kaptan_dogum_tarihi_entry = ttk.Entry(kaptanlar_frame)
    kaptan_dogum_tarihi_entry.grid(column=1, row=4, padx=(0, 50))

    kaptan_ise_giris_tarihi_label = ttk.Label(kaptanlar_frame, text="İşe Giriş Tarihi (YYYY-MM-DD):")
    kaptan_ise_giris_tarihi_label.grid(column=0, row=5, padx=(30,30))
    kaptan_ise_giris_tarihi_entry = ttk.Entry(kaptanlar_frame)
    kaptan_ise_giris_tarihi_entry.grid(column=1, row=5, padx=(0, 50))

    kaptan_lisans_label = ttk.Label(kaptanlar_frame, text="Lisans:")
    kaptan_lisans_label.grid(column=0, row=6)
    kaptan_lisans_entry = ttk.Entry(kaptanlar_frame)
    kaptan_lisans_entry.grid(column=1, row=6, padx=(0, 50))

    kaptan_id_label = ttk.Label(kaptanlar_frame, text="Kaptan ID:")
    kaptan_id_label.grid(column=2, row=2)
    kaptan_id_entry = ttk.Entry(kaptanlar_frame)
    kaptan_id_entry.grid(column=3, row=2, padx=(0, 50))

    kaptan_adi2_label = ttk.Label(kaptanlar_frame, text="Kaptan Adı:")
    kaptan_adi2_label.grid(column=2, row=3)
    kaptan_adi2_entry = ttk.Entry(kaptanlar_frame)
    kaptan_adi2_entry.grid(column=3, row=3, padx=(0, 50))

    kaptan_id2_label = ttk.Label(kaptanlar_frame, text="Kaptan ID:")
    kaptan_id2_label.grid(column=4, row=1)
    kaptan_id2_entry = ttk.Entry(kaptanlar_frame)
    kaptan_id2_entry.grid(column=5, row=1, padx=(0, 50))

    sutun_adi_label = ttk.Label(kaptanlar_frame, text="Düzenlenecek Sütun:")
    sutun_adi_label.grid(column=4, row=2)
    sutun_adi_entry = ttk.Entry(kaptanlar_frame)
    sutun_adi_entry.grid(column=5, row=2, padx=(0, 50))

    yeni_veri_label = ttk.Label(kaptanlar_frame, text="Yeni Veri:")
    yeni_veri_label.grid(column=4, row=3)
    yeni_veri_entry = ttk.Entry(kaptanlar_frame)
    yeni_veri_entry.grid(column=5, row=3, padx=(0, 50))

    # Yeni kaptan ekleme düğmesi
    def yeni_kaptan_ekle():
        kaptan_adi = kaptan_adi_entry.get()
        kaptan_soyadi = kaptan_soyadi_entry.get()
        kaptan_adresi = kaptan_adresi_entry.get()
        kaptan_vatandaslik = kaptan_vatandaslik_entry.get()
        kaptan_dogum_tarihi = kaptan_dogum_tarihi_entry.get()
        kaptan_ise_giris_tarihi = kaptan_ise_giris_tarihi_entry.get()
        kaptan_lisans = kaptan_lisans_entry.get()

        if kaptan_adi and kaptan_soyadi and kaptan_adresi and kaptan_vatandaslik and kaptan_dogum_tarihi and kaptan_ise_giris_tarihi and kaptan_lisans:
            kaptan=Kaptan(kaptan_adi, kaptan_soyadi, kaptan_adresi, kaptan_vatandaslik, kaptan_dogum_tarihi,kaptan_ise_giris_tarihi, kaptan_lisans)
            kaptan.veritabanina_ekle()
            print("Yeni kaptan eklendi:", kaptan_adi, kaptan_soyadi)
        else:
            print("Tüm kaptan bilgileri doldurulmalıdır.")

    ekle_button = ttk.Button(kaptanlar_frame, text="Yeni Kaptan Ekle", command=yeni_kaptan_ekle)
    ekle_button.grid(column=0, row=7, columnspan=2)


    def kaptan_verisini_sil():
        kaptan_id = kaptan_id_entry.get()
        kaptan_adi = kaptan_adi2_entry.get()

        if kaptan_id and kaptan_adi:
            conn = baglan()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Kaptanlar WHERE ID = ?", (kaptan_id,))
            kaptan_count = cursor.fetchone()[0]

            if kaptan_count == 1:
                cursor.execute("SELECT Ad FROM Kaptanlar WHERE ID = ?", (kaptan_id,))
                kaptan_adi_veri = cursor.fetchone()[0]

                if kaptan_adi_veri == kaptan_adi:
                    cursor.execute("DELETE FROM Kaptanlar WHERE ID = ?", (kaptan_id,))
                    conn.commit()
                    print(f"{kaptan_adi} isimli kaptan başarıyla silindi.")
                else:
                    print("Girilen ad ile tablodaki ad verisi uyuşmuyor!")
            else:
                print("Belirtilen kaptan bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(kaptanlar_frame, text="Kaptan Verisini Sil", command=kaptan_verisini_sil)
    ekle_button.grid(column=1, row=4, columnspan=4)


    def kaptan_verisini_duzenle():
        kaptan_id2 = kaptan_id2_entry.get()
        sutun_adi = sutun_adi_entry.get()
        yeni_veri = yeni_veri_entry.get()

        if kaptan_id2 and sutun_adi and yeni_veri:
            conn = baglan()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Kaptanlar WHERE ID = ?", (kaptan_id2,))
            gemi_count = cursor.fetchone()[0]

            if gemi_count == 1:
                sorgu = f"UPDATE Kaptanlar SET {sutun_adi} = ? WHERE ID = ?"
                cursor.execute(sorgu, (yeni_veri, kaptan_id2))
                conn.commit()
                print(f"Kaptan verisi başarıyla güncellendi.")
            else:
                print("Belirtilen gemi bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(kaptanlar_frame, text="Kaptan Verisini Düzenle", command=kaptan_verisini_duzenle)
    ekle_button.grid(column=4, row=4, columnspan=4)
    


def murettebat_formu(tab):
    # Mürettebat sekmesi içeriği
    murettebat_frame = ttk.Frame(tab)
    murettebat_frame.pack(fill="both", expand=True)

    # Mürettebat form alanları
    murettebat_adi_label = ttk.Label(murettebat_frame, text="Adı:")
    murettebat_adi_label.grid(column=0, row=0, pady=(15,0))
    murettebat_adi_entry = ttk.Entry(murettebat_frame)
    murettebat_adi_entry.grid(column=1, row=0, padx=(0, 50), pady=(15,0))

    murettebat_soyadi_label = ttk.Label(murettebat_frame, text="Soyadı:")
    murettebat_soyadi_label.grid(column=0, row=1)
    murettebat_soyadi_entry = ttk.Entry(murettebat_frame)
    murettebat_soyadi_entry.grid(column=1, row=1, padx=(0, 50))

    murettebat_adres_label = ttk.Label(murettebat_frame, text="Adres:")
    murettebat_adres_label.grid(column=0, row=2)
    murettebat_adres_entry = ttk.Entry(murettebat_frame)
    murettebat_adres_entry.grid(column=1, row=2, padx=(0, 50))

    murettebat_vatandaslik_label = ttk.Label(murettebat_frame, text="Vatandaşlık:")
    murettebat_vatandaslik_label.grid(column=0, row=3)
    murettebat_vatandaslik_entry = ttk.Entry(murettebat_frame)
    murettebat_vatandaslik_entry.grid(column=1, row=3, padx=(0, 50))

    murettebat_dogum_tarihi_label = ttk.Label(murettebat_frame, text="Doğum Tarihi (YYYY-MM-DD):")
    murettebat_dogum_tarihi_label.grid(column=0, row=4, padx=(30,30))
    murettebat_dogum_tarihi_entry = ttk.Entry(murettebat_frame)
    murettebat_dogum_tarihi_entry.grid(column=1, row=4, padx=(0, 50))

    murettebat_ise_giris_tarihi_label = ttk.Label(murettebat_frame, text="İşe Giriş Tarihi (YYYY-MM-DD):")
    murettebat_ise_giris_tarihi_label.grid(column=0, row=5, padx=(30,30))
    murettebat_ise_giris_tarihi_entry = ttk.Entry(murettebat_frame)
    murettebat_ise_giris_tarihi_entry.grid(column=1, row=5, padx=(0, 50))

    murettebat_gorev_label = ttk.Label(murettebat_frame, text="Görev:")
    murettebat_gorev_label.grid(column=0, row=6)
    murettebat_gorev_entry = ttk.Entry(murettebat_frame)
    murettebat_gorev_entry.grid(column=1, row=6, padx=(0, 50))

    murettebat_id_label = ttk.Label(murettebat_frame, text="Mürettebat ID:")
    murettebat_id_label.grid(column=2, row=2)
    murettebat_id_entry = ttk.Entry(murettebat_frame)
    murettebat_id_entry.grid(column=3, row=2, padx=(0, 50))

    murettebat_adi2_label = ttk.Label(murettebat_frame, text="Mürettebat Adı:")
    murettebat_adi2_label.grid(column=2, row=3)
    murettebat_adi2_entry = ttk.Entry(murettebat_frame)
    murettebat_adi2_entry.grid(column=3, row=3, padx=(0, 50))

    murettebat_id2_label = ttk.Label(murettebat_frame, text="Mürettebat ID:")
    murettebat_id2_label.grid(column=4, row=1)
    murettebat_id2_entry = ttk.Entry(murettebat_frame)
    murettebat_id2_entry.grid(column=5, row=1, padx=(0, 50))

    sutun_adi_label = ttk.Label(murettebat_frame, text="Düzenlenecek Sütun:")
    sutun_adi_label.grid(column=4, row=2)
    sutun_adi_entry = ttk.Entry(murettebat_frame)
    sutun_adi_entry.grid(column=5, row=2, padx=(0, 50))

    yeni_veri_label = ttk.Label(murettebat_frame, text="Yeni Veri:")
    yeni_veri_label.grid(column=4, row=3)
    yeni_veri_entry = ttk.Entry(murettebat_frame)
    yeni_veri_entry.grid(column=5, row=3, padx=(0, 50))


    def yeni_murettebat_ekle():
        murettebat_adi = murettebat_adi_entry.get()
        murettebat_soyadi = murettebat_soyadi_entry.get()
        murettebat_adres = murettebat_adres_entry.get()
        murettebat_vatandaslik = murettebat_vatandaslik_entry.get()
        murettebat_dogum_tarihi = murettebat_dogum_tarihi_entry.get()
        murettebat_ise_giris_tarihi = murettebat_ise_giris_tarihi_entry.get()
        murettebat_gorev = murettebat_gorev_entry.get()

        if murettebat_adi and murettebat_soyadi and murettebat_adres and murettebat_vatandaslik and murettebat_dogum_tarihi and murettebat_ise_giris_tarihi and murettebat_gorev:
            mürettebat = Mürettebat(murettebat_adi, murettebat_soyadi, murettebat_adres, murettebat_vatandaslik, murettebat_dogum_tarihi, murettebat_ise_giris_tarihi, murettebat_gorev)
            mürettebat.veritabanina_ekle()
            print("Yeni mürettebat eklendi:", murettebat_adi, murettebat_soyadi)
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(murettebat_frame, text="Yeni Mürettebat Ekle", command=yeni_murettebat_ekle)
    ekle_button.grid(column=0, row=7, columnspan=2)


    def murettebat_verisini_sil():
        murettebat_id = murettebat_id_entry.get()
        murettebat_adi = murettebat_adi2_entry.get()

        if murettebat_id and murettebat_adi:
            conn = baglan()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Mürettebatlar WHERE ID = ?", (murettebat_id,))
            murettebat_count = cursor.fetchone()[0]

            if murettebat_count == 1:
                cursor.execute("SELECT Ad FROM Mürettebatlar WHERE ID = ?", (murettebat_id,))
                murettebat_adi_veri = cursor.fetchone()[0]

                if murettebat_adi_veri == murettebat_adi:
                    cursor.execute("DELETE FROM Mürettebatlar WHERE ID = ?", (murettebat_id,))
                    conn.commit()
                    print(f"{murettebat_adi} isimli mürettebat başarıyla silindi.")
                else:
                    print("Girilen ad ile tablodaki ad verisi uyuşmuyor!")
            else:
                print("Belirtilen mürettebat bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(murettebat_frame, text="Mürettebat Verisini Sil", command=murettebat_verisini_sil)
    ekle_button.grid(column=1, row=4, columnspan=4)


    def murettebat_verisini_duzenle():
        murettebat_id2 = murettebat_id2_entry.get()
        sutun_adi = sutun_adi_entry.get()
        yeni_veri = yeni_veri_entry.get()

        if murettebat_id2 and sutun_adi and yeni_veri:
            conn = baglan()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Mürettebatlar WHERE ID = ?", (murettebat_id2,))
            gemi_count = cursor.fetchone()[0]

            if gemi_count == 1:
                sorgu = f"UPDATE Mürettebatlar SET {sutun_adi} = ? WHERE ID = ?"
                cursor.execute(sorgu, (yeni_veri, murettebat_id2))
                conn.commit()
                print(f"Mürettebat verisi başarıyla güncellendi.")
            else:
                print("Belirtilen mürettebat bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(murettebat_frame, text="Mürettebat Verisini Düzenle", command=murettebat_verisini_duzenle)
    ekle_button.grid(column=4, row=4, columnspan=4)

def liman_formu(tab):
    # Liman sekmesi içeriği
    liman_frame = ttk.Frame(tab)
    liman_frame.pack(fill="both", expand=True)

    # Liman form alanları
    liman_adi_label = ttk.Label(liman_frame, text="Liman Adı:")
    liman_adi_label.grid(column=0, row=0, pady=(15,0))
    liman_adi_entry = ttk.Entry(liman_frame)
    liman_adi_entry.grid(column=1, row=0, padx=(0, 50), pady=(15,0))

    liman_ulke_label = ttk.Label(liman_frame, text="Ülke:")
    liman_ulke_label.grid(column=0, row=1)
    liman_ulke_entry = ttk.Entry(liman_frame)
    liman_ulke_entry.grid(column=1, row=1, padx=(0, 50))

    liman_nufus_label = ttk.Label(liman_frame, text="Nüfus:")
    liman_nufus_label.grid(column=0, row=2)
    liman_nufus_entry = ttk.Entry(liman_frame)
    liman_nufus_entry.grid(column=1, row=2, padx=(0, 50))

    liman_pasaport_gerekli_label = ttk.Label(liman_frame, text="Pasaport Gerekli:")
    liman_pasaport_gerekli_label.grid(column=0, row=3, padx=(30,30))
    liman_pasaport_gerekli_combobox = ttk.Combobox(liman_frame, values=["Evet", "Hayır"])
    liman_pasaport_gerekli_combobox.grid(column=1, row=3, padx=(0, 50))

    liman_demirleme_ucreti_label = ttk.Label(liman_frame, text="Demirleme Ücreti:")
    liman_demirleme_ucreti_label.grid(column=0, row=4)
    liman_demirleme_ucreti_entry = ttk.Entry(liman_frame)
    liman_demirleme_ucreti_entry.grid(column=1, row=4, padx=(0, 50))

    # Ziyaret edildi onay kutusu
    liman_ziyaret_edildi_onay = tk.BooleanVar()
    liman_ziyaret_edildi_checkbox = ttk.Checkbutton(liman_frame, text="Ziyaret Edildi", variable=liman_ziyaret_edildi_onay)
    liman_ziyaret_edildi_checkbox.grid(column=0, row=5, columnspan=1)

    liman_ad2_label = ttk.Label(liman_frame, text="Liman Adı:")
    liman_ad2_label.grid(column=2, row=1)
    liman_ad2_entry = ttk.Entry(liman_frame)
    liman_ad2_entry.grid(column=3, row=1, padx=(0, 50))

    liman_ulke2_label = ttk.Label(liman_frame, text="Liman Ülkesi:")
    liman_ulke2_label.grid(column=2, row=2)
    liman_ulke2_entry = ttk.Entry(liman_frame)
    liman_ulke2_entry.grid(column=3, row=2, padx=(0, 50))

    liman_ad3_label = ttk.Label(liman_frame, text="Liman Adı:")
    liman_ad3_label.grid(column=4, row=1)
    liman_ad3_entry = ttk.Entry(liman_frame)
    liman_ad3_entry.grid(column=5, row=1, padx=(0, 50))

    liman_ulke3_label = ttk.Label(liman_frame, text="Liman Ülkesi:")
    liman_ulke3_label.grid(column=4, row=2)
    liman_ulke3_entry = ttk.Entry(liman_frame)
    liman_ulke3_entry.grid(column=5, row=2, padx=(0, 50))

    sutun_adi_label = ttk.Label(liman_frame, text="Düzenlenecek Sütun:")
    sutun_adi_label.grid(column=4, row=3)
    sutun_adi_entry = ttk.Entry(liman_frame)
    sutun_adi_entry.grid(column=5, row=3, padx=(0, 50))

    yeni_veri_label = ttk.Label(liman_frame, text="Yeni Veri:")
    yeni_veri_label.grid(column=4, row=4)
    yeni_veri_entry = ttk.Entry(liman_frame)
    yeni_veri_entry.grid(column=5, row=4, padx=(0, 50))

    # Yeni liman ekleme düğmesi
    def yeni_liman_ekle():
        liman_adi = liman_adi_entry.get()
        liman_ulke = liman_ulke_entry.get()
        liman_nufus = liman_nufus_entry.get()
        liman_pasaport_gerekli = liman_pasaport_gerekli_combobox.get()
        liman_demirleme_ucreti = liman_demirleme_ucreti_entry.get()
        liman_ziyaret_edildi = liman_ziyaret_edildi_onay.get()

        if liman_adi and liman_ulke and liman_nufus and liman_pasaport_gerekli and liman_demirleme_ucreti:
            liman = Liman(liman_adi, liman_ulke, liman_nufus, liman_pasaport_gerekli, liman_demirleme_ucreti, liman_ziyaret_edildi)
            liman.veritabanina_ekle()
            print("Yeni liman eklendi:", liman_adi)
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(liman_frame, text="Yeni Liman Ekle", command=yeni_liman_ekle)
    ekle_button.grid(column=0, row=6, columnspan=2)


    def liman_verisini_sil():
        liman_adi = liman_ad2_entry.get()
        liman_ulke2 = liman_ulke2_entry.get()

        if liman_adi and liman_ulke2:
            conn = baglan()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Limanlar WHERE LimanAdı = ?", (liman_adi,))
            liman_count = cursor.fetchone()[0]

            if liman_count == 1:
                cursor.execute("SELECT Ülke FROM Limanlar WHERE LimanAdı = ?", (liman_adi,))
                liman_ulke2_veri = cursor.fetchone()[0]

                if liman_ulke2_veri == liman_ulke2:
                    cursor.execute("DELETE FROM Limanlar WHERE LimanAdı = ?", (liman_adi,))
                    conn.commit()
                    print(f"{liman_adi} isimli liman başarıyla silindi.")
                else:
                    print("Girilen ülke ile tablodaki ülke verisi uyuşmuyor!")
            else:
                print("Belirtilen liman bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(liman_frame, text="Liman Verisini Sil", command=liman_verisini_sil)
    ekle_button.grid(column=1, row=3, columnspan=4)


    def liman_verisini_duzenle():
        liman_ad3 = liman_ad3_entry.get()
        liman_ulke3 = liman_ulke3_entry.get()
        sutun_adi = sutun_adi_entry.get()
        yeni_veri = yeni_veri_entry.get()

        if liman_ad3 and liman_ulke3 and sutun_adi and yeni_veri:
            conn = baglan()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Limanlar WHERE LimanAdı = ? AND Ülke = ?", (liman_ad3, liman_ulke3))
            liman_count = cursor.fetchone()[0]

            if liman_count == 1:
                sorgu = f"UPDATE Limanlar SET {sutun_adi} = ? WHERE LimanAdı = ? AND Ülke = ?"
                cursor.execute(sorgu, (yeni_veri, liman_ad3, liman_ulke3))
                conn.commit()
                print(f"Liman verisi başarıyla güncellendi.")
            else:
                print("Belirtilen liman bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(liman_frame, text="Liman Verisini Düzenle", command=liman_verisini_duzenle)
    ekle_button.grid(column=4, row=5, columnspan=4)


def gemi_id_al():
    conn = baglan() 
    cursor = conn.cursor()  

    # Veritabanından gemi ID'lerini al
    cursor.execute("SELECT ID FROM Gemiler")
    gemiler = cursor.fetchall()
    gemi_idler = [g[0] for g in gemiler]

    conn.close()  
    return gemi_idler

def murettebat_id_al():
    conn = baglan()  
    cursor = conn.cursor()  

    # Veritabanından mürettebat ID'lerini al
    cursor.execute("SELECT ID FROM Mürettebatlar")
    murettebatlar = cursor.fetchall()
    murettebat_idler = [m[0] for m in murettebatlar]

    conn.close()  
    return murettebat_idler

def kaptan_donus_kontrol(kaptan_id):
    conn = baglan()
    cursor = conn.cursor()

    # Kaptanın son seferinin dönüş tarihini al
    cursor.execute("SELECT MAX(DönüşTarihi) FROM Seferler INNER JOIN Sefer_Kaptan ON Seferler.SeferID = Sefer_Kaptan.SeferID WHERE KaptanID = ?", (kaptan_id,))
    son_donus_tarihi_str = cursor.fetchone()[0]

    if son_donus_tarihi_str:
        # Dönüş tarihini datetime nesnesine dönüştür
        son_donus_tarihi = datetime.strptime(son_donus_tarihi_str, "%Y-%m-%d")

        # Eğer dönüş tarihi mevcutsa ve son dönüş tarihi mevcut tarihten sonraki bir tarihse, kaptanın dönüş yapmadığı kabul edilir
        if son_donus_tarihi < datetime.now():
            return False
    return True

def gemi_donus_kontrol(gemi_id):
    conn = baglan()
    cursor = conn.cursor()

    # Geminin son seferinin dönüş tarihini al
    cursor.execute("SELECT MAX(DönüşTarihi) FROM Seferler WHERE GemiID = ?", (gemi_id,))
    son_donus_tarihi_str = cursor.fetchone()[0]

    if son_donus_tarihi_str:
        # Dönüş tarihini datetime nesnesine dönüştür
        son_donus_tarihi = datetime.strptime(son_donus_tarihi_str, "%Y-%m-%d")

        # Eğer dönüş tarihi mevcutsa ve son dönüş tarihi mevcut tarihten sonraki bir tarihse, kaptanın dönüş yapmadığı kabul edilir
        if son_donus_tarihi < datetime.now():
            return False
    return True

def murettebat_donus_kontrol(murettebat_id):
    conn = baglan()
    cursor = conn.cursor()

    # Mürettebatın son seferinin dönüş tarihini al
    cursor.execute("SELECT MAX(DönüşTarihi) FROM Seferler WHERE MürettebatID = ?", (murettebat_id,))
    son_donus_tarihi_str = cursor.fetchone()[0]

    if son_donus_tarihi_str:
        son_donus_tarihi = datetime.strptime(son_donus_tarihi_str, "%Y-%m-%d")

        if son_donus_tarihi < datetime.now():
            return False
    return True

def kaptan_id_kontrol(kaptan_id_entries):
    selected_kaptan_ids = []
    for entry in kaptan_id_entries:
        kaptan_id = entry.get()
        if not kaptan_id:
            print("Eksik kaptan ID'si.")
            return False  # Eksik kaptan ID varsa False döndür
        if kaptan_id in selected_kaptan_ids:
            print("Aynı kaptan ID'si birden fazla kez seçilemez.")
            return False  # Tekrar eden kaptan ID varsa False döndür
        selected_kaptan_ids.append(kaptan_id)
    return True


def sefer_formu(tab):
    # Seferler sekmesi içeriği
    seferler_frame = ttk.Frame(tab)
    seferler_frame.pack(fill="both", expand=True)

    # Seferler form alanları
    gemi_id_label = ttk.Label(seferler_frame, text="Gemi ID:")
    gemi_id_label.grid(column=0, row=0, pady=(15, 0))
    gemi_id_combobox = ttk.Combobox(seferler_frame, values=gemi_id_al())
    gemi_id_combobox.grid(column=1, row=0, pady=(15, 0))

    kaptan_sayisi_label = ttk.Label(seferler_frame, text="Kaptan Sayısı:")
    kaptan_sayisi_label.grid(column=0, row=1)
    kaptan_sayisi_entry = ttk.Entry(seferler_frame)
    kaptan_sayisi_entry.grid(column=1, row=1)

    murettebat_id_label = ttk.Label(seferler_frame, text="Mürettebat ID:")
    murettebat_id_label.grid(column=0, row=2)
    murettebat_id_combobox = ttk.Combobox(seferler_frame, values=murettebat_id_al())
    murettebat_id_combobox.grid(column=1, row=2)

    yola_cikis_tarihi_label = ttk.Label(seferler_frame, text="Yola Çıkış Tarihi (YYYY-MM-DD):")
    yola_cikis_tarihi_label.grid(column=0, row=3, padx=(30, 30))
    yola_cikis_tarihi_entry = ttk.Entry(seferler_frame)
    yola_cikis_tarihi_entry.grid(column=1, row=3)

    donus_tarihi_label = ttk.Label(seferler_frame, text="Dönüş Tarihi (YYYY-MM-DD):")
    donus_tarihi_label.grid(column=0, row=4)
    donus_tarihi_entry = ttk.Entry(seferler_frame)
    donus_tarihi_entry.grid(column=1, row=4)

    yola_cikis_limani_label = ttk.Label(seferler_frame, text="Yola Çıkış Limanı:")
    yola_cikis_limani_label.grid(column=0, row=5)
    yola_cikis_limani_entry = ttk.Entry(seferler_frame)
    yola_cikis_limani_entry.grid(column=1, row=5)

    liman_sayisi_label = ttk.Label(seferler_frame, text="Uğranılacak Liman Sayısı:")
    liman_sayisi_label.grid(column=0, row=6)
    liman_sayisi_entry = ttk.Entry(seferler_frame)
    liman_sayisi_entry.grid(column=1, row=6)

    sefer_id_label = ttk.Label(seferler_frame, text="Sefer ID:")
    sefer_id_label.grid(column=4, row=2, padx=(50, 0))
    sefer_id_entry = ttk.Entry(seferler_frame)
    sefer_id_entry.grid(column=5, row=2)

    gemi_id2_label = ttk.Label(seferler_frame, text="Gemi ID:")
    gemi_id2_label.grid(column=4, row=3, padx=(50, 0))
    gemi_id2_entry = ttk.Entry(seferler_frame)
    gemi_id2_entry.grid(column=5, row=3)

    sefer_id2_label = ttk.Label(seferler_frame, text="Sefer ID:")
    sefer_id2_label.grid(column=6, row=1, padx=(50, 0))
    sefer_id2_entry = ttk.Entry(seferler_frame)
    sefer_id2_entry.grid(column=7, row=1)

    gemi_id3_label = ttk.Label(seferler_frame, text="Gemi ID:")
    gemi_id3_label.grid(column=6, row=2, padx=(50, 0))
    gemi_id3_entry = ttk.Entry(seferler_frame)
    gemi_id3_entry.grid(column=7, row=2)

    sutun_adi_label = ttk.Label(seferler_frame, text="Sütun Adı:")
    sutun_adi_label.grid(column=6, row=3, padx=(50, 0))
    sutun_adi_entry = ttk.Entry(seferler_frame)
    sutun_adi_entry.grid(column=7, row=3)

    yeni_veri_label = ttk.Label(seferler_frame, text="Sütun Adı:")
    yeni_veri_label.grid(column=6, row=4, padx=(50, 0))
    yeni_veri_entry = ttk.Entry(seferler_frame)
    yeni_veri_entry.grid(column=7, row=4)

    limanlar_entry_list = []

    def liman_ekle():
        liman_sayisi = int(liman_sayisi_entry.get())
        for i in range(liman_sayisi):
            liman_label = ttk.Label(seferler_frame, text=f"Liman {i + 1}:")
            liman_label.grid(column=0, row=7 + i)
            liman_entry = ttk.Entry(seferler_frame)
            liman_entry.grid(column=1, row=7 + i)
            limanlar_entry_list.append(liman_entry)

        # Yeni sefer ekle düğmesinin konumunu güncelle
        ekle_button.grid(column=1, row=7 + liman_sayisi)

    def kaptan_id_al():
        kaptan_id_labels = []
        kaptan_id_entries = []

        def ekle():
            nonlocal kaptan_id_labels, kaptan_id_entries
            kaptan_id_sayisi = int(kaptan_sayisi_entry.get())

            if kaptan_id_sayisi < 2:
                print("En az 2 kaptan eklenmeli.")
                return

            conn = baglan()
            cursor = conn.cursor()

            for i in range(kaptan_id_sayisi):
                label = ttk.Label(seferler_frame, text=f"Kaptan {i + 1} ID:")
                label.grid(column=2, row=i + 2)
                kaptan_id_labels.append(label)

                entry = ttk.Combobox(seferler_frame, width=3)
                entry.grid(column=3, row=i + 2)
                kaptan_id_entries.append(entry)

                # Veritabanından kaptan ID'leri alınıp Combobox'a eklenir
                cursor.execute("SELECT ID FROM Kaptanlar")
                kaptanlar = cursor.fetchall()
                kaptan_id_entries[i]['values'] = tuple([kaptan[0] for kaptan in kaptanlar])

            conn.close()

        ekle_button = ttk.Button(seferler_frame, text="Kaptan ID Ekle", command=ekle)
        ekle_button.grid(column=2, row=1)

        return kaptan_id_labels, kaptan_id_entries
    
    def sefer_verisini_sil():
        sefer_id = sefer_id_entry.get()
        gemi_id2 = gemi_id2_entry.get()

        if sefer_id and gemi_id2:
            conn = baglan()
            cursor = conn.cursor()

            # Belirtilen SeferID ve GemiID'ye sahip sefer kaydını sil
            cursor.execute("DELETE FROM Seferler WHERE SeferID = ? AND GemiID = ?", (sefer_id, gemi_id2))
            conn.commit()

            # Sefer_Kaptan tablosundan belirtilen SeferID'ye sahip kaptan kayıtlarını sil
            cursor.execute("DELETE FROM Sefer_Kaptan WHERE SeferID = ?", (sefer_id,))
            conn.commit()

            print(f"SeferID: {sefer_id}, GemiID: {gemi_id2} olan sefer kaydı başarıyla silindi.")
            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(seferler_frame, text="Sefer Verisini Sil", command=sefer_verisini_sil)
    ekle_button.grid(column=3, row=4, columnspan=4)
    
    
    def sefer_verisini_duzenle():
        sefer_id2 = sefer_id_entry.get()
        gemi_id3 = gemi_id3_entry.get()
        sutun_adi = sutun_adi_entry.get()
        yeni_veri = yeni_veri_entry.get()

        if sefer_id2 and gemi_id3 and sutun_adi and yeni_veri:
            conn = baglan()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Seferler WHERE SeferID = ? AND GemiID = ?", (sefer_id2, gemi_id3))
            sefer_count = cursor.fetchone()[0]

            if sefer_count == 1:
                sorgu = f"UPDATE Seferler SET {sutun_adi} = ? WHERE SeferID = ? AND GemiID = ?"
                cursor.execute(sorgu, (yeni_veri, sefer_id2, gemi_id3))
                conn.commit()
                print("Sefer verisi başarıyla güncellendi.")
            else:
                print("Belirtilen sefer bulunamadı.")

            conn.close()
        else:
            print("Tüm alanlar doldurulmalıdır.")

    ekle_button = ttk.Button(seferler_frame, text="Sefer Verisini Düzenle", command=sefer_verisini_duzenle)
    ekle_button.grid(column=6, row=5, columnspan=4)


    def yeni_sefer_ekle():
        gemi_id = gemi_id_combobox.get()
        kaptan_ids = [entry.get() for entry in kaptan_id_entries]
        murettebat_id = murettebat_id_combobox.get()
        yola_cikis_tarihi = yola_cikis_tarihi_entry.get()
        donus_tarihi = donus_tarihi_entry.get()
        yola_cikis_limani = yola_cikis_limani_entry.get()
        limanlar = ", ".join(entry.get() for entry in limanlar_entry_list)

        if not gemi_donus_kontrol(gemi_id):
            print("Seçilen gemi henüz dönmemiştir.Yeni sefer eklenemez.")
            return

        for kaptan_id in kaptan_ids:
            if not kaptan_donus_kontrol(kaptan_id):
                print(f"Seçilen kaptan için dönüş kontrolü başarısız.Yeni sefer eklenemez.")
                return

        if not murettebat_donus_kontrol(murettebat_id):
            print("Seçilen mürettebat henüz dönmemiştir.Yeni sefer eklenemez.")
            return

        if not donus_tarihi > yola_cikis_tarihi:
            print("Dönüş tarihi, yola çıkış tarihinden sonra olmalıdır.")
            return

        if not all([gemi_id, kaptan_ids, murettebat_id, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani, limanlar]):
            print("Tüm alanlar doldurulmalıdır.")
            return

        if not kaptan_id_kontrol(kaptan_id_entries):
            return

        sefer = Sefer(gemi_id, kaptan_ids, murettebat_id, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani, limanlar)
        sefer_turu = sefer.sefer_turunu_al()

        conn = baglan() 
        cursor = conn.cursor() 
        # Seferler tablosuna SeferID ekleyin ve son eklenen SeferID'yi alın
        cursor.execute("INSERT INTO Seferler (GemiID, MürettebatID, YolaÇıkışTarihi, DönüşTarihi, YolaÇıkışLimanı, Limanlar, SeferTürü) VALUES (?, ?, ?, ?, ?, ?, ?)",(gemi_id, murettebat_id, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani, limanlar, sefer_turu))

        # Son eklenen SeferID'yi bir sorgu kullanarak alın
        cursor.execute("SELECT @@IDENTITY")
        sefer_id = cursor.fetchone()[0]

        # Sefer_Kaptan tablosuna SeferID değerlerini ekleyin
        for kaptan_id in kaptan_ids:
            cursor.execute("INSERT INTO Sefer_Kaptan (SeferID, KaptanID) VALUES (?, ?)", (sefer_id, kaptan_id))
        conn.commit()
        conn.close()
        print("Yeni sefer eklendi.")
    
    liman_ekle_button = ttk.Button(seferler_frame, text="Liman Ekle", command=liman_ekle)
    liman_ekle_button.grid(column=1, row=7)
    kaptan_id_labels, kaptan_id_entries = kaptan_id_al()
    ekle_button = ttk.Button(seferler_frame, text="Yeni Sefer Ekle", command=yeni_sefer_ekle)
    ekle_button.grid(column=1, row=8)

    return seferler_frame


# Ana uygulama penceresini oluşturma
root = tk.Tk()
root.title("Gezgin Gemi Şirketi Veritabanı Yönetimi")

# Arka plan resmini yükle
background_image = tk.PhotoImage(file="gemi.png")

# Canvas oluştur
canvas = tk.Canvas(root, width=800, height=300)
canvas.pack(fill="both", expand=True)

# Arka plan resmini canvas'a yerleştir
canvas.create_image(165, 0, image=background_image, anchor="nw")

# Gemiler sekmesi oluşturma
tab_control = ttk.Notebook(root)  
gemiler_tab = ttk.Frame(tab_control)  
tab_control.add(gemiler_tab, text='Gemiler') 
gemiler_formu(gemiler_tab) 
tab_control.pack(expand=1, fill="both")  

# Kaptanlar sekmesini oluşturma
kaptanlar_tab = ttk.Frame(tab_control)
tab_control.add(kaptanlar_tab, text='Kaptanlar')
kaptan_formu(kaptanlar_tab)

# Mürettebatlar sekmesini oluşturma
murettebat_tab = ttk.Frame(tab_control)
tab_control.add(murettebat_tab, text='Mürettebatlar')
murettebat_formu(murettebat_tab)

# Limanlar sekmesini oluşturma
liman_tab = ttk.Frame(tab_control)
tab_control.add(liman_tab, text='Limanlar')
liman_formu(liman_tab)

# Seferler sekmesini oluşturma
sefer_tab = ttk.Frame(tab_control)
tab_control.add(sefer_tab, text='Seferler')
sefer_formu(sefer_tab)

# Ana döngüyü başlat
root.mainloop()