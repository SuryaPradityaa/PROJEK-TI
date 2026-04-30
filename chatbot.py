"""
chatbot.py  –  BaliGuide AI (Versi Improved)
============================================
Fitur baru:
  - Sistem tanya-jawab bertahap (multi-turn) sebelum memberikan rekomendasi
  - State machine: GREETING → COLLECTING → CONFIRMING → RECOMMENDING → FOLLOWUP
  - Slot filling: mengumpulkan 5 dimensi preferensi dari user
  - Confidence scoring untuk memutuskan kapan rekomendasi layak diberikan
  - Fallback bertahap: jika informasi masih kurang, chatbot bertanya lebih lanjut
  - Model Naive Bayes + TF-IDF dengan data latih yang diperluas
"""

import re
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# ─────────────────────────────────────────────
# 1. LOAD DATASET
# ─────────────────────────────────────────────
df = pd.read_csv("dataset_wisata_bali.csv")

# ─────────────────────────────────────────────
# 2. KAMUS & MAPPING
# ─────────────────────────────────────────────
SYNONYMS = {
    "pantai": ["beach", "laut", "bahari", "tepi laut", "pesisir"],
    "alam":   ["nature", "outdoor", "pegunungan", "air terjun", "gunung", "hutan"],
    "budaya": ["culture", "adat", "tradisi", "sejarah", "pura", "temple"],
    "kuliner": ["makanan", "makan", "food", "restoran", "cafe", "warung", "seafood"],
    "hiburan": ["fun", "seru", "atraksi", "waterpark", "wahana", "taman"],
    "murah":  ["hemat", "gratis", "ekonomis", "terjangkau", "low budget"],
    "mahal":  ["premium", "mewah", "luxury", "eksklusif"],
    "rekomendasi": ["recommend", "saran", "pilihan", "rekomen"],
}

LOCATION_MAP = {
    "badung": "Badung", "seminyak": "Badung", "kuta": "Badung",
    "uluwatu": "Badung", "jimbaran": "Badung", "nusa dua": "Badung",
    "canggu": "Badung", "pecatu": "Badung",
    "ubud": "Gianyar", "gianyar": "Gianyar", "tegalalang": "Gianyar",
    "sukawati": "Gianyar",
    "denpasar": "Denpasar", "sanur": "Denpasar",
    "karangasem": "Karangasem", "amed": "Karangasem", "candidasa": "Karangasem",
    "buleleng": "Buleleng", "singaraja": "Buleleng", "lovina": "Buleleng",
    "tabanan": "Tabanan", "bedugul": "Tabanan", "jatiluwih": "Tabanan",
    "bangli": "Bangli", "kintamani": "Bangli",
    "klungkung": "Klungkung", "nusa penida": "Klungkung", "semarapura": "Klungkung",
    "jembrana": "Jembrana", "negara": "Jembrana",
}

CATEGORY_KEYWORDS = {
    "pantai":   ["pantai", "sunset", "snorkeling", "diving", "surfing", "berenang", "pasir", "beach", "laut"],
    "alam":     ["alam", "hiking", "trekking", "camping", "air terjun", "gunung", "sawah", "danau", "hutan"],
    "budaya":   ["budaya", "pura", "sejarah", "museum", "tari", "adat", "heritage", "religi", "temple"],
    "kuliner":  ["kuliner", "makan", "cafe", "restoran", "pasar", "souvenir", "oleh oleh", "seafood", "warung"],
    "hiburan":  ["hiburan", "waterpark", "rafting", "atv", "parasailing", "bermain", "dolphin", "wahana", "swing"],
}

BUDGET_PATTERNS = {
    "hemat":   ["hemat", "murah", "gratis", "terjangkau", "low budget", "budget terbatas", "tidak mahal", "ekonomis"],
    "sedang":  ["sedang", "cukup", "normal", "standar", "lumayan"],
    "premium": ["premium", "mewah", "luxury", "eksklusif", "mahal", "tidak masalah harganya", "uang bukan masalah"],
}

