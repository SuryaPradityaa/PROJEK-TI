import os
import requests
import pandas as pd
import time
import re
import json
from datetime import datetime

# ─────────────────────────────────────────
# ⚙️  KONFIGURASI — GANTI DI SINI
# ─────────────────────────────────────────
OPENTRIPMAP_API_KEY = os.environ.get(
    "OPENTRIPMAP_API_KEY", "MASUKKAN_API_KEY_ANDA_DI_SINI"
)  # Daftar di opentripmap.io
OUTPUT_FILE = "dataset_wisata_bali_baru.csv"
MAX_TEMPAT = 200  # Berapa banyak tempat yang ingin diambil
DELAY_ANTAR_REQUEST = 0.5  # Jeda antar request (detik) — jangan terlalu cepat

# ─────────────────────────────────────────
# 🗺️  KABUPATEN DI BALI (koordinat tengah)
# ─────────────────────────────────────────
KABUPATEN_BALI = [
    {"nama": "Badung", "lat": -8.5816, "lon": 115.1671, "radius": 20000},
    {"nama": "Gianyar", "lat": -8.5319, "lon": 115.3268, "radius": 15000},
    {"nama": "Denpasar", "lat": -8.6705, "lon": 115.2126, "radius": 10000},
    {"nama": "Tabanan", "lat": -8.5400, "lon": 115.1200, "radius": 20000},
    {"nama": "Karangasem", "lat": -8.4536, "lon": 115.5800, "radius": 20000},
    {"nama": "Buleleng", "lat": -8.1116, "lon": 115.0892, "radius": 30000},
    {"nama": "Bangli", "lat": -8.4561, "lon": 115.3560, "radius": 15000},
    {"nama": "Klungkung", "lat": -8.5397, "lon": 115.4049, "radius": 15000},
    {"nama": "Jembrana", "lat": -8.3592, "lon": 114.6203, "radius": 20000},
]

# ─────────────────────────────────────────
# 📦  MAPPING KATEGORI OpenTripMap → Sistem
# ─────────────────────────────────────────
KATEGORI_MAP = {
    "beaches": "Pantai",
    "water": "Pantai",
    "natural": "Alam",
    "gardens": "Alam",
    "waterfalls": "Alam",
    "mountains": "Alam",
    "lakes": "Alam",
    "national_parks": "Alam",
    "religion": "Budaya",
    "historic": "Budaya",
    "cultural": "Budaya",
    "archaeology": "Budaya",
    "architecture": "Budaya",
    "museums": "Budaya",
    "amusements": "Taman Hiburan",
    "sport": "Taman Hiburan",
    "foods": "Kuliner & Belanja",
    "shops": "Kuliner & Belanja",
    "markets": "Kuliner & Belanja",
    "tourist_facilities": "Alam",
}

# Aktivitas default per kategori
AKTIVITAS_DEFAULT = {
    "Pantai": "Bersantai, berenang, berfoto, snorkeling",
    "Alam": "Trekking, berfoto, menikmati alam",
    "Budaya": "Wisata budaya, berfoto, wisata sejarah",
    "Taman Hiburan": "Bermain, berfoto, hiburan keluarga",
    "Kuliner & Belanja": "Makan, belanja oleh-oleh, wisata kuliner",
}

JAM_BUKA_DEFAULT = "08.00-17.00"


# ═════════════════════════════════════════
# BAGIAN 1: OPENTRIPMAP API
# ═════════════════════════════════════════


def otm_get_places(lat, lon, radius, limit=50):
    """
    Ambil daftar tempat wisata dari OpenTripMap berdasarkan koordinat.
    Docs: https://dev.opentripmap.org/docs
    """
    url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "apikey": OPENTRIPMAP_API_KEY,
        "radius": radius,
        "lon": lon,
        "lat": lat,
        "kinds": "interesting_places",  # Semua tempat menarik
        "rate": "2",  # Minimal popularitas (1=rendah, 3=tinggi)
        "format": "json",
        "limit": limit,
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"    ⚠️  OTM radius error: {e}")
        return []


def otm_get_detail(xid):
    """
    Ambil detail satu tempat dari OpenTripMap berdasarkan xid (ID unik).
    """
    url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
    params = {"apikey": OPENTRIPMAP_API_KEY}
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"    ⚠️  OTM detail error ({xid}): {e}")
        return {}


