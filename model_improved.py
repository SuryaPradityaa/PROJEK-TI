import pandas as pd
import numpy as np
import re
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("dataset_wisata_bali.csv")

# =========================
# TEXT PREPROCESSING
# =========================
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Dictionary sinonim bahasa Indonesia
synonyms = {
    "pantai": ["tepi laut", "pesisir", "pantay", "laut"],
    "gunung": ["bukit", "pegunungan", "puncak"],
    "berenang": ["mandi", "renang", "diving", "snorkeling"],
    "indah": ["bagus", "cantik", "menarik", "seru", "keren"],
    "liburan": ["libur", "traveling", "berlibur", "jalan jalan"],
    "tempat": ["lokasi", "destinasi", "spot", "area"],
    "bali": ["pulau bali", "bali pulau"],
    "murah": ["hemat", "ekonomis", "terjangkau", "minim"],
    "gratis": ["bebas", "tanpa bayar", "cuma cuma"],
    "terbaik": ["terpopuler", "terkenal", "paling bagus", "paling recommended"],
}

def preprocess_text(text):
    """Preprocessing text: lowercase, stemming, remove special chars"""
    # Lowercase
    text = text.lower()
    
    # Expand synonyms
    for key, values in synonyms.items():
        for syn in values:
            if syn in text:
                text = text.replace(syn, key)
    
    # Remove special characters tapi jaga spasi
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Stemming untuk setiap kata
    words = text.split()
    words = [stemmer.stem(word) for word in words]
    text = ' '.join(words)
    
    return text