PROFILE_HINTS = {
    "hobbies": {
        "fotografi":    ["foto", "fotografi", "aesthetic", "instagramable", "berfoto", "tiktok", "konten"],
        "hiking":       ["hiking", "trekking", "gunung", "trail", "camping", "mendaki"],
        "kuliner":      ["kuliner", "makan", "cafe", "restoran", "food", "wisata kuliner"],
        "berenang":     ["berenang", "snorkeling", "diving", "water sport", "renang"],
        "healing":      ["healing", "tenang", "santai", "relaks", "sunrise", "meditasi"],
        "budaya":       ["budaya", "sejarah", "museum", "pura", "adat", "religi"],
        "petualangan":  ["petualangan", "rafting", "atv", "surfing", "adrenalin", "ekstrem"],
        "keluarga":     ["anak", "keluarga", "family", "ramah keluarga", "anak-anak"],
    },
    "mood_preferences": {
        "tenang":       ["tenang", "damai", "sepi", "relaks", "healing", "nyaman"],
        "seru":         ["seru", "rame", "aktif", "fun", "bermain", "ramai"],
        "romantis":     ["romantis", "honeymoon", "pasangan", "sunset", "berdua"],
        "petualangan":  ["petualangan", "adventure", "menantang", "adrenalin", "seru"],
        "keluarga":     ["keluarga", "anak", "family", "bersama keluarga"],
    },
    "trip_type": {
        "solo":       ["solo", "sendiri", "seorang diri"],
        "pasangan":   ["pasangan", "honeymoon", "romantis", "berdua", "couple"],
        "keluarga":   ["keluarga", "anak", "family", "bersama anak"],
        "rombongan":  ["rombongan", "grup", "teman-teman", "rame-rame", "group tour"],
    },
    "mobility_level": {
        "santai":  ["santai", "tidak capek", "pelan", "easy", "mudah"],
        "sedang":  ["sedang", "moderat", "lumayan"],
        "aktif":   ["aktif", "hiking", "trekking", "petualangan", "adventure", "mendaki"],
    },
}

AGE_PATTERNS = [
    (r"\b(anak|balita|anak kecil)\b",     "anak"),
    (r"\b(remaja|teen|teenager)\b",        "remaja"),
    (r"\b(dewasa muda|mahasiswa|20an|30an)\b", "dewasa"),
    (r"\b(keluarga muda|keluarga)\b",      "keluarga"),
    (r"\b(lansia|orang tua|senior|40an|50an)\b", "lansia"),
]

