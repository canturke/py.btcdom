# KrediOran.com - Türkiye'nin En Uygun Kredi Karşılaştırma Platformu

Modern ve responsive bir web uygulaması ile Türkiye'deki en uygun kredi faiz oranlarını karşılaştırın.

## 🎯 Özellikler

- **3 Kredi Türü Karşılaştırması**
  - 🏠 Konut Kredisi
  - 🚗 Oto Kredisi
  - 💰 İhtiyaç Kredisi

- **Gelişmiş Hesaplama**
  - Aylık taksit hesaplama
  - Toplam geri ödeme tutarı
  - Toplam faiz hesaplama
  - Özelleştirilebilir vade ve tutar

- **Modern Arayüz**
  - Responsive tasarım (mobil, tablet, desktop)
  - Kullanıcı dostu interface
  - Gerçek zamanlı hesaplama

- **Güncel Veriler**
  - Hangikred.com entegrasyonu
  - Cache sistemi ile hızlı yanıt
  - Otomatik veri güncelleme

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- Modern web tarayıcı

### Adımlar

1. **Repoyu klonlayın**
```bash
git clone <repo-url>
cd py.btcdom
```

2. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

3. **Uygulamayı başlatın**
```bash
python app.py
```

4. **Tarayıcıda açın**
```
http://localhost:5000
```

## 📁 Proje Yapısı

```
py.btcdom/
├── index.html          # Ana sayfa
├── styles.css          # CSS stilleri
├── script.js           # JavaScript mantığı
├── app.py              # Flask backend
├── requirements.txt    # Python bağımlılıkları
└── README.md          # Dokümantasyon
```

## 🔧 Kullanım

### Web Arayüzü

1. **Kredi Türü Seçin**: Konut, Oto veya İhtiyaç kredisini seçin
2. **Tutar Girin**: Almak istediğiniz kredi tutarını girin
3. **Vade Seçin**: Kaç ay vadede ödemek istediğinizi girin
4. **Hesapla**: Butona tıklayın ve sonuçları görün

### API Endpoints

#### Tüm Faiz Oranlarını Getir
```bash
GET /api/rates
```

#### Belirli Kredi Türü İçin Oranlar
```bash
GET /api/rates/{konut|oto|ihtiyac}
```

#### Kredi Hesaplama
```bash
POST /api/calculate
Content-Type: application/json

{
  "amount": 500000,
  "rate": 2.49,
  "term": 120
}
```

#### Sağlık Kontrolü
```bash
GET /api/health
```

## 🎨 Özelleştirme

### Banka Verilerini Güncelleme

`script.js` dosyasındaki `bankData` nesnesini düzenleyin:

```javascript
const bankData = {
    konut: [
        { name: "Banka Adı", rate: 2.49, logo: "🏦" },
        // ...
    ]
};
```

### Stil Değişiklikleri

`styles.css` dosyasındaki CSS değişkenlerini düzenleyin:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #10b981;
    /* ... */
}
```

## 🔄 Veri Kaynağı

Faiz oranları [hangikred.com](https://www.hangikred.com) sitesinden alınmaktadır.

## 📱 Responsive Tasarım

- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: 320px - 767px

## 🛠️ Teknolojiler

- **Frontend**
  - HTML5
  - CSS3 (Flexbox, Grid)
  - Vanilla JavaScript (ES6+)

- **Backend**
  - Python 3.8+
  - Flask
  - BeautifulSoup4 (Web Scraping)
  - Requests

## 📊 Hesaplama Formülü

Aylık taksit hesaplaması için kullanılan formül:

```
A = P × [r(1+r)^n] / [(1+r)^n - 1]

A: Aylık ödeme
P: Ana para (kredi tutarı)
r: Aylık faiz oranı
n: Toplam taksit sayısı
```

## 🔐 Güvenlik

- CORS koruması
- Input validasyonu
- XSS koruması
- Rate limiting (önerilir)

## 📈 Geliştirme Planı

- [ ] Gerçek zamanlı hangikred.com scraping
- [ ] Kullanıcı favorileri
- [ ] Karşılaştırma geçmişi
- [ ] PDF rapor oluşturma
- [ ] E-posta bildirimleri
- [ ] Daha fazla banka ekleme
- [ ] Mobil uygulama

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje eğitim amaçlıdır. Ticari kullanım için ilgili bankalardan izin alınmalıdır.

## ⚠️ Yasal Uyarı

Bu sitedeki faiz oranları bilgilendirme amaçlıdır. Kesin oranlar için lütfen ilgili banka ile iletişime geçiniz. KrediOran.com herhangi bir banka veya finans kuruluşu değildir.

## 📞 İletişim

- Website: kredioran.com
- Email: info@kredioran.com

---

Made with ❤️ for Turkish loan seekers