# =========================
# EXPANDED TRAINING DATA
# =========================
training_data = [
    # --- PANTAI ---
    ("saya mau ke pantai", "pantai"),
    ("rekomendasi pantai di bali", "pantai"),
    ("pantai yang bagus", "pantai"),
    ("wisata pantai", "pantai"),
    ("mau liburan ke tepi laut", "pantai"),
    ("pantai yang sepi", "pantai"),
    ("ingin berenang di pantai", "pantai"),
    ("pantai indah bali", "pantai"),
    ("ke pantai yuk", "pantai"),
    ("mau snorkeling", "pantai"),
    ("mau surfing", "pantai"),
    ("pantai pasir putih", "pantai"),
    ("pantai romantis", "pantai"),
    ("sunset di pantai", "pantai"),
    ("pantai mana yang bagus", "pantai"),
    ("pantai terbaik bali", "pantai"),
    ("mau lihat laut", "pantai"),
    ("pantai untuk keluarga", "pantai"),
    ("pantai sepi dan tenang", "pantai"),
    ("diving di pantai", "pantai"),

    # --- ALAM ---
    ("wisata alam", "alam"),
    ("mau ke gunung", "alam"),
    ("air terjun bali", "alam"),
    ("trekking di bali", "alam"),
    ("hiking bali", "alam"),
    ("wisata pegunungan", "alam"),
    ("mau ke hutan", "alam"),
    ("pemandangan alam indah", "alam"),
    ("danau bali", "alam"),
    ("air terjun yang bagus", "alam"),
    ("wisata outbound", "alam"),
    ("alam bali yang asri", "alam"),
    ("mau camping", "alam"),
    ("sawah terasering", "alam"),
    ("naik bukit", "alam"),
    ("panjat gunung", "alam"),
    ("mau di alam", "alam"),
    ("air terjun tersembunyi", "alam"),
    ("danau indah", "alam"),

    # --- BUDAYA ---
    ("wisata budaya", "budaya"),
    ("mau ke pura", "budaya"),
    ("tempat bersejarah bali", "budaya"),
    ("wisata tradisional", "budaya"),
    ("mau lihat tari kecak", "budaya"),
    ("museum bali", "budaya"),
    ("pura besar bali", "budaya"),
    ("kebudayaan bali", "budaya"),
    ("mau ke ubud", "budaya"),
    ("seni budaya bali", "budaya"),
    ("mau ke desa adat", "budaya"),
    ("temple bali", "budaya"),
    ("mau foto di pura", "budaya"),
    ("seni tradisional", "budaya"),
    ("mau belajar budaya", "budaya"),
    ("peninggalan sejarah", "budaya"),

    # --- KULINER ---
    ("wisata kuliner", "kuliner"),
    ("mau belanja", "kuliner"),
    ("pasar oleh oleh", "kuliner"),
    ("makanan khas bali", "kuliner"),
    ("tempat makan bali", "kuliner"),
    ("belanja souvenir", "kuliner"),
    ("pasar tradisional", "kuliner"),
    ("oleh oleh bali", "kuliner"),
    ("mau cari makan", "kuliner"),
    ("kuliner enak bali", "kuliner"),
    ("tempat belanja murah", "kuliner"),
    ("cari makan enak", "kuliner"),
    ("restoran bali", "kuliner"),
    ("makanan lokal", "kuliner"),
    ("pasar bali", "kuliner"),

    # --- HIBURAN ---
    ("wisata hiburan", "hiburan"),
    ("taman bermain", "hiburan"),
    ("tempat seru", "hiburan"),
    ("mau seru seruan", "hiburan"),
    ("wahana permainan", "hiburan"),
    ("liburan keluarga", "hiburan"),
    ("bawa anak main", "hiburan"),
    ("taman hiburan bali", "hiburan"),
    ("waterpark bali", "hiburan"),
    ("mau yang seru", "hiburan"),
    ("tempat asik", "hiburan"),
    ("main main", "hiburan"),

    # --- MURAH ---
    ("wisata murah", "murah"),
    ("tempat gratis bali", "murah"),
    ("liburan hemat", "murah"),
    ("tidak punya banyak uang", "murah"),
    ("budget terbatas", "murah"),
    ("tiket murah", "murah"),
    ("wisata gratis", "murah"),
    ("tempat murah meriah", "murah"),
    ("liburan dengan budget minim", "murah"),
    ("hemat biaya", "murah"),
    ("gratis tiket", "murah"),

    # --- RATING TINGGI ---
    ("tempat terbaik di bali", "terbaik"),
    ("wisata paling populer", "terbaik"),
    ("rekomendasi terbaik", "terbaik"),
    ("tempat yang bagus banget", "terbaik"),
    ("rating tertinggi", "terbaik"),
    ("tempat terkenal bali", "terbaik"),
    ("yang paling recommended", "terbaik"),
    ("destinasi terpopuler", "terbaik"),
    ("wisata hits bali", "terbaik"),
    ("tempat yang paling bagus", "terbaik"),
    ("favorit wisatawan", "terbaik"),

    # --- LOKASI ---
    ("wisata di badung", "lokasi_badung"),
    ("tempat di badung", "lokasi_badung"),
    ("seminyak kuta", "lokasi_badung"),
    ("pantai kuta badung", "lokasi_badung"),
    ("nusa dua badung", "lokasi_badung"),
    ("wisata di ubud", "lokasi_gianyar"),
    ("tempat di gianyar", "lokasi_gianyar"),
    ("monkey forest ubud", "lokasi_gianyar"),
    ("tegalalang gianyar", "lokasi_gianyar"),
    ("wisata di denpasar", "lokasi_denpasar"),
    ("tempat di denpasar", "lokasi_denpasar"),
    ("sanur denpasar", "lokasi_denpasar"),
    ("museum denpasar", "lokasi_denpasar"),
    ("wisata di karangasem", "lokasi_karangasem"),
    ("tirta gangga karangasem", "lokasi_karangasem"),
    ("amed karangasem", "lokasi_karangasem"),
    ("wisata di buleleng", "lokasi_buleleng"),
    ("lovina buleleng", "lokasi_buleleng"),
    ("singaraja buleleng", "lokasi_buleleng"),
    ("wisata di tabanan", "lokasi_tabanan"),
    ("tanah lot tabanan", "lokasi_tabanan"),
    ("bedugul tabanan", "lokasi_tabanan"),
    ("wisata di bangli", "lokasi_bangli"),
    ("kintamani bangli", "lokasi_bangli"),
    ("danau batur bangli", "lokasi_bangli"),
    ("wisata di klungkung", "lokasi_klungkung"),
    ("nusa penida klungkung", "lokasi_klungkung"),
    ("kertha gosa klungkung", "lokasi_klungkung"),
    ("wisata di jembrana", "lokasi_jembrana"),
    ("medewi jembrana", "lokasi_jembrana"),
    ("taman nasional bali barat jembrana", "lokasi_jembrana"),

    # --- SALAM / UMUM ---
    ("halo", "salam"),
    ("hai", "salam"),
    ("hello", "salam"),
    ("selamat pagi", "salam"),
    ("selamat siang", "salam"),
    ("selamat malam", "salam"),
    ("hei bali guide", "salam"),
    ("apa kabar", "salam"),
    ("help", "bantuan"),
    ("tolong bantu", "bantuan"),
    ("bisa bantu saya", "bantuan"),
    ("mau liburan ke bali", "bantuan"),
    ("tidak tahu mau kemana", "bantuan"),
    ("bingung mau ke mana", "bantuan"),
    ("ada rekomendasi", "bantuan"),
    ("bantu saya pilih", "bantuan"),
    ("gimana caranya", "bantuan"),
]