# ─────────────────────────────────────────────
# 3. TRAINING DATA YANG DIPERLUAS
# ─────────────────────────────────────────────
TRAINING_DATA = [
    # --- SALAM ---
    ("halo", "salam"), ("hai", "salam"), ("hello", "salam"),
    ("selamat pagi", "salam"), ("selamat siang", "salam"),
    ("hey", "salam"), ("hi", "salam"), ("hei", "salam"),
    ("apa kabar", "salam"), ("halo bali guide", "salam"),

    # --- PANTAI ---
    ("saya mau ke pantai", "pantai"), ("rekomendasi pantai di bali", "pantai"),
    ("pantai romantis", "pantai"), ("pantai untuk foto aesthetic", "pantai"),
    ("mau snorkeling", "pantai"), ("mau surfing", "pantai"),
    ("pantai pasir putih", "pantai"), ("sunset di pantai", "pantai"),
    ("pantai terbaik bali", "pantai"), ("mau lihat laut", "pantai"),
    ("pantai sepi dan tenang", "pantai"), ("diving di pantai", "pantai"),
    ("mau ke beach", "pantai"), ("pantai tersembunyi", "pantai"),
    ("ingin berenang di laut", "pantai"), ("wisata bahari", "pantai"),
    ("pantai untuk keluarga", "pantai"), ("mau liburan ke tepi laut", "pantai"),

    # --- ALAM ---
    ("wisata alam", "alam"), ("mau ke gunung", "alam"),
    ("air terjun bali", "alam"), ("trekking di bali", "alam"),
    ("hiking bali", "alam"), ("wisata pegunungan", "alam"),
    ("mau ke hutan", "alam"), ("pemandangan alam", "alam"),
    ("camping di bali", "alam"), ("mendaki gunung batur", "alam"),
    ("wisata sawah", "alam"), ("danau di bali", "alam"),
    ("mau ke air terjun", "alam"), ("sunrise di gunung", "alam"),
    ("petualangan alam bali", "alam"), ("river tubing", "alam"),
    ("taman nasional bali", "alam"), ("wisata outdoor", "alam"),
    ("healing di alam", "alam"), ("menikmati alam terbuka", "alam"),

    # --- BUDAYA ---
    ("wisata budaya", "budaya"), ("mau ke pura", "budaya"),
    ("museum bali", "budaya"), ("wisata sejarah", "budaya"),
    ("mau lihat tari kecak", "budaya"), ("pura di bali", "budaya"),
    ("wisata religi", "budaya"), ("tradisi bali", "budaya"),
    ("mau ke besakih", "budaya"), ("belajar budaya bali", "budaya"),
    ("wisata adat", "budaya"), ("seni budaya bali", "budaya"),
    ("arsitektur bali", "budaya"), ("pertunjukan seni", "budaya"),
    ("melukat di bali", "budaya"),

    # --- KULINER ---
    ("wisata kuliner", "kuliner"), ("mau cari makan", "kuliner"),
    ("cafe instagramable bali", "kuliner"), ("seafood bali", "kuliner"),
    ("kuliner lokal bali", "kuliner"), ("restoran romantis", "kuliner"),
    ("mau belanja oleh-oleh", "kuliner"), ("pasar tradisional bali", "kuliner"),
    ("makanan khas bali", "kuliner"), ("beli souvenir", "kuliner"),
    ("kopi bali", "kuliner"), ("warung makan bali", "kuliner"),

    # --- HIBURAN ---
    ("wisata hiburan", "hiburan"), ("liburan keluarga", "hiburan"),
    ("waterpark bali", "hiburan"), ("bali swing", "hiburan"),
    ("taman hiburan bali", "hiburan"), ("wahana bali", "hiburan"),
    ("rafting di bali", "hiburan"), ("atv bali", "hiburan"),
    ("mau ke waterbom", "hiburan"), ("gwk bali", "hiburan"),
    ("mau naik ayunan ekstrem", "hiburan"), ("seru-seruan di bali", "hiburan"),
    ("mau lihat lumba-lumba", "hiburan"), ("safari bali", "hiburan"),

    # --- MURAH / BUDGET ---
    ("wisata murah", "murah"), ("budget terbatas", "murah"),
    ("wisata gratis", "murah"), ("hemat di bali", "murah"),
    ("liburan low budget", "murah"), ("tiket murah bali", "murah"),
    ("tidak punya banyak uang", "murah"), ("cari yang ekonomis", "murah"),

    # --- TERBAIK ---
    ("tempat terbaik di bali", "terbaik"), ("wisata paling populer", "terbaik"),
    ("destinasi viral bali", "terbaik"), ("wajib dikunjungi", "terbaik"),
    ("tempat paling keren", "terbaik"), ("spot terfavorit", "terbaik"),
    ("bali paling terkenal", "terbaik"),

    # --- LOKASI ---
    ("wisata di badung", "lokasi_badung"), ("kuta bali", "lokasi_badung"),
    ("seminyak bali", "lokasi_badung"), ("uluwatu", "lokasi_badung"),
    ("wisata di ubud", "lokasi_gianyar"), ("gianyar", "lokasi_gianyar"),
    ("tegalalang", "lokasi_gianyar"),
    ("wisata di denpasar", "lokasi_denpasar"), ("sanur", "lokasi_denpasar"),
    ("wisata di karangasem", "lokasi_karangasem"), ("amed", "lokasi_karangasem"),
    ("wisata di buleleng", "lokasi_buleleng"), ("lovina", "lokasi_buleleng"),
    ("singaraja", "lokasi_buleleng"),
    ("wisata di tabanan", "lokasi_tabanan"), ("bedugul", "lokasi_tabanan"),
    ("wisata di bangli", "lokasi_bangli"), ("kintamani", "lokasi_bangli"),
    ("wisata di klungkung", "lokasi_klungkung"), ("nusa penida", "lokasi_klungkung"),
    ("wisata di jembrana", "lokasi_jembrana"),

    # --- LANJUT / LAINNYA ---
    ("ada lagi", "lanjut"), ("selain itu", "lanjut"), ("yang lain", "lanjut"),
    ("ada rekomendasi lain", "lanjut"), ("mau yang berbeda", "lanjut"),
    ("kasih alternatif lain", "lanjut"), ("opsi lain", "lanjut"),

    # --- TERIMA KASIH ---
    ("terima kasih", "terima_kasih"), ("makasih", "terima_kasih"),
    ("thanks", "terima_kasih"), ("thx", "terima_kasih"),
    ("oke bagus", "terima_kasih"), ("oke siap", "terima_kasih"),

    # --- BANTUAN / BINGUNG ---
    ("bingung mau ke mana", "bantuan"), ("tolong bantu", "bantuan"),
    ("rekomendasiin dong", "bantuan"), ("saya tidak tahu", "bantuan"),
    ("bantu saya pilih", "bantuan"), ("minta saran", "bantuan"),
    ("saran wisata bali", "bantuan"),

    # --- JAWABAN PROFIL (untuk slot filling) ---
    ("saya suka foto", "jawaban_profil"), ("saya senang hiking", "jawaban_profil"),
    ("budget saya 200rb", "jawaban_profil"), ("pergi berdua", "jawaban_profil"),
    ("bawa keluarga", "jawaban_profil"), ("mau yang tenang", "jawaban_profil"),
    ("saya suka petualangan", "jawaban_profil"), ("mood santai", "jawaban_profil"),
    ("saya dari badung", "jawaban_profil"), ("ingin ke ubud", "jawaban_profil"),
    ("mau yang sepi", "jawaban_profil"), ("mau yang ramai", "jawaban_profil"),
    ("pergi sama teman", "jawaban_profil"), ("honeymoon", "jawaban_profil"),
    ("solo traveling", "jawaban_profil"), ("tidak mau jauh-jauh", "jawaban_profil"),
    ("umur saya 25", "jawaban_profil"), ("remaja", "jawaban_profil"),
]

kalimat_train = [d[0] for d in TRAINING_DATA]
intent_train  = [d[1] for d in TRAINING_DATA]

model_chatbot = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
    ("clf",   MultinomialNB(alpha=0.05)),
])
model_chatbot.fit(kalimat_train, intent_train)


