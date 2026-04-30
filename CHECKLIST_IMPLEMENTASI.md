# ✅ CHECKLIST IMPLEMENTASI: Melatih Model agar Paham Banyak Kata

## STEP 1: Install Dependencies (5 menit)
```bash
# Install Sastrawi untuk stemming bahasa Indonesia
pip install Sastrawi

# Verifikasi install
python -c "from Sastrawi.Stemmer.StemmerFactory import StemmerFactory; print('✓ Sastrawi installed')"
```

---

## STEP 2: Test Model Sebelum & Sesudah (10 menit)

```bash
# Jalankan comparison test
python test_comparison.py
```

**Output yang diharapkan:**
- Tabel perbandingan accuracy Model Lama vs Model Baru
- Model Baru harus lebih tinggi ~10-20%
- Terlihat improvement untuk sinonim yang belum ada di training

---

## STEP 3: Tambah Training Data (20-30 menit)

### Edit: `chatbot.py` atau `model_improved.py`

**Tambahkan 10-15 kalimat per intent**

Contoh untuk "PANTAI":
```python
# Sebelum (14 kalimat)
("saya mau ke pantai", "pantai"),
("rekomendasi pantai di bali", "pantai"),
("pantai yang bagus", "pantai"),
# ... dst

# Sesudah (25+ kalimat)
("saya mau ke pantai", "pantai"),
("rekomendasi pantai di bali", "pantai"),
("pantai yang bagus", "pantai"),
("pantai mana yang recommended", "pantai"),        # ← NEW
("pantai dengan pasir putih", "pantai"),           # ← NEW
("pantai untuk liburan keluarga", "pantai"),       # ← NEW
("mau lihat pantai yang romantis", "pantai"),      # ← NEW
("pantai sepi jauh dari keramaian", "pantai"),     # ← NEW
("pantai tepi laut bali", "pantai"),               # ← NEW
("pantai apa saja di bali", "pantai"),             # ← NEW
("diving snorkeling di pantai", "pantai"),         # ← NEW
("pantai untuk berenang", "pantai"),               # ← NEW
("pantai dengan sunset indah", "pantai"),          # ← NEW
("pantai pasir halus dan putih", "pantai"),        # ← NEW
# ... dan seterusnya
```

**Strategi menambah:**
- [ ] Pikir 10 cara berbeda user bertanya tentang "pantai"
- [ ] Variasikan panjang kalimat (short & long)
- [ ] Tambah detail/adjective (sepi, indah, romantis, dll)
- [ ] Tambah kombinasi kata (pantai + berenang, pantai + sunset, dll)
- [ ] Jangan hanya copy-paste, ubah struktur kalimat

---

## STEP 4: Update Sinonim Dictionary (10 menit)

**Buka: `model_improved.py` atau `chatbot.py`**

Cari bagian:
```python
synonyms = {
    "pantai": ["tepi laut", "pesisir", "pantay", "laut"],
    "gunung": ["bukit", "pegunungan"],
    # ...
}
```

**Tambahkan sinonim lokal:**
```python
synonyms = {
    "pantai": ["tepi laut", "pesisir", "pantay", "laut", "beach"],
    "gunung": ["bukit", "pegunungan", "puncak", "gunung", "mountain"],
    "berenang": ["mandi", "renang", "diving", "snorkeling", "swimming"],
    "indah": ["bagus", "cantik", "menarik", "seru", "keren", "beautiful"],
    "liburan": ["libur", "traveling", "berlibur", "jalan jalan", "vacation"],
    "murah": ["hemat", "ekonomis", "terjangkau", "minim", "cheap"],
    "gratis": ["bebas", "tanpa bayar", "cuma cuma", "free"],
    "restoran": ["makan", "cafe", "warung", "kedai"],
    "tempat": ["lokasi", "destinasi", "spot", "area", "place"],
    # Tambah sinonim baru sesuai kebutuhan
}
```

---

## STEP 5: Re-train Model (5 menit)

```bash
# Test dengan data training baru
python model_improved.py

# Atau test dengan comparison
python test_comparison.py
```

---

## STEP 6: Integrasi ke Production (15 menit)

**Update: `chatbot.py` untuk gunakan preprocessing**