def parse_kategori(kinds_str):
    """Konversi kinds string OpenTripMap ke kategori sistem kita."""
    if not kinds_str:
        return "Alam"
    kinds = kinds_str.lower().split(",")
    for kind in kinds:
        kind = kind.strip()
        for key, kat in KATEGORI_MAP.items():
            if key in kind:
                return kat
    return "Alam"  # default


# ═════════════════════════════════════════
# BAGIAN 2: WIKIPEDIA API
# ═════════════════════════════════════════


def wiki_get_deskripsi(nama_tempat, kabupaten="Bali"):
    """
    Cari deskripsi dari Wikipedia Bahasa Indonesia.
    Docs: https://www.mediawiki.org/wiki/API:Search
    """
    # Coba beberapa variasi query
    queries = [
        f"{nama_tempat} Bali",
        f"{nama_tempat} {kabupaten}",
        nama_tempat,
    ]

    for query in queries:
        url = "https://id.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 1,
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            hasil = data.get("query", {}).get("search", [])

            if hasil:
                # Ambil snippet/ringkasan
                snippet = hasil[0].get("snippet", "")
                # Bersihkan tag HTML dari Wikipedia
                snippet = re.sub(r"<[^>]+>", "", snippet)
                snippet = snippet.replace("&quot;", '"').replace("&amp;", "&")
                snippet = snippet.strip()

                if len(snippet) > 50:  # Pastikan deskripsi cukup panjang
                    # Coba ambil intro artikel yang lebih lengkap
                    title = hasil[0].get("title", "")
                    intro = wiki_get_intro(title)
                    if intro:
                        return intro
                    return snippet

        except Exception as e:
            pass  # Lanjut ke query berikutnya

        time.sleep(0.3)

    return ""  # Tidak ditemukan


def wiki_get_intro(title):
    """Ambil paragraf pembuka artikel Wikipedia (lebih lengkap dari snippet)."""
    url = "https://id.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "format": "json",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            extract = page.get("extract", "").strip()
            if extract and len(extract) > 50:
                # Ambil 2 kalimat pertama saja
                kalimat = re.split(r"(?<=[.!?])\s+", extract)
                dua_kalimat = " ".join(kalimat[:2])
                if len(dua_kalimat) > 30:
                    return dua_kalimat[:400]  # Maksimal 400 karakter
    except Exception:
        pass
    return ""


# ═════════════════════════════════════════
# BAGIAN 3: PROSES UTAMA
# ═════════════════════════════════════════


def tentukan_kabupaten(lat, lon):
    """Tentukan kabupaten berdasarkan koordinat (approx bounding box)."""
    bounds = {
        "Jembrana": {"lat": (-8.6, -8.1), "lon": (114.4, 115.0)},
        "Buleleng": {"lat": (-8.3, -7.9), "lon": (114.5, 115.7)},
        "Tabanan": {"lat": (-8.7, -8.3), "lon": (114.9, 115.2)},
        "Badung": {"lat": (-8.8, -8.5), "lon": (115.1, 115.3)},
        "Denpasar": {"lat": (-8.8, -8.6), "lon": (115.1, 115.3)},
        "Gianyar": {"lat": (-8.6, -8.3), "lon": (115.2, 115.5)},
        "Bangli": {"lat": (-8.5, -8.2), "lon": (115.2, 115.5)},
        "Klungkung": {"lat": (-8.6, -8.4), "lon": (115.3, 115.6)},
        "Karangasem": {"lat": (-8.6, -8.2), "lon": (115.4, 115.7)},
    }
    for kab, b in bounds.items():
        if b["lat"][0] <= lat <= b["lat"][1] and b["lon"][0] <= lon <= b["lon"][1]:
            return kab
    return "Bali"  # Fallback


def hitung_rating_dari_stars(stars):
    """Konversi stars OTM (0-3) ke rating (3.5-5.0)."""
    mapping = {0: 3.5, 1: 3.8, 2: 4.2, 3: 4.6}
    return mapping.get(int(stars) if stars else 0, 3.5)