# ─────────────────────────────────────────────
# 4. HELPER FUNCTIONS
# ─────────────────────────────────────────────

def normalize_text(teks: str) -> str:
    return re.sub(r"\s+", " ", (teks or "").lower()).strip()

def preprocess_text(teks: str) -> str:
    teks = normalize_text(teks)
    for key, syns in SYNONYMS.items():
        for syn in syns:
            teks = teks.replace(syn, key)
    return re.sub(r"[^a-zA-Z0-9\s]", " ", teks)

def cek_keyword_lokasi(teks: str) -> str | None:
    teks = normalize_text(teks)
    for keyword, kabupaten in LOCATION_MAP.items():
        if keyword in teks:
            return kabupaten
    return None

def classify_budget(harga):
    try:
        harga = float(harga)
    except Exception:
        harga = 0
    if harga <= 20000:
        return "hemat"
    if harga <= 100000:
        return "sedang"
    return "premium"

def detect_intent(teks: str) -> str:
    proc = preprocess_text(teks)
    intent = model_chatbot.predict([proc])[0]
    proba  = model_chatbot.predict_proba([proc]).max()
    if proba < 0.20:
        return "bantuan"
    return intent

def infer_requested_category(teks: str) -> str | None:
    teks_norm = normalize_text(teks)
    scores = {kat: sum(1 for kw in kws if kw in teks_norm)
              for kat, kws in CATEGORY_KEYWORDS.items()}
    best, score = max(scores.items(), key=lambda x: x[1])
    return best if score > 0 else None

def extract_profile_from_text(teks: str) -> dict:
    teks_norm = normalize_text(teks)
    profile = {
        "age_range": "", "hobbies": [], "mood_preferences": [],
        "budget_level": "", "trip_type": "", "mobility_level": "",
        "preferred_locations": [],
    }
    for pattern, label in AGE_PATTERNS:
        if re.search(pattern, teks_norm):
            profile["age_range"] = label
            break
    for label, keywords in BUDGET_PATTERNS.items():
        if any(kw in teks_norm for kw in keywords):
            profile["budget_level"] = label
            break
    lokasi = cek_keyword_lokasi(teks_norm)
    if lokasi:
        profile["preferred_locations"] = [lokasi]
    for field in ("hobbies", "mood_preferences"):
        for label, keywords in PROFILE_HINTS[field].items():
            if any(kw in teks_norm for kw in keywords):
                profile[field].append(label)
    for label, keywords in PROFILE_HINTS["trip_type"].items():
        if any(kw in teks_norm for kw in keywords):
            profile["trip_type"] = label
            break
    for label, keywords in PROFILE_HINTS["mobility_level"].items():
        if any(kw in teks_norm for kw in keywords):
            profile["mobility_level"] = label
            break
    return profile

def merge_preferences(base: dict, override: dict) -> dict:
    merged = {
        "age_range":          base.get("age_range", "") or "",
        "hobbies":            list(base.get("hobbies", []) or []),
        "mood_preferences":   list(base.get("mood_preferences", []) or []),
        "budget_level":       base.get("budget_level", "") or "",
        "trip_type":          base.get("trip_type", "") or "",
        "mobility_level":     base.get("mobility_level", "") or "",
        "preferred_locations":list(base.get("preferred_locations", []) or []),
    }
    for key in ("age_range", "budget_level", "trip_type", "mobility_level"):
        if override.get(key):
            merged[key] = override[key]
    for key in ("hobbies", "mood_preferences", "preferred_locations"):
        extra = override.get(key, []) or []
        merged[key] = list(dict.fromkeys(merged[key] + extra))
    return merged


# ─────────────────────────────────────────────
# 5. SLOT FILLING & CONVERSATION STATE
# ─────────────────────────────────────────────

# Slot yang harus diisi sebelum rekomendasi diberikan
SLOTS_REQUIRED = ["trip_type", "budget_level", "mood_preferences", "hobbies"]