```python
# IMPORT PREPROCESSING
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

factory = StemmerFactory()
stemmer = factory.create_stemmer()

synonyms = {
    # ... sinonim dictionary ...
}

def preprocess_text(text):
    """Preprocessing untuk normalize input user"""
    text = text.lower()
    
    # Expand sinonim
    for key, values in synonyms.items():
        for syn in values:
            if syn in text:
                text = text.replace(syn, key)
    
    # Remove special chars
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Stemming
    words = text.split()
    words = [stemmer.stem(word) for word in words]
    
    return ' '.join(words)

# SAAT PREDICT, GUNAKAN PREPROCESSING
def chat(user_input):
    # Preprocess
    processed = preprocess_text(user_input)
    
    # Predict intent
    intent = model_chatbot.predict([processed])[0]
    confidence = max(model_chatbot.predict_proba([processed])[0])
    
    # Confidence threshold
    if confidence < 0.5:
        return "Maaf, saya kurang paham. Bisa coba tanya dengan cara lain?"
    
    # ... rest of logic ...
```

---

## STEP 7: Testing & Validation (Ongoing)

Buat file test dengan input yang mungkin user masukkan:

```python
# test_inputs.py
test_cases = [
    "mau ke pantai",
    "pantai apa yang bagus",
    "mau ke tepi laut",          # sinonim
    "pantay indah dimana",       # typo
    "liburan ke pantai murah",   # multiple intent
    "halo bali guide",           # greeting
    "bisa bantu saya",           # request help
]

for test_input in test_cases:
    response = chat(test_input)
    print(f"User: {test_input}")
    print(f"Bot: {response}\n")
```

---

## 📊 Metrics untuk Monitor

**Setelah implementasi, track:**

```python
from sklearn.metrics import accuracy_score, classification_report

# Validation set (separate dari training)
valid_inputs = [...]
valid_intents = [...]

# Preprocess
valid_inputs_processed = [preprocess_text(v) for v in valid_inputs]

# Evaluate
predictions = model_chatbot.predict(valid_inputs_processed)
accuracy = accuracy_score(valid_intents, predictions)

print(f"Accuracy: {accuracy:.2%}")
print("\n" + classification_report(valid_intents, predictions))
```

---

## 🎯 Expected Results

| Tahap | Akurasi | Notes |
|-------|---------|-------|
| Awal | ~70-75% | Model dasar |
| + Preprocessing | ~80-85% | Bersih & normalize |
| + Training Data | ~85-90% | Lebih banyak variasi |
| + Sinonim | ~90-95% | Pahami variasi kata |

---

## ❌ Troubleshooting

### Problem: Model masih tidak paham kata tertentu
**Solusi:**
1. Tambah training data untuk intent itu (min 15-20 variasi)
2. Check apakah kata sudah di sinonim dictionary
3. Test dengan `predict_proba()` untuk lihat confidence

### Problem: Confidence score terlalu rendah
**Solusi:**
1. Tambah training data lebih banyak
2. Adjust alpha parameter: `MultinomialNB(alpha=0.5)` (default 1.0)
3. Adjust max_features di TfidfVectorizer

### Problem: Model memilih intent yang salah
**Solusi:**
1. Ada overlap antara kategori? Pisahkan lebih jelas
2. Tambah contoh pembeda di training data
3. Gunakan confidence threshold untuk reject ambiguous input

---

## ✨ Tips Pro

1. **Jangan overfit:** Terlalu banyak data spesifik bisa membuat model rigid
2. **Balanced dataset:** Pastikan setiap intent punya jumlah data kira-kira sama
3. **Iterative:** Model ML perlu iterasi - train, test, improve, repeat
4. **Monitor real usage:** Log user input yang model tidak paham, gunakan untuk improve
5. **Version control:** Simpan model yang bagus, track progress dengan versioning

---

## 📚 Reference

- [Scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Sastrawi Indonesian Stemmer](https://github.com/har07/PySastrawi)
- [Naive Bayes Classifier](https://scikit-learn.org/stable/modules/naive_bayes.html)

---

**Total waktu implementasi: ~1-2 jam**

Mulai dari STEP 1 dan ikuti secara berurutan! 🚀
