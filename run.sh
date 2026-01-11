#!/bin/bash

# KrediOran.com Başlatma Scripti

echo "🚀 KrediOran.com başlatılıyor..."
echo ""

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı aktifleştir
echo "🔧 Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Bağımlılıkları yükle
echo "📥 Bağımlılıklar yükleniyor..."
pip install -r requirements.txt --quiet

# Uygulamayı başlat
echo ""
echo "✅ Uygulama başlatılıyor..."
echo "🌐 Tarayıcınızda açın: http://localhost:5000"
echo "⏹️  Durdurmak için: CTRL+C"
echo ""

python app.py