# Pertanyaan untuk setiap slot yang belum terisi
SLOT_QUESTIONS = {
    "trip_type": [
        "Oke! Kamu pergi sama siapa nih? 👥\n"
        "- Sendiri (solo)\n"
        "- Berdua / pasangan\n"
        "- Bareng keluarga dengan anak-anak\n"
        "- Rombongan / grup teman",

        "Perjalanan ini buat siapa? Sendiri, berdua, keluarga, atau rombongan teman? 😊",
    ],
    "budget_level": [
        "Kira-kira budget per orang untuk tiket masuk ya? 💸\n"
        "- Hemat (di bawah Rp 20.000)\n"
        "- Sedang (Rp 20.000 – Rp 100.000)\n"
        "- Premium (di atas Rp 100.000, no problemo!)",

        "Soal budget, maunya yang gimana? Hemat, sedang, atau premium boleh? 💰",
    ],
    "mood_preferences": [
        "Suasana seperti apa yang lagi kamu cari? 🌿\n"
        "- Tenang & healing (jauh dari keramaian)\n"
        "- Seru & ramai (penuh aktivitas)\n"
        "- Romantis (cocok buat pasangan)\n"
        "- Petualangan (adrenalin!)\n"
        "- Keluarga (ramah anak)",

        "Lagi mau suasana yang gimana? Santai, seru, romantis, atau penuh petualangan? ✨",
    ],
    "hobbies": [
        "Aktivitas apa yang paling kamu suka? 🎯\n"
        "- Foto-foto / konten (instagramable)\n"
        "- Hiking / trekking\n"
        "- Kuliner & belanja\n"
        "- Berenang / water sport\n"
        "- Sejarah & budaya\n"
        "- Healing & meditasi\n"
        "- Petualangan ekstrem",

        "Kalau lagi liburan, kamu lebih suka ngapain? Foto-foto, jalan-jalan alam, kuliner, atau apa? 🤔",
    ],
    "preferred_locations": [
        "Ada area favorit di Bali? 📍\n"
        "Misalnya: Ubud, Seminyak/Kuta, Nusa Penida, Buleleng, Karangasem, dll.\n"
        "Kalau tidak ada preferensi, bilang 'bebas' ya!",

        "Mau di area mana di Bali? Atau bebas, nanti saya cariin yang terbaik! 🗺️",
    ],
}

def get_missing_slots(prefs: dict) -> list:
    """Kembalikan daftar slot penting yang belum terisi."""
    missing = []
    if not prefs.get("trip_type"):
        missing.append("trip_type")
    if not prefs.get("budget_level"):
        missing.append("budget_level")
    if not prefs.get("mood_preferences"):
        missing.append("mood_preferences")
    if not prefs.get("hobbies"):
        missing.append("hobbies")
    return missing

def get_preference_confidence(prefs: dict) -> int:
    """Hitung skor kelengkapan preferensi (0-100)."""
    score = 0
    if prefs.get("trip_type"):         score += 25
    if prefs.get("budget_level"):      score += 25
    if prefs.get("mood_preferences"):  score += 25
    if prefs.get("hobbies"):           score += 15
    if prefs.get("preferred_locations"): score += 10
    return score

def ask_next_slot(prefs: dict, context: dict) -> str | None:
    """Kembalikan pertanyaan untuk slot berikutnya, atau None jika semua sudah terisi."""
    missing = get_missing_slots(prefs)
    if not missing:
        return None
    slot = missing[0]
    questions = SLOT_QUESTIONS.get(slot, [])
    already_asked = context.get("asked_slots", [])
    # Pilih pertanyaan yang bervariasi
    idx = already_asked.count(slot) % len(questions)
    return questions[idx]

def ekstrak_konteks(riwayat: list) -> dict:
    """Ekstrak semua informasi relevan dari riwayat percakapan."""
    konteks = {
        "intent_terakhir":    None,
        "lokasi_terakhir":    None,
        "hasil_terakhir":     [],
        "profil_percakapan":  {
            "age_range": "", "hobbies": [], "mood_preferences": [],
            "budget_level": "", "trip_type": "", "mobility_level": "",
            "preferred_locations": [],
        },
        "pertanyaan_terakhir": None,
        "asked_slots":        [],
        "rekomendasi_diberikan": False,
        "jumlah_pesan_user":  0,
    }
    if not riwayat:
        return konteks

    for pesan in riwayat:
        if pesan.get("role") == "user":
            konteks["jumlah_pesan_user"] += 1
            override = extract_profile_from_text(pesan.get("content", ""))
            konteks["profil_percakapan"] = merge_preferences(
                konteks["profil_percakapan"], override
            )
            lokasi = cek_keyword_lokasi(pesan.get("content", ""))
            if lokasi:
                konteks["lokasi_terakhir"] = lokasi
            teks = preprocess_text(pesan.get("content", ""))
            try:
                intent = model_chatbot.predict([teks])[0]
                if intent not in {"salam", "bantuan", "terima_kasih", "jawaban_profil"}:
                    konteks["intent_terakhir"] = intent
            except Exception:
                pass

        elif pesan.get("role") == "assistant":
            content = pesan.get("content", "")
            # Tandai slot yang sudah ditanyakan
            for slot in SLOT_QUESTIONS:
                for q in SLOT_QUESTIONS[slot]:
                    if q[:40] in content:
                        konteks["asked_slots"].append(slot)
                        break
            # Cek apakah rekomendasi sudah pernah diberikan
            if "Rekomendasi" in content and "<b>" in content:
                konteks["rekomendasi_diberikan"] = True
            # Ambil nama tempat yang sudah direkomendasikan
            for match in re.finditer(r"<b>\s*\d+\.\s*(.*?)\s*</b>", content):
                nama = match.group(1).strip()
                if nama:
                    konteks["hasil_terakhir"].append(nama)

    return konteks


# ─────────────────────────────────────────────
# 6. SCORING & REKOMENDASI
# ─────────────────────────────────────────────

