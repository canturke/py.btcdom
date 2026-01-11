// Banka Verileri - hangikred.com'dan alınan örnek veriler
const bankData = {
    konut: [
        { name: "Ziraat Bankası", rate: 2.49, logo: "🏦" },
        { name: "Vakıfbank", rate: 2.54, logo: "🏦" },
        { name: "Halkbank", rate: 2.59, logo: "🏦" },
        { name: "İş Bankası", rate: 2.69, logo: "🏦" },
        { name: "Garanti BBVA", rate: 2.74, logo: "🏦" },
        { name: "Yapı Kredi", rate: 2.79, logo: "🏦" },
        { name: "Akbank", rate: 2.84, logo: "🏦" },
        { name: "QNB Finansbank", rate: 2.89, logo: "🏦" },
        { name: "Denizbank", rate: 2.94, logo: "🏦" },
        { name: "TEB", rate: 2.99, logo: "🏦" }
    ],
    oto: [
        { name: "Toyota Finans", rate: 2.99, logo: "🚗" },
        { name: "Vakıfbank", rate: 3.09, logo: "🏦" },
        { name: "Garanti BBVA", rate: 3.19, logo: "🏦" },
        { name: "Ziraat Bankası", rate: 3.24, logo: "🏦" },
        { name: "Halkbank", rate: 3.29, logo: "🏦" },
        { name: "İş Bankası", rate: 3.34, logo: "🏦" },
        { name: "Akbank", rate: 3.39, logo: "🏦" },
        { name: "Yapı Kredi", rate: 3.44, logo: "🏦" },
        { name: "QNB Finansbank", rate: 3.49, logo: "🏦" },
        { name: "Denizbank", rate: 3.54, logo: "🏦" }
    ],
    ihtiyac: [
        { name: "Ziraat Bankası", rate: 3.49, logo: "🏦" },
        { name: "Vakıfbank", rate: 3.59, logo: "🏦" },
        { name: "Halkbank", rate: 3.69, logo: "🏦" },
        { name: "İş Bankası", rate: 3.79, logo: "🏦" },
        { name: "Garanti BBVA", rate: 3.84, logo: "🏦" },
        { name: "Akbank", rate: 3.89, logo: "🏦" },
        { name: "Yapı Kredi", rate: 3.94, logo: "🏦" },
        { name: "QNB Finansbank", rate: 3.99, logo: "🏦" },
        { name: "Denizbank", rate: 4.04, logo: "🏦" },
        { name: "TEB", rate: 4.09, logo: "🏦" }
    ]
};

// Global değişkenler
let currentLoanType = 'konut';
let currentAmount = 500000;
let currentTerm = 120;

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Kredi tipi butonlarına event listener ekle
    const loanTypeBtns = document.querySelectorAll('.loan-type-btn');
    loanTypeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Aktif sınıfı kaldır
            loanTypeBtns.forEach(b => b.classList.remove('active'));
            // Yeni aktif sınıfı ekle
            this.classList.add('active');
            // Kredi tipini güncelle
            currentLoanType = this.dataset.type;
            // Sonuçları güncelle
            updateResults();
        });
    });

    // Form submit event listener
    const form = document.getElementById('loanCalculator');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        calculateLoans();
    });

    // İlk yükleme
    updateResults();
}