def generate_harga(kategori):
    """Generate estimasi harga tiket berdasarkan kategori."""
    harga_map = {
        "Pantai": (0, 0),
        "Alam": (15000, 25000),
        "Budaya": (20000, 30000),
        "Taman Hiburan": (50000, 100000),
        "Kuliner & Belanja": (0, 0),
    }
    return harga_map.get(kategori, (10000, 20000))


def proses_scraping():
    """Fungsi utama: ambil data dari semua kabupaten Bali."""
    print("=" * 60)
    print("  SCRAPER WISATA BALI - OpenTripMap + Wikipedia API")
    print("=" * 60)
    print(f"  Target: {MAX_TEMPAT} tempat wisata")
    print(f"  Output: {OUTPUT_FILE}")
    print("=" * 60)

    if OPENTRIPMAP_API_KEY == "MASUKKAN_API_KEY_ANDA_DI_SINI":
        print("\n❌ ERROR: API Key belum diisi!")
        print("   Daftar gratis di: https://opentripmap.io/register")
        print("   Lalu isi OPENTRIPMAP_API_KEY di bagian atas script ini.")
        return

    semua_data = []
    nama_sudah_ada = set()
    id_counter = 1

    for kab_info in KABUPATEN_BALI:
        kab_nama = kab_info["nama"]
        print(f"\n📍 Mengambil data: {kab_nama}")
        print(
            f"   Koordinat: ({kab_info['lat']}, {kab_info['lon']}), radius: {kab_info['radius']}m"
        )

        # Ambil daftar tempat dari OpenTripMap
        places = otm_get_places(
            lat=kab_info["lat"],
            lon=kab_info["lon"],
            radius=kab_info["radius"],
            limit=30,  # Ambil 30 tempat per kabupaten
        )

        if not places:
            print(f"   ⚠️  Tidak ada data untuk {kab_nama}")
            continue

        print(f"   ✅ Ditemukan {len(places)} tempat")

        for place in places:
            if len(semua_data) >= MAX_TEMPAT:
                print(f"\n✅ Target {MAX_TEMPAT} tempat tercapai!")
                break

            try:
                # Ambil data dasar
                xid = place.get("xid", "")
                nama = place.get("name", "").strip()
                lat = place.get("point", {}).get("lat", 0)
                lon = place.get("point", {}).get("lon", 0)
                kinds = place.get("kinds", "")
                stars = place.get("rate", 0)

                # Skip jika nama kosong atau sudah ada
                if not nama or nama in nama_sudah_ada:
                    continue

                # Skip nama yang terlalu pendek atau aneh
                if len(nama) < 3 or nama.isdigit():
                    continue

                nama_sudah_ada.add(nama)

                # Ambil detail (koordinat lebih akurat, dll)
                print(f"   → [{id_counter}] {nama}...", end="", flush=True)
                time.sleep(DELAY_ANTAR_REQUEST)

                detail = otm_get_detail(xid) if xid else {}

                # Koordinat final
                if detail.get("point"):
                    lat = detail["point"].get("lat", lat)
                    lon = detail["point"].get("lon", lon)

                # Tentukan kabupaten dari koordinat
                kabupaten = tentukan_kabupaten(lat, lon)

                # Kategori
                kinds_detail = detail.get("kinds", kinds)
                kategori = parse_kategori(kinds_detail)

                # Rating
                stars_detail = detail.get("rate", stars)
                rating = hitung_rating_dari_stars(stars_detail)

                # Harga tiket
                harga_wni, harga_wna = generate_harga(kategori)

                # Aktivitas
                aktivitas = AKTIVITAS_DEFAULT.get(
                    kategori, "Berfoto, menikmati suasana"
                )

                # Jam buka
                jam_buka = JAM_BUKA_DEFAULT
                if "wikipedia" in detail:
                    # Beberapa entry OTM punya info tambahan
                    pass

                # Deskripsi dari Wikipedia
                deskripsi = ""
                if detail.get("wikipedia_extracts", {}).get("text"):
                    # OTM terkadang sudah menyertakan extract Wikipedia
                    raw = detail["wikipedia_extracts"]["text"]
                    kalimat = re.split(r"(?<=[.!?])\s+", raw.strip())
                    deskripsi = " ".join(kalimat[:2])[:400]

                if not deskripsi:
                    # Cari ke Wikipedia API secara terpisah
                    deskripsi = wiki_get_deskripsi(nama, kabupaten)

                if not deskripsi:
                    deskripsi = f"Tempat wisata {kategori.lower()} yang menarik di {kabupaten}, Bali."

                # Simpan ke list
                semua_data.append(
                    {
                        "id": id_counter,
                        "nama_tempat": nama,
                        "kategori": kategori,
                        "kabupaten": kabupaten,
                        "deskripsi": deskripsi,
                        "rating": rating,
                        "harga_tiket_wni": harga_wni,
                        "harga_tiket_wna": harga_wna,
                        "jam_buka": jam_buka,
                        "aktivitas": aktivitas,
                        "latitude": round(lat, 4),
                        "longitude": round(lon, 4),
                    }
                )

                id_counter += 1
                print(f" ✅ ({kategori})")

            except Exception as e:
                print(f" ❌ Error: {e}")
                continue

        if len(semua_data) >= MAX_TEMPAT:
            break

    # ── Simpan ke CSV ──
    if semua_data:
        df_baru = pd.DataFrame(semua_data)
        df_baru.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

        print("\n" + "=" * 60)
        print(f"  ✅ SELESAI! {len(semua_data)} tempat wisata berhasil disimpan")
        print(f"  📄 File: {OUTPUT_FILE}")
        print(f"  📊 Distribusi kategori:")
        for kat, jml in df_baru["kategori"].value_counts().items():
            print(f"     • {kat}: {jml} tempat")
        print(f"  🗺️  Distribusi kabupaten:")
        for kab, jml in df_baru["kabupaten"].value_counts().items():
            print(f"     • {kab}: {jml} tempat")
        print("=" * 60)

        return df_baru
    else:
        print("\n❌ Tidak ada data yang berhasil diambil.")
        return None