def infer_place_profile(row):
    teks = normalize_text(
        f"{row.get('kategori','')} {row.get('deskripsi','')} {row.get('aktivitas','')} {row.get('nama_tempat','')}"
    )
    kategori = normalize_text(str(row.get("kategori", "")))
    hobbies    = [n for n, kws in PROFILE_HINTS["hobbies"].items() if any(k in teks for k in kws)]
    moods      = [n for n, kws in PROFILE_HINTS["mood_preferences"].items() if any(k in teks for k in kws)]
    trip_types = [n for n, kws in PROFILE_HINTS["trip_type"].items() if any(k in teks for k in kws)]
    mobility   = "aktif" if any(k in teks for k in ["hiking","trekking","rafting","atv","surfing","camping","mendaki"]) else "santai"
    if any(k in teks for k in ["bersepeda","berenang","walking","jalan santai"]):
        mobility = "sedang"
    if "taman hiburan" in kategori and "keluarga" not in trip_types:
        trip_types.append("keluarga")
    age_fit = "keluarga" if "keluarga" in teks or "anak" in teks else "dewasa"
    if "lansia" in teks or "tenang" in teks:
        age_fit = "lansia"
    return {
        "hobbies": hobbies, "moods": moods, "trip_types": trip_types,
        "mobility": mobility, "age_fit": age_fit,
        "budget_level": classify_budget(row.get("harga_tiket_wni", 0)),
    }

df["profile_tags"] = df.apply(infer_place_profile, axis=1)

def score_row(row, preferences, kategori_target=None, lokasi_target=None, exclude_names=None):
    if exclude_names and row["nama_tempat"] in exclude_names:
        return None
    score = float(row.get("rating", 0)) * 8
    kategori  = normalize_text(str(row.get("kategori", "")))
    kabupaten = normalize_text(str(row.get("kabupaten", "")))
    teks = normalize_text(f"{row.get('deskripsi','')} {row.get('aktivitas','')} {row.get('nama_tempat','')}")
    tags = row.get("profile_tags", {})

    if kategori_target:
        kategori_map = {
            "pantai": "pantai", "alam": "alam", "budaya": "budaya",
            "kuliner": "kuliner & belanja", "hiburan": "taman hiburan",
        }
        if kategori_map.get(kategori_target, kategori_target) == kategori:
            score += 45
        elif any(kw in teks for kw in CATEGORY_KEYWORDS.get(kategori_target, [])):
            score += 20
        else:
            score -= 15

    if lokasi_target:
        if normalize_text(lokasi_target) in kabupaten:
            score += 25
        else:
            score -= 5

    # Budget matching
    if preferences.get("budget_level"):
        place_budget = tags.get("budget_level")
        if place_budget == preferences["budget_level"]:
            score += 20
        elif preferences["budget_level"] == "hemat" and place_budget == "sedang":
            score += 5
        elif preferences["budget_level"] == "premium" and place_budget == "hemat":
            score -= 8

    # Hobi matching
    hobbies = preferences.get("hobbies", [])
    score += sum(12 for h in hobbies if h in tags.get("hobbies", []))

    # Mood matching
    moods = preferences.get("mood_preferences", [])
    score += sum(10 for m in moods if m in tags.get("moods", []))

    # Trip type matching
    trip_type = preferences.get("trip_type")
    if trip_type and trip_type in tags.get("trip_types", []):
        score += 12

    # Mobility matching
    mobility = preferences.get("mobility_level")
    if mobility:
        if mobility == tags.get("mobility"):
            score += 10
        elif mobility == "santai" and tags.get("mobility") == "aktif":
            score -= 12

    # Usia
    age_range = preferences.get("age_range")
    if age_range:
        if age_range == tags.get("age_fit"):
            score += 8
        elif age_range == "lansia" and tags.get("mobility") == "aktif":
            score -= 15

    # Lokasi preferensi
    pref_locs = [normalize_text(l) for l in preferences.get("preferred_locations", [])]
    if pref_locs and any(l in kabupaten for l in pref_locs):
        score += 15

    return score

