"""
KrediOran.com - Kredi Karşılaştırma Backend
Hangikred.com'dan faiz oranlarını çeken Flask uygulaması
"""

from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List
import os

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Logging yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache için global değişkenler
cached_data = None
cache_time = None
CACHE_DURATION = timedelta(hours=1)  # 1 saat cache


class LoanRateScraper:
    """Hangikred.com'dan kredi faiz oranlarını çeken sınıf"""

    def __init__(self):
        self.base_url = "https://www.hangikred.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_sample_data(self) -> Dict:
        """
        Örnek veri seti (hangikred.com erişilemezse kullanılır)
        Gerçek uygulama için web scraping veya API kullanılmalı
        """
        return {
            "konut": [
                {"name": "Ziraat Bankası", "rate": 2.49, "logo": "🏦"},
                {"name": "Vakıfbank", "rate": 2.54, "logo": "🏦"},
                {"name": "Halkbank", "rate": 2.59, "logo": "🏦"},
                {"name": "İş Bankası", "rate": 2.69, "logo": "🏦"},
                {"name": "Garanti BBVA", "rate": 2.74, "logo": "🏦"},
                {"name": "Yapı Kredi", "rate": 2.79, "logo": "🏦"},
                {"name": "Akbank", "rate": 2.84, "logo": "🏦"},
                {"name": "QNB Finansbank", "rate": 2.89, "logo": "🏦"},
                {"name": "Denizbank", "rate": 2.94, "logo": "🏦"},
                {"name": "TEB", "rate": 2.99, "logo": "🏦"}
            ],
            "oto": [
                {"name": "Toyota Finans", "rate": 2.99, "logo": "🚗"},
                {"name": "Vakıfbank", "rate": 3.09, "logo": "🏦"},
                {"name": "Garanti BBVA", "rate": 3.19, "logo": "🏦"},
                {"name": "Ziraat Bankası", "rate": 3.24, "logo": "🏦"},
                {"name": "Halkbank", "rate": 3.29, "logo": "🏦"},
                {"name": "İş Bankası", "rate": 3.34, "logo": "🏦"},
                {"name": "Akbank", "rate": 3.39, "logo": "🏦"},
                {"name": "Yapı Kredi", "rate": 3.44, "logo": "🏦"},
                {"name": "QNB Finansbank", "rate": 3.49, "logo": "🏦"},
                {"name": "Denizbank", "rate": 3.54, "logo": "🏦"}
            ],
            "ihtiyac": [
                {"name": "Ziraat Bankası", "rate": 3.49, "logo": "🏦"},
                {"name": "Vakıfbank", "rate": 3.59, "logo": "🏦"},
                {"name": "Halkbank", "rate": 3.69, "logo": "🏦"},
                {"name": "İş Bankası", "rate": 3.79, "logo": "🏦"},
                {"name": "Garanti BBVA", "rate": 3.84, "logo": "🏦"},
                {"name": "Akbank", "rate": 3.89, "logo": "🏦"},
                {"name": "Yapı Kredi", "rate": 3.94, "logo": "🏦"},
                {"name": "QNB Finansbank", "rate": 3.99, "logo": "🏦"},
                {"name": "Denizbank", "rate": 4.04, "logo": "🏦"},
                {"name": "TEB", "rate": 4.09, "logo": "🏦"}
            ],
            "last_updated": datetime.now().isoformat()
        }

    def scrape_rates(self) -> Dict:
        """
        Hangikred.com'dan faiz oranlarını çeker
        Not: Gerçek scraping için sitenin yapısı analiz edilmeli
        """
        try:
            # Gerçek scraping kodu buraya gelecek
            # Şimdilik örnek veri döndürüyoruz
            logger.info("Hangikred.com'dan veri çekiliyor...")

            # TODO: Gerçek web scraping implementasyonu
            # response = requests.get(self.base_url, headers=self.headers, timeout=10)
            # soup = BeautifulSoup(response.content, 'html.parser')
            # # Parse işlemleri...

            return self.get_sample_data()

        except Exception as e:
            logger.error(f"Veri çekme hatası: {e}")
            return self.get_sample_data()


# Scraper instance
scraper = LoanRateScraper()


@app.route('/')
def index():
    """Ana sayfa"""
    return send_from_directory('.', 'index.html')


@app.route('/api/rates')
def get_rates():
    """Faiz oranlarını döndüren API endpoint"""
    global cached_data, cache_time

    # Cache kontrolü
    if cached_data and cache_time:
        if datetime.now() - cache_time < CACHE_DURATION:
            logger.info("Cache'den veri döndürülüyor")
            return jsonify(cached_data)

    # Yeni veri çek
    logger.info("Yeni veri çekiliyor...")
    data = scraper.scrape_rates()

    # Cache'e kaydet
    cached_data = data
    cache_time = datetime.now()

    return jsonify(data)


@app.route('/api/rates/<loan_type>')
def get_rates_by_type(loan_type):
    """Belirli bir kredi tipi için faiz oranlarını döndürür"""
    global cached_data, cache_time

    # Cache kontrolü
    if not cached_data or not cache_time or datetime.now() - cache_time >= CACHE_DURATION:
        cached_data = scraper.scrape_rates()
        cache_time = datetime.now()

    if loan_type in cached_data:
        return jsonify({
            loan_type: cached_data[loan_type],
            "last_updated": cached_data.get("last_updated")
        })
    else:
        return jsonify({"error": "Geçersiz kredi tipi"}), 400


@app.route('/api/calculate', methods=['POST'])
def calculate_loan():
    """Kredi hesaplama API endpoint"""
    from flask import request

    try:
        data = request.get_json()
        principal = float(data.get('amount', 0))
        rate = float(data.get('rate', 0))
        term = int(data.get('term', 0))

        # Hesaplama
        r = rate / 100
        monthly_payment = principal * (r * (1 + r) ** term) / ((1 + r) ** term - 1)
        total_payment = monthly_payment * term
        total_interest = total_payment - principal

        return jsonify({
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2)
        })

    except Exception as e:
        logger.error(f"Hesaplama hatası: {e}")
        return jsonify({"error": "Hesaplama hatası"}), 400


@app.route('/api/health')
def health_check():
    """Sağlık kontrolü endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache_age": (datetime.now() - cache_time).seconds if cache_time else None
    })


# Static dosyalar için route
@app.route('/<path:path>')
def static_files(path):
    """Static dosyaları serve et"""
    return send_from_directory('.', path)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