# ═════════════════════════════════════════
# BAGIAN 4: MERGE DENGAN DATASET LAMA
# ═════════════════════════════════════════


def merge_dataset(file_lama="dataset_wisata_bali.csv", file_baru=OUTPUT_FILE):
    """
    Fungsi opsional: merge dataset baru dengan yang lama, hapus duplikat.
    Jalankan setelah proses_scraping() selesai dan Anda sudah review hasilnya.
    """
    try:
        df_lama = pd.read_csv(file_lama, encoding="utf-8-sig")
        df_baru = pd.read_csv(file_baru, encoding="utf-8-sig")

        print(f"\n📊 Dataset lama: {len(df_lama)} baris")
        print(f"📊 Dataset baru: {len(df_baru)} baris")

        # Gabungkan
        df_gabung = pd.concat([df_lama, df_baru], ignore_index=True)

        # Hapus duplikat berdasarkan nama_tempat (case-insensitive)
        df_gabung["nama_lower"] = df_gabung["nama_tempat"].str.lower().str.strip()
        df_gabung = df_gabung.drop_duplicates(subset=["nama_lower"], keep="first")
        df_gabung = df_gabung.drop(columns=["nama_lower"])

        # Reset ID
        df_gabung["id"] = range(1, len(df_gabung) + 1)

        output_merge = "dataset_wisata_bali_MERGED.csv"
        df_gabung.to_csv(output_merge, index=False, encoding="utf-8-sig")

        print(f"✅ Merge selesai! Total: {len(df_gabung)} baris")
        print(f"📄 Disimpan ke: {output_merge}")
        print(f"💡 Review dulu file ini, lalu ganti nama jadi dataset_wisata_bali.csv")

        return df_gabung

    except FileNotFoundError as e:
        print(f"❌ File tidak ditemukan: {e}")
        return None


# ═════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════

if __name__ == "__main__":
    print("\nMemulai scraping data wisata Bali...\n")

    # LANGKAH 1: Scraping data baru
    hasil = proses_scraping()

    # LANGKAH 2 (Opsional): Uncomment baris di bawah untuk merge dengan dataset lama
    # Pastikan file dataset_wisata_bali.csv ada di folder yang sama
    merge_dataset()

    print("\n📝 LANGKAH SELANJUTNYA:")
    print("   1. Cek file:", OUTPUT_FILE)
    print("   2. Review data (hapus yang tidak relevan)")
    print("   3. Jalankan merge_dataset() untuk gabungkan dengan data lama")
    print("   4. Ganti nama hasil merge jadi dataset_wisata_bali.csv")
    print("   5. Restart Flask app Anda")