kalimat_train = [d[0] for d in training_data]
intent_train  = [d[1] for d in training_data]

# Preprocessing
kalimat_train_processed = [preprocess_text(k) for k in kalimat_train]

# =========================
# TRAIN MODEL IMPROVED
# =========================
model_chatbot = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 2),           # Unigram + Bigram
        min_df=1,
        max_df=0.95,
        lowercase=True,
        token_pattern=r'(?u)\b\w+\b'
    )),
    ('clf', MultinomialNB(alpha=0.1))
])

# =========================
# SPLIT DATA: TRAIN & TEST
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    kalimat_train_processed,
    intent_train,
    test_size=0.2,
    random_state=42
    # stratify dihapus karena beberapa kategori lokasi hanya punya 1-2 data
)

# Fit model hanya dengan data training
model_chatbot.fit(X_train, y_train)

# =========================
# EVALUASI MODEL
# =========================
y_pred = model_chatbot.predict(X_test)
akurasi = accuracy_score(y_test, y_pred)

print("=" * 50)
print("     EVALUASI MODEL CHATBOT WISATA BALI")
print("=" * 50)
print(f"\n✅ Akurasi: {akurasi * 100:.1f}%")
print(f"   Data Training : {len(X_train)} kalimat")
print(f"   Data Testing  : {len(X_test)} kalimat")
print("\n📊 Detail per Kategori:")
print(classification_report(y_test, y_pred))

# =========================
# SIMPAN MODEL KE FILE
# =========================
MODEL_PATH = "model_chatbot.pkl"
joblib.dump(model_chatbot, MODEL_PATH)
print(f"💾 Model berhasil disimpan ke: {MODEL_PATH}")

# =========================
# FUNGSI PREDIKSI
# =========================
def load_model(path=MODEL_PATH):
    """Load model dari file (lebih cepat dari training ulang)"""
    if os.path.exists(path):
        return joblib.load(path)
    else:
        raise FileNotFoundError(f"Model tidak ditemukan di {path}. Jalankan training ulang.")

def predict_intent(user_input, confidence=False, model=None):
    """Predict intent dari input user"""
    mdl = model if model else model_chatbot
    processed = preprocess_text(user_input)
    intent = mdl.predict([processed])[0]

    if confidence:
        probabilities = mdl.predict_proba([processed])
        confidence_score = max(probabilities[0])
        # Jika confidence rendah, kembalikan 'unknown'
        if confidence_score < 0.4:
            return "unknown", confidence_score
        return intent, confidence_score

    return intent

# =========================
# TEST MODEL
# =========================
if __name__ == "__main__":
    test_inputs = [
        "mau ke pantai yang indah",
        "rekomendasi tempat makan enak",
        "budget saya terbatas",
        "mau lihat alam",
        "pura mana yang terkenal",
        "halo bali guide",
        "pantai apa yang bagus",
        "xyz random tidak jelas",   # uji confidence rendah
    ]

    print("\n=== TEST PREDIKSI ===\n")
    for user_input in test_inputs:
        intent, conf = predict_intent(user_input, confidence=True)
        status = "⚠️ Tidak dikenali" if intent == "unknown" else "✅"
        print(f"{status} Input     : {user_input}")
        print(f"   Intent    : {intent}")
        print(f"   Confidence: {conf:.2f}\n")