function calculateLoans() {
    // Form verilerini al
    const amountInput = document.getElementById('loanAmount');
    const termInput = document.getElementById('loanTerm');

    currentAmount = parseFloat(amountInput.value);
    currentTerm = parseInt(termInput.value);

    // Validasyon
    if (currentAmount < 1000) {
        alert('Kredi tutarı en az 1.000 TL olmalıdır.');
        return;
    }

    if (currentTerm < 1 || currentTerm > 360) {
        alert('Vade 1 ile 360 ay arasında olmalıdır.');
        return;
    }

    // Sonuçları güncelle
    updateResults();

    // Sonuçlara scroll yap
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function updateResults() {
    // Kredi tipi ismini güncelle
    const loanTypeNames = {
        'konut': 'Konut',
        'oto': 'Oto',
        'ihtiyac': 'İhtiyaç'
    };
    document.getElementById('loanTypeName').textContent = loanTypeNames[currentLoanType];

    // Bankaları sırala (en düşük faizden yükseğe)
    const banks = [...bankData[currentLoanType]].sort((a, b) => a.rate - b.rate);

    // En iyi 3 bankayı göster
    displayTopBanks(banks.slice(0, 3));

    // Detaylı tabloyu doldur
    displayDetailTable(banks);
}

function displayTopBanks(topBanks) {
    const container = document.getElementById('banksContainer');
    container.innerHTML = '';

    topBanks.forEach((bank, index) => {
        const calculation = calculateMonthlyPayment(currentAmount, bank.rate, currentTerm);

        const card = document.createElement('div');
        card.className = `bank-card ${index === 0 ? 'best' : ''}`;

        card.innerHTML = `
            ${index === 0 ? '<div class="best-badge">En Uygun</div>' : ''}
            <div class="rank" style="background: ${index === 0 ? '#10b981' : index === 1 ? '#3b82f6' : '#6366f1'}">${index + 1}</div>
            <div class="bank-name">${bank.logo} ${bank.name}</div>
            <div class="interest-rate">
                %${bank.rate.toFixed(2)}
                <span>aylık faiz oranı</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Aylık Taksit:</span>
                <span class="detail-value">${formatCurrency(calculation.monthlyPayment)}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Toplam Geri Ödeme:</span>
                <span class="detail-value">${formatCurrency(calculation.totalPayment)}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Toplam Faiz:</span>
                <span class="detail-value">${formatCurrency(calculation.totalInterest)}</span>
            </div>
        `;

        container.appendChild(card);
    });
}

function displayDetailTable(banks) {
    const tbody = document.getElementById('detailTableBody');
    tbody.innerHTML = '';

    banks.forEach((bank, index) => {
        const calculation = calculateMonthlyPayment(currentAmount, bank.rate, currentTerm);

        const row = document.createElement('tr');
        row.className = index < 3 ? 'best-rate' : '';

        row.innerHTML = `
            <td><strong>${bank.logo} ${bank.name}</strong></td>
            <td><strong>%${bank.rate.toFixed(2)}</strong></td>
            <td>${formatCurrency(calculation.monthlyPayment)}</td>
            <td>${formatCurrency(calculation.totalPayment)}</td>
            <td>${formatCurrency(calculation.totalInterest)}</td>
        `;

        tbody.appendChild(row);
    });
}

/**
 * Aylık taksit hesaplama fonksiyonu
 * Formül: A = P * [r(1+r)^n] / [(1+r)^n - 1]
 * A = Aylık ödeme
 * P = Ana para (kredi tutarı)
 * r = Aylık faiz oranı (yıllık faiz / 12 / 100)
 * n = Toplam taksit sayısı
 */
function calculateMonthlyPayment(principal, monthlyRate, term) {
    // Aylık faiz oranını decimal'e çevir
    const r = monthlyRate / 100;

    // Aylık ödemeyi hesapla
    const monthlyPayment = principal * (r * Math.pow(1 + r, term)) / (Math.pow(1 + r, term) - 1);

    // Toplam ödeme
    const totalPayment = monthlyPayment * term;

    // Toplam faiz
    const totalInterest = totalPayment - principal;

    return {
        monthlyPayment: monthlyPayment,
        totalPayment: totalPayment,
        totalInterest: totalInterest
    };
}

/**
 * Para formatı (₺ işareti ile)
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('tr-TR', {
        style: 'currency',
        currency: 'TRY',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

/**
 * Veri güncelleme fonksiyonu (API entegrasyonu için hazır)
 */
async function fetchBankData() {
    try {
        // API endpoint'i buraya gelecek
        // const response = await fetch('/api/rates');
        // const data = await response.json();
        // bankData = data;
        // updateResults();
        console.log('Veri güncelleme fonksiyonu - API entegrasyonu için hazır');
    } catch (error) {
        console.error('Veri güncelleme hatası:', error);
    }
}

// Otomatik veri güncelleme (her 30 dakikada bir)
// setInterval(fetchBankData, 30 * 60 * 1000);