def get_ranked_recommendations(preferences, kategori_target=None, lokasi_target=None,
                                exclude_names=None, top=4):
    scored = []
    for _, row in df.iterrows():
        s = score_row(row, preferences, kategori_target, lokasi_target, exclude_names)
        if s is not None:
            scored.append((s, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [row for _, row in scored[:top]]

def format_tempat(row, idx=None):
    nomor = f"{idx}." if idx else "-"
    return (
        f"<b>{nomor} {row['nama_tempat']}</b><br>"
        f"<b>Lokasi:</b> {row['kabupaten']}<br>"
        f"<b>Kategori:</b> {row['kategori']}<br>"
        f"<b>Rating:</b> ⭐ {row['rating']}<br>"
        f"<b>Tiket WNI:</b> {'Gratis' if float(row['harga_tiket_wni']) == 0 else f'Rp{int(row[chr(104)+chr(97)+chr(114)+chr(103)+chr(97)+chr(95)+chr(116)+chr(105)+chr(107)+chr(101)+chr(116)+chr(95)+chr(119)+chr(110)+chr(105)]):,}'}<br>"
        f"<b>Jam Buka:</b> {row['jam_buka']} (WITA)<br>"
        f"<b>Aktivitas:</b> {row['aktivitas']}<br>"
        f"<b>Deskripsi:</b> {str(row['deskripsi'])[:160]}..."
    )

def format_tempat(row, idx=None):
    nomor = f"{idx}." if idx else "-"
    harga = float(row.get("harga_tiket_wni", 0))
    harga_str = "Gratis" if harga == 0 else f"Rp{int(harga):,}"
    return (
        f"<b>{nomor} {row['nama_tempat']}</b><br>"
        f"<b>Lokasi:</b> {row['kabupaten']}<br>"
        f"<b>Kategori:</b> {row['kategori']}<br>"
        f"<b>Rating:</b> ⭐ {row['rating']}<br>"
        f"<b>Tiket WNI:</b> {harga_str}<br>"
        f"<b>Jam Buka:</b> {row['jam_buka']} (WITA)<br>"
        f"<b>Aktivitas:</b> {row['aktivitas']}<br>"
        f"<b>Deskripsi:</b> {str(row['deskripsi'])[:160]}..."
    )

def build_recommendation_response(judul, hasil, preferences, suffix=""):
    if not hasil:
        return (
            "Hmm, saya belum menemukan destinasi yang pas untuk kriteria itu. 😕\n\n"
            "Coba ceritakan lagi preferensimu — misalnya ubah area, budget, atau suasana yang dicari."
        )
    lines = [f"✨ <b>{judul}</b>\n\n"]
    for idx, row in enumerate(hasil, 1):
        lines.append(format_tempat(row, idx))
        if idx < len(hasil):
            lines.append("\n[PLACE_SEPARATOR]\n")

    summary = []
    if preferences.get("trip_type"):         summary.append(f"perjalanan {preferences['trip_type']}")
    if preferences.get("mood_preferences"):  summary.append(f"suasana {', '.join(preferences['mood_preferences'][:2])}")
    if preferences.get("budget_level"):      summary.append(f"budget {preferences['budget_level']}")
    if preferences.get("hobbies"):           summary.append(f"hobi {', '.join(preferences['hobbies'][:2])}")
    if summary:
        lines.append(f"\n\n*📋 Rekomendasi berdasarkan: {', '.join(summary)}.*")
    if suffix:
        lines.append(suffix)
    lines.append("\n\n💡 Ada yang mau ditanyakan lebih lanjut? Atau mau saya carikan alternatif lain?")
    return "".join(lines)


# ─────────────────────────────────────────────
# 7. MAIN CHAT LOGIC  (State Machine)
# ─────────────────────────────────────────────

def chat_ml(pesan_user: str, riwayat: list = None, preferences: dict = None) -> str:
    """
    State Machine:
      GREETING     → sapaan awal, mulai tanya
      COLLECTING   → kumpulkan slot preferensi satu per satu
      RECOMMENDING → berikan rekomendasi
      FOLLOWUP     → tindak lanjut / refinement
    """
    if riwayat is None:
        riwayat = []
    if preferences is None:
        preferences = {}

    teks       = pesan_user.strip()
    teks_lower = normalize_text(teks)
    konteks    = ekstrak_konteks(riwayat)

    # Gabung preferensi: DB → riwayat → pesan baru
    merged_prefs = merge_preferences(preferences, konteks["profil_percakapan"])
    merged_prefs = merge_preferences(merged_prefs, extract_profile_from_text(teks))

    intent   = detect_intent(teks)
    lokasi   = cek_keyword_lokasi(teks_lower) or konteks.get("lokasi_terakhir")
    kategori = infer_requested_category(teks) or konteks.get("intent_terakhir")
    exclude  = konteks.get("hasil_terakhir") or None
    confidence = get_preference_confidence(merged_prefs)
    jumlah_pesan = konteks.get("jumlah_pesan_user", 0)

    # ── TERIMA KASIH ──────────────────────────────────────────
    if intent == "terima_kasih":
        return random.choice([
            "Sama-sama! 😊 Semoga liburannya menyenangkan ya!\n\nKalau mau cari tempat lain atau punya pertanyaan, saya siap bantu.",
            "Senang bisa membantu! 🌟 Selamat berlibur di Bali!\n\nKalau butuh rekomendasi lagi, kabari saya ya.",
        ])

    # ── LANJUT / ALTERNATIF ───────────────────────────────────
    if intent == "lanjut" and konteks.get("rekomendasi_diberikan"):
        hasil = get_ranked_recommendations(
            merged_prefs, kategori_target=kategori,
            lokasi_target=lokasi, exclude_names=exclude, top=4,
        )
        return build_recommendation_response(
            "Rekomendasi Alternatif untuk Kamu", hasil, merged_prefs,
            "\n\n*Ini adalah pilihan lain dari preferensi sebelumnya.*"
        )

    # ── SALAM / GREETING ─────────────────────────────────────
    if intent == "salam" and jumlah_pesan == 0:
        return (
            "Halo! Selamat datang di <b>BaliGuide AI</b> 🌴\n\n"
            "Saya siap bantu kamu menemukan destinasi wisata Bali yang paling cocok!\n\n"
            "Sebelum saya kasih rekomendasi, boleh saya tanya beberapa hal dulu? "
            "Supaya rekomendasinya benar-benar pas buat kamu. 😊\n\n"
            + SLOT_QUESTIONS["trip_type"][0]
        )

    # ── TANYA-JAWAB PENGUMPULAN PREFERENSI (SLOT FILLING) ────
    # Cek slot mana yang belum terisi
    missing_slots = get_missing_slots(merged_prefs)
    sudah_ada_intent_wisata = intent in {
        "pantai","alam","budaya","kuliner","hiburan","murah","terbaik",
        "lokasi_badung","lokasi_gianyar","lokasi_denpasar","lokasi_karangasem",
        "lokasi_buleleng","lokasi_tabanan","lokasi_bangli","lokasi_klungkung",
        "lokasi_jembrana",
    } or kategori is not None

    # Jika ada intent wisata atau user bertanya untuk pertama kali
    # dan confidence masih rendah → tanya dulu
    if sudah_ada_intent_wisata and confidence < 50 and jumlah_pesan <= 6:
        pertanyaan = ask_next_slot(merged_prefs, konteks)
        if pertanyaan:
            # Acknowledge dulu pesan user
            ack = ""
            if intent in {"pantai","alam","budaya","kuliner","hiburan"}:
                labels = {"pantai":"pantai","alam":"alam/pegunungan","budaya":"budaya","kuliner":"kuliner","hiburan":"hiburan"}
                ack = f"Oke, kamu tertarik wisata <b>{labels.get(intent,intent)}</b>! 👍\n\n"
            elif lokasi:
                ack = f"Area <b>{lokasi}</b> ya, siap!\n\n"
            return ack + "Sebelum saya rekomendasikan, boleh tanya dulu:\n\n" + pertanyaan

    # Jika jawaban profil diterima dan masih ada slot kosong → lanjut tanya
    if intent == "jawaban_profil" and missing_slots:
        pertanyaan = ask_next_slot(merged_prefs, konteks)
        if pertanyaan:
            return "Noted! 📝\n\n" + pertanyaan

    # Semua slot terisi ATAU user sudah memberi cukup info → rekomendasikan
    # Juga rekomendasikan jika user sudah menjawab > 4 kali (sabar menunggu)
    if confidence >= 50 or not missing_slots or jumlah_pesan > 6:
        # Jika budget murah, set ke hemat
        if intent == "murah":
            merged_prefs["budget_level"] = "hemat"

        if intent == "terbaik":
            hasil = get_ranked_recommendations(
                merged_prefs, kategori_target=kategori,
                lokasi_target=lokasi, exclude_names=exclude, top=5,
            )
            return build_recommendation_response(
                "Top Destinasi Terbaik untuk Kamu", hasil, merged_prefs
            )

        hasil = get_ranked_recommendations(
            merged_prefs, kategori_target=kategori,
            lokasi_target=lokasi, exclude_names=exclude, top=4,
        )
        if kategori and lokasi:
            judul = f"Rekomendasi {kategori.title()} di {lokasi} untuk Kamu"
        elif kategori:
            judul = f"Rekomendasi {kategori.title()} Terbaik untuk Kamu"
        elif lokasi:
            judul = f"Destinasi Terbaik di {lokasi} untuk Kamu"
        else:
            judul = "Rekomendasi Wisata Personal untuk Kamu"

        return build_recommendation_response(judul, hasil, merged_prefs)

    # Fallback: jika belum punya info apapun, mulai tanya
    if not any(merged_prefs.values()):
        return (
            "Hai! Saya BaliGuide AI 🌴\n\n"
            "Untuk memberikan rekomendasi yang paling cocok, "
            "saya perlu kenalan dulu sedikit. 😊\n\n"
            + SLOT_QUESTIONS["trip_type"][0]
        )

    # Fallback terakhir: tanya slot berikutnya
    pertanyaan = ask_next_slot(merged_prefs, konteks)
    if pertanyaan:
        return pertanyaan

    # Jika semua sudah terjawab
    hasil = get_ranked_recommendations(
        merged_prefs, kategori_target=kategori,
        lokasi_target=lokasi, exclude_names=exclude, top=4,
    )
    return build_recommendation_response("Rekomendasi untuk Kamu", hasil, merged_prefs)


def chat_response(pesan_user: str, riwayat: list = None, preferences: dict = None) -> str:
    return chat_ml(pesan_user, riwayat, preferences)