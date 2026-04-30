"""
COMPARISON: Model Lama vs Model Improved
Lihat perbedaan performa dengan/tanpa preprocessing
"""

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# ========================
# SETUP DATA
# ========================
df = pd.read_csv("dataset_wisata_bali.csv")

# Sinonim dictionary
synonyms = {
    "pantai": ["tepi laut", "pesisir", "pantay", "laut"],
    "gunung": ["bukit", "pegunungan"],
    "berenang": ["mandi", "renang", "diving", "snorkeling"],
    "bagus": ["indah", "cantik", "menarik", "seru", "keren"],
    "liburan": ["libur", "traveling"],
    "murah": ["hemat", "ekonomis"],
    "terbaik": ["terkenal", "paling bagus"],
}

# Setup stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def preprocess_text(text):
    """Full preprocessing dengan stemming + sinonim"""
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

# ========================
# TRAINING DATA (SAMA UNTUK DAYA)
# ========================
training_data = [
    # PANTAI
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
    
    # ALAM
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
    
    # BUDAYA
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
    
    # KULINER
    ("wisata kuliner", "kuliner"),
    ("mau belanja", "kuliner"),
    ("pasar oleh oleh", "kuliner"),
    ("makanan khas bali", "kuliner"),
    ("tempat makan bali", "kuliner"),
    ("belanja souvenir", "kuliner"),
    ("pasar tradisional", "kuliner"),
    ("oleh oleh bali", "kuliner"),
    
    # HIBURAN
    ("wisata hiburan", "hiburan"),
    ("taman bermain", "hiburan"),
    ("tempat seru", "hiburan"),
    ("mau seru seruan", "hiburan"),
    ("wahana permainan", "hiburan"),
    
    # MURAH
    ("wisata murah", "murah"),
    ("tempat gratis bali", "murah"),
    ("liburan hemat", "murah"),
    ("budget terbatas", "murah"),
    ("tiket murah", "murah"),
    
    # TERBAIK
    ("tempat terbaik di bali", "terbaik"),
    ("wisata paling populer", "terbaik"),
    ("rekomendasi terbaik", "terbaik"),
    ("rating tertinggi", "terbaik"),
    
    # SALAM
    ("halo", "salam"),
    ("hai", "salam"),
    ("hello", "salam"),
    ("selamat pagi", "salam"),
]

kalimat_train = [d[0] for d in training_data]
intent_train = [d[1] for d in training_data]

# ========================
# MODEL 1: LAMA (TANPA PREPROCESSING)
# ========================
print("=" * 60)
print("TRAINING MODEL LAMA (Tanpa Preprocessing)")
print("=" * 60)

model_lama = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
    ('clf', MultinomialNB(alpha=0.1))
])
model_lama.fit(kalimat_train, intent_train)

# ========================
# MODEL 2: BARU (DENGAN PREPROCESSING)
# ========================
print("\nTRAINING MODEL BARU (Dengan Preprocessing)")

kalimat_train_processed = [preprocess_text(k) for k in kalimat_train]

model_baru = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        lowercase=True
    )),
    ('clf', MultinomialNB(alpha=0.1))
])
model_baru.fit(kalimat_train_processed, intent_train)
print("✓ Model baru dilatih")

# ========================
# TEST CASES (VARIASI KATA)
# ========================
test_cases = [
    # Original intent
    ("mau ke pantai", "pantai"),
    ("wisata kuliner", "kuliner"),
    ("tempat murah", "murah"),
    
    # Sinonim yang BELUM ada di training data
    ("mau ke tepi laut", "pantai"),          # sinonim: tepi laut = pantai
    ("mau ke pesisir", "pantai"),            # sinonim: pesisir = pantai
    ("mau menyelam", "pantai"),              # sinonim: menyelam = snorkeling
    
    # Variasi kata
    ("kuliner bali enak", "kuliner"),        # tambah kata "enak"
    ("liburan murah", "murah"),              # ganti: hemat -> liburan
    ("tempat yang hemat", "murah"),          # sinonim: hemat = murah
    
    # Typo/variasi
    ("pantay bagus", "pantai"),              # typo: pantay -> pantai
    ("mau ke pantai yg bagus", "pantai"),    # abbrev: yg -> yang
]

# ========================
# TESTING & COMPARISON
# ========================
print("\n" + "=" * 100)
print("COMPARISON RESULTS")
print("=" * 100)

correct_lama = 0
correct_baru = 0

print(f"\n{'Input':<35} | {'Expected':<12} | {'Model Lama':<12} | {'Model Baru':<12} | {'Status':<15}")
print("-" * 100)

for test_input, expected in test_cases:
    pred_lama = model_lama.predict([test_input])[0]
    pred_baru = model_baru.predict([preprocess_text(test_input)])[0]
    
    # Confidence scores
    conf_lama = max(model_lama.predict_proba([test_input])[0])
    conf_baru = max(model_baru.predict_proba([preprocess_text(test_input)])[0])
    
    correct_lama += (pred_lama == expected)
    correct_baru += (pred_baru == expected)
    
    status = "✓ Keduanya" if (pred_lama == expected and pred_baru == expected) else \
             "✓ Baru lebih baik" if (pred_baru == expected and pred_lama != expected) else \
             "✓ Sama-sama benar" if (pred_lama == expected and pred_baru == expected) else \
             "✗ Keduanya salah"
    
    print(f"{test_input:<35} | {expected:<12} | {pred_lama:<12} | {pred_baru:<12} | {status:<15}")
    
    # Show confidence jika ada perbedaan
    if pred_lama != pred_baru:
        print(f"  └─ Confidence Lama: {conf_lama:.2f} | Confidence Baru: {conf_baru:.2f}")

# ========================
# SUMMARY
# ========================
print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)

accuracy_lama = (correct_lama / len(test_cases)) * 100
accuracy_baru = (correct_baru / len(test_cases)) * 100

print(f"\nModel Lama (Tanpa Preprocessing):")
print(f"  Akurasi: {correct_lama}/{len(test_cases)} ({accuracy_lama:.1f}%)")

print(f"\nModel Baru (Dengan Preprocessing):")
print(f"  Akurasi: {correct_baru}/{len(test_cases)} ({accuracy_baru:.1f}%)")

improvement = accuracy_baru - accuracy_lama
print(f"\n🚀 Peningkatan: {improvement:+.1f}%")

# ========================
# EXAMPLE: Confidence Scoring
# ========================
print("\n" + "=" * 100)
print("EXAMPLE: CONFIDENCE SCORING")
print("=" * 100)

example_input = "mau mandi di pantai yang sepi"
processed = preprocess_text(example_input)

print(f"\nInput: '{example_input}'")
print(f"Processed: '{processed}'")

pred = model_baru.predict([processed])[0]
proba = model_baru.predict_proba([processed])[0]

print(f"\nPrediction: {pred}")
print("\nProbability per intent:")

# Get intent names dari training
intents = model_baru.named_steps['clf'].classes_
for intent, prob in zip(intents, proba):
    bar = "█" * int(prob * 50) + "░" * (50 - int(prob * 50))
    print(f"  {intent:<15}: {prob:.3f} [{bar}]")
