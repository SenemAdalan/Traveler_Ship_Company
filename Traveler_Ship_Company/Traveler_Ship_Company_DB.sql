CREATE TABLE Gemiler(
	ID INT PRIMARY KEY IDENTITY(1,1),
	Adı NVARCHAR(50) NOT NULL,
	Ağırlık FLOAT, 
	YapımYılı INT,
	Tip NVARCHAR(50),
	YolcuKapasitesi INT,
	PetrolKapasitesi FLOAT,
	KonteynerSayısı INT,
	MaksimumAğırlık FLOAT
);

CREATE TABLE Kaptanlar (
	ID INT PRIMARY KEY IDENTITY(1,1),
	Ad NVARCHAR(50) NOT NULL,
	Soyad NVARCHAR(50),
	Adres NVARCHAR(100),
	Vatandaşlık NVARCHAR(50),
	DoğumTarihi DATE,
	İşeGirişTarihi DATE,
	Lisans NVARCHAR(50),
);

CREATE TABLE Mürettebatlar (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Ad NVARCHAR(50) NOT NULL,
    Soyad NVARCHAR(50),
    Adres NVARCHAR(100),
    Vatandaşlık NVARCHAR(50),
    DoğumTarihi DATE,
    İşeGirişTarihi DATE,
    Görev NVARCHAR(50)
);

CREATE TABLE Limanlar (
    LimanAdı NVARCHAR(50) PRIMARY KEY,
    Ülke NVARCHAR(50),
    Nüfus INT,
    PasaportGerekli NVARCHAR(5),
    DemirlemeÜcreti FLOAT
);

CREATE TABLE Seferler (
    SeferID INT PRIMARY KEY IDENTITY,
    GemiID INT NOT NULL,
    MürettebatID INT NOT NULL,
    YolaÇıkışTarihi DATE NOT NULL,
    DönüşTarihi DATE NOT NULL,
    YolaÇıkışLimani NVARCHAR(100) NOT NULL,
    Limanlar NVARCHAR(MAX) NOT NULL,
    SeferTürü NVARCHAR(50),
    FOREIGN KEY (GemiID) REFERENCES Gemiler(ID),
    FOREIGN KEY (MürettebatID) REFERENCES Mürettebatlar(ID)
);

CREATE TABLE Sefer_Kaptan (
    SeferID INT,
    KaptanID INT,
    FOREIGN KEY (SeferID) REFERENCES Seferler(SeferID),
    FOREIGN KEY (KaptanID) REFERENCES Kaptanlar(ID)
);

