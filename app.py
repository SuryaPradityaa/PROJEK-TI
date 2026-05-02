from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import pandas as pd
import pymysql
import bcrypt
import os
from chatbot import chat_response
import json

# KONFIGURASI DATABASE MySQL

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "wisata_bali"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_db():
    return pymysql.connect(**DB_CONFIG)


def clean_value(value):
    if pd.isna(value):
        return None
    return value


def seed_wisata_records(conn):
    with conn.cursor() as c:
        c.execute("SELECT COUNT(*) AS total FROM wisata")
        count_row = c.fetchone() or {"total": 0}
        if count_row.get("total", 0) > 0:
            return

        insert_rows = []
        for _, row in df.iterrows():
            insert_rows.append(
                (
                    int(clean_value(row.get("id") or 0)),
                    clean_value(row.get("nama_tempat")),
                    clean_value(row.get("kategori")),
                    clean_value(row.get("kabupaten")),
                    clean_value(row.get("deskripsi")),
                    float(clean_value(row.get("rating") or 0)),
                    clean_value(row.get("harga_tiket_wni")),
                    clean_value(row.get("harga_tiket_wna")),
                    clean_value(row.get("jam_buka")),
                    clean_value(row.get("aktivitas")),
                    (
                        float(clean_value(row.get("latitude") or 0))
                        if clean_value(row.get("latitude")) is not None
                        else None
                    ),
                    (
                        float(clean_value(row.get("longitude") or 0))
                        if clean_value(row.get("longitude")) is not None
                        else None
                    ),
                )
            )

        c.executemany(
            "INSERT INTO wisata (id, nama_tempat, kategori, kabupaten, deskripsi, rating, harga_tiket_wni, harga_tiket_wna, jam_buka, aktivitas, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            insert_rows,
        )


def get_wisata_rows(tempat="", kategori="", sort="rating"):
    conn = get_db()
    try:
        seed_wisata_records(conn)
        with conn.cursor() as c:
            query = "SELECT id, nama_tempat, kategori, kabupaten, deskripsi, rating, harga_tiket_wni, harga_tiket_wna, jam_buka, aktivitas, latitude, longitude FROM wisata WHERE 1"
            params = []
            if tempat:
                query += " AND nama_tempat LIKE %s"
                params.append(f"%{tempat}%")
            if kategori:
                query += " AND kategori LIKE %s"
                params.append(f"%{kategori}%")

            if sort == "harga_terendah":
                query += " ORDER BY (harga_tiket_wni IS NULL), harga_tiket_wni ASC"
            elif sort == "harga_tertinggi":
                query += " ORDER BY (harga_tiket_wni IS NULL), harga_tiket_wni DESC"
            else:
                query += " ORDER BY rating DESC"

            c.execute(query, tuple(params))
            return c.fetchall()
    finally:
        conn.close()


def get_wisata_detail(wisata_id):
    conn = get_db()
    try:
        seed_wisata_records(conn)
        with conn.cursor() as c:
            c.execute(
                "SELECT id, nama_tempat, kategori, kabupaten, deskripsi, rating, harga_tiket_wni, harga_tiket_wna, jam_buka, aktivitas, latitude, longitude FROM wisata WHERE id = %s",
                (wisata_id,),
            )
            return c.fetchone()
    finally:
        conn.close()


def admin_required(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "admin":
            return jsonify({"message": "Akses admin dibutuhkan"}), 403
        return func(*args, **kwargs)

    return wrapper


def parse_json_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def normalize_preferences_row(row):
    if not row:
        return {
            "age_range": "",
            "hobbies": [],
            "mood_preferences": [],
            "budget_level": "",
            "trip_type": "",
            "mobility_level": "",
            "preferred_locations": [],
        }
    return {
        "age_range": row.get("age_range") or "",
        "hobbies": parse_json_list(row.get("hobbies")),
        "mood_preferences": parse_json_list(row.get("mood_preferences")),
        "budget_level": row.get("budget_level") or "",
        "trip_type": row.get("trip_type") or "",
        "mobility_level": row.get("mobility_level") or "",
        "preferred_locations": parse_json_list(row.get("preferred_locations")),
    }


# LOAD DATASET
df = pd.read_csv("dataset_wisata_bali.csv")

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "ganti-dengan-secret-key-acak-yang-panjang"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# REGISTER
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(silent=True) or {}

        nama = data.get("nama", "").strip()
        gmail = data.get("gmail", "").strip()
        password = data.get("password", "")

        # Validasi input
        if not nama or not gmail or not password:
            return jsonify({"message": "Semua field wajib diisi"}), 400
        if len(password) < 6:
            return jsonify({"message": "Password minimal 6 karakter"}), 400
        if "@" not in gmail:
            return jsonify({"message": "Format gmail tidak valid"}), 400

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        conn = get_db()
        try:
            with conn.cursor() as c:
                # AMAN: nama tabel adalah konstanta, nilai pakai %s
                c.execute("SELECT id FROM users WHERE nama = %s", (nama,))
                if c.fetchone():
                    return jsonify({"message": "Nama sudah digunakan"}), 400

                c.execute("SELECT id FROM users WHERE gmail = %s", (gmail,))
                if c.fetchone():
                    return jsonify({"message": "Gmail sudah digunakan"}), 400

                c.execute(
                    "INSERT INTO users (nama, gmail, password, role) VALUES (%s, %s, %s, %s)",
                    (nama, gmail, hashed, "user"),
                )
                conn.commit()
        finally:
            conn.close()

        return jsonify({"message": "Register berhasil"})

    except Exception as e:
        print("REGISTER ERROR:", e)
        return jsonify({"message": "Terjadi error"}), 500


# LOGIN
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(silent=True) or {}

        nama = data.get("nama", "").strip()
        password = data.get("password", "")

        if not nama or not password:
            return jsonify({"message": "Nama dan password wajib diisi"}), 400

        conn = get_db()
        try:
            with conn.cursor() as c:
                # AMAN: query statis, nilai pakai %s
                c.execute(
                    "SELECT id, password, role FROM users WHERE nama = %s", (nama,)
                )
                user = c.fetchone()
        finally:
            conn.close()

        if user:
            stored_password = user["password"].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), stored_password):
                session["user_id"] = user["id"]
                session["role"] = user.get("role", "user")
                return jsonify({"message": "Login berhasil"})

        # Pesan error yang sama untuk nama salah maupun password salah
        # (hindari user enumeration attack)
        return jsonify({"message": "Nama atau password salah"}), 401

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"message": "Terjadi error login"}), 500


# SESSION CHECK + PROFILE
@app.route("/me")
def me():
    if "user_id" not in session:
        return jsonify({"message": "Belum login"}), 401
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT id, nama, gmail, role, tanggal_lahir, jenis_kelamin, foto_profil "
                "FROM users WHERE id = %s",
                (session["user_id"],),
            )
            user = c.fetchone()
    finally:
        conn.close()
    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404
    if user.get("tanggal_lahir"):
        user["tanggal_lahir"] = str(user["tanggal_lahir"])
    return jsonify(user)


@app.route("/profile", methods=["PUT"])
def update_profile():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    data = request.get_json(silent=True) or {}
    tanggal_lahir = data.get("tanggal_lahir", None)
    jenis_kelamin = data.get("jenis_kelamin", None)
    foto_profil = data.get("foto_profil", None)

    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "UPDATE users SET tanggal_lahir=%s, jenis_kelamin=%s, foto_profil=%s WHERE id=%s",
                (tanggal_lahir, jenis_kelamin, foto_profil, session["user_id"]),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Profil berhasil diperbarui"})


@app.route("/profile-page")
def profile_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("profile.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logout berhasil"})


# HALAMAN LOGIN
@app.route("/login-page")
def login_page():
    if "user_id" in session:
        return redirect(url_for("ui"))
    return render_template("login.html")


@app.route("/admin-login-page")
def admin_login_page():
    if "user_id" in session and session.get("role") == "admin":
        return redirect(url_for("admin_page"))
    return render_template("admin_login.html")


# UI (PROTECTED)
@app.route("/ui")
def ui():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("index.html")


# HOME
@app.route("/")
def home():
    return "API Rekomendasi Wisata Bali aktif."


# KATEGORI
@app.route("/kategori")
def get_kategori():
    conn = get_db()
    try:
        seed_wisata_records(conn)
        with conn.cursor() as c:
            c.execute(
                "SELECT DISTINCT kategori FROM wisata WHERE kategori IS NOT NULL AND kategori <> '' ORDER BY kategori"
            )
            rows = c.fetchall()
    finally:
        conn.close()
    return jsonify([r["kategori"] for r in rows])


# REKOMENDASI (PROTECTED)
@app.route("/rekomendasi")
def get_rekomendasi():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401

    tempat = request.args.get("tempat", "").strip()
    kategori = request.args.get("kategori", "").strip()
    sort = request.args.get("sort", "rating").strip()

    hasil = get_wisata_rows(tempat, kategori, sort)
    if not hasil:
        return jsonify({"message": "Tempat tidak ditemukan"})

    return jsonify(
        [
            {
                "id": row.get("id"),
                "nama_tempat": row.get("nama_tempat", ""),
                "kategori": row.get("kategori", ""),
                "kabupaten": row.get("kabupaten", ""),
                "rating": float(row.get("rating", 0) or 0),
                "latitude": float(row.get("latitude") or 0),
                "longitude": float(row.get("longitude") or 0),
                "deskripsi": row.get("deskripsi", ""),
                "aktivitas": row.get("aktivitas", ""),
                "harga_tiket_wni": row.get("harga_tiket_wni", ""),
                "harga_tiket_wna": row.get("harga_tiket_wna", ""),
                "jam_buka": row.get("jam_buka", ""),
            }
            for row in hasil
        ]
    )


# DETAIL WISATA
@app.route("/wisata/<int:wisata_id>")
def get_wisata_by_id(wisata_id):
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401

    row = get_wisata_detail(wisata_id)
    if not row:
        return jsonify({"message": "Wisata tidak ditemukan"}), 404

    return jsonify(
        {
            "id": row.get("id"),
            "nama_tempat": row.get("nama_tempat", ""),
            "kategori": row.get("kategori", ""),
            "kabupaten": row.get("kabupaten", ""),
            "deskripsi": row.get("deskripsi", ""),
            "rating": float(row.get("rating", 0) or 0),
            "harga_tiket_wni": row.get("harga_tiket_wni", ""),
            "harga_tiket_wna": row.get("harga_tiket_wna", ""),
            "jam_buka": row.get("jam_buka", ""),
            "aktivitas": row.get("aktivitas", ""),
            "latitude": float(row.get("latitude") or 0),
            "longitude": float(row.get("longitude") or 0),
        }
    )


# RUTE WISATA
@app.route("/rute")
def get_route():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401

    nama_tempat = request.args.get("nama_tempat", "").strip()
    if not nama_tempat:
        return jsonify({"message": "nama_tempat wajib diisi"}), 400

    conn = get_db()
    try:
        seed_wisata_records(conn)
        with conn.cursor() as c:
            c.execute(
                "SELECT id, nama_tempat, latitude, longitude, kabupaten, kategori FROM wisata WHERE nama_tempat LIKE %s LIMIT 1",
                (f"%{nama_tempat}%",),
            )
            row = c.fetchone()
    finally:
        conn.close()

    if not row:
        return jsonify({"message": "Wisata tidak ditemukan untuk rute"}), 404

    return jsonify(
        {
            "id": row.get("id"),
            "nama_tempat": row.get("nama_tempat"),
            "latitude": float(row.get("latitude") or 0),
            "longitude": float(row.get("longitude") or 0),
            "kabupaten": row.get("kabupaten", ""),
            "kategori": row.get("kategori", ""),
        }
    )


# ULASAN WISATA
@app.route("/ulasan", methods=["GET"])
def get_ulasan():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401

    wisata_id = request.args.get("wisata_id", None)
    conn = get_db()
    try:
        seed_wisata_records(conn)
        with conn.cursor() as c:
            if wisata_id:
                c.execute(
                    "SELECT u.id, u.user_id, u.wisata_id, u.rating, u.komentar, u.created_at, w.nama_tempat FROM ulasan u LEFT JOIN wisata w ON u.wisata_id = w.id WHERE u.wisata_id = %s ORDER BY u.created_at DESC",
                    (wisata_id,),
                )
                rows = c.fetchall()
                return jsonify(rows)
            c.execute(
                "SELECT u.id, u.wisata_id, u.rating, u.komentar, u.created_at, w.nama_tempat FROM ulasan u LEFT JOIN wisata w ON u.wisata_id = w.id WHERE u.user_id = %s ORDER BY u.created_at DESC",
                (session["user_id"],),
            )
            rows = c.fetchall()
    finally:
        conn.close()
    return jsonify(rows)


@app.route("/ulasan", methods=["POST"])
def tambah_ulasan():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401

    data = request.get_json(silent=True) or {}
    wisata_id = data.get("wisata_id")
    rating = data.get("rating")
    komentar = data.get("komentar", "").strip()

    if not wisata_id:
        return jsonify({"message": "wisata_id wajib diisi"}), 400

    try:
        wisata_id = int(wisata_id)
    except ValueError:
        return jsonify({"message": "wisata_id tidak valid"}), 400

    try:
        rating = int(rating) if rating is not None else None
        if rating is not None and (rating < 1 or rating > 5):
            return jsonify({"message": "Rating harus antara 1 sampai 5"}), 400
    except (TypeError, ValueError):
        return jsonify({"message": "Rating tidak valid"}), 400

    conn = get_db()
    try:
        seed_wisata_records(conn)
        with conn.cursor() as c:
            c.execute("SELECT id FROM wisata WHERE id = %s", (wisata_id,))
            if not c.fetchone():
                return jsonify({"message": "Wisata tidak ditemukan"}), 404
            c.execute(
                "INSERT INTO ulasan (user_id, wisata_id, rating, komentar) VALUES (%s, %s, %s, %s)",
                (session["user_id"], wisata_id, rating, komentar),
            )
            conn.commit()
    finally:
        conn.close()

    return jsonify({"message": "Ulasan berhasil disimpan"})


# ADMIN LOGIN
@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    nama = data.get("nama", "").strip()
    password = data.get("password", "")

    if not nama or not password:
        return jsonify({"message": "Nama dan password wajib diisi"}), 400

    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT id, password FROM users WHERE nama = %s AND role = 'admin'",
                (nama,),
            )
            user = c.fetchone()
    finally:
        conn.close()

    if user and bcrypt.checkpw(
        password.encode("utf-8"), user["password"].encode("utf-8")
    ):
        session["user_id"] = user["id"]
        session["role"] = "admin"
        return jsonify({"message": "Login admin berhasil"})

    return jsonify({"message": "Nama atau password admin salah"}), 401


# ADMIN PAGE
@app.route("/admin-page")
def admin_page():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("admin_login_page"))
    return render_template("admin.html")


# ADMIN WISATA CRUD
@app.route("/admin/wisata", methods=["GET"])
@admin_required
def admin_list_wisata():
    conn = get_db()
    try:
        seed_wisata_records(conn)
        with conn.cursor() as c:
            c.execute(
                "SELECT id, nama_tempat, kategori, kabupaten, rating, harga_tiket_wni, harga_tiket_wna, jam_buka, aktivitas, latitude, longitude FROM wisata ORDER BY id DESC"
            )
            rows = c.fetchall()
    finally:
        conn.close()
    return jsonify(rows)


@app.route("/admin/wisata", methods=["POST"])
@admin_required
def admin_create_wisata():
    data = request.get_json(silent=True) or {}
    nama_tempat = data.get("nama_tempat", "").strip()
    if not nama_tempat:
        return jsonify({"message": "nama_tempat wajib diisi"}), 400

    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO wisata (nama_tempat, kategori, kabupaten, deskripsi, rating, harga_tiket_wni, harga_tiket_wna, jam_buka, aktivitas, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    nama_tempat,
                    data.get("kategori", "").strip(),
                    data.get("kabupaten", "").strip(),
                    data.get("deskripsi", "").strip(),
                    float(data.get("rating") or 0),
                    data.get("harga_tiket_wni", "").strip(),
                    data.get("harga_tiket_wna", "").strip(),
                    data.get("jam_buka", "").strip(),
                    data.get("aktivitas", "").strip(),
                    float(data.get("latitude") or 0),
                    float(data.get("longitude") or 0),
                ),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Data wisata berhasil ditambahkan"})


@app.route("/admin/wisata/<int:wisata_id>", methods=["PUT"])
@admin_required
def admin_update_wisata(wisata_id):
    data = request.get_json(silent=True) or {}
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute("SELECT id FROM wisata WHERE id = %s", (wisata_id,))
            if not c.fetchone():
                return jsonify({"message": "Wisata tidak ditemukan"}), 404
            c.execute(
                "UPDATE wisata SET nama_tempat=%s, kategori=%s, kabupaten=%s, deskripsi=%s, rating=%s, harga_tiket_wni=%s, harga_tiket_wna=%s, jam_buka=%s, aktivitas=%s, latitude=%s, longitude=%s WHERE id=%s",
                (
                    data.get("nama_tempat", "").strip(),
                    data.get("kategori", "").strip(),
                    data.get("kabupaten", "").strip(),
                    data.get("deskripsi", "").strip(),
                    float(data.get("rating") or 0),
                    data.get("harga_tiket_wni", "").strip(),
                    data.get("harga_tiket_wna", "").strip(),
                    data.get("jam_buka", "").strip(),
                    data.get("aktivitas", "").strip(),
                    float(data.get("latitude") or 0),
                    float(data.get("longitude") or 0),
                    wisata_id,
                ),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Data wisata berhasil diperbarui"})


@app.route("/admin/wisata/<int:wisata_id>", methods=["DELETE"])
@admin_required
def admin_delete_wisata(wisata_id):
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute("DELETE FROM wisata WHERE id = %s", (wisata_id,))
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Data wisata berhasil dihapus"})


# SUKA / FAVORIT (PROTECTED)
@app.route("/suka", methods=["GET"])
def get_suka():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    user_id = session["user_id"]
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute("SELECT nama_tempat FROM suka WHERE user_id = %s", (user_id,))
            rows = c.fetchall()
    finally:
        conn.close()
    return jsonify([r["nama_tempat"] for r in rows])


@app.route("/suka", methods=["POST"])
def tambah_suka():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    data = request.get_json(silent=True) or {}
    nama_tempat = data.get("nama_tempat", "").strip()
    if not nama_tempat:
        return jsonify({"message": "nama_tempat wajib diisi"}), 400
    user_id = session["user_id"]
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT id FROM suka WHERE user_id = %s AND nama_tempat = %s",
                (user_id, nama_tempat),
            )
            if c.fetchone():
                return jsonify({"message": "Sudah ada di favorit"})
            c.execute(
                "INSERT INTO suka (user_id, nama_tempat) VALUES (%s, %s)",
                (user_id, nama_tempat),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Berhasil ditambahkan ke favorit"})


@app.route("/suka", methods=["DELETE"])
def hapus_suka():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    data = request.get_json(silent=True) or {}
    nama_tempat = data.get("nama_tempat", "").strip()
    user_id = session["user_id"]
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "DELETE FROM suka WHERE user_id = %s AND nama_tempat = %s",
                (user_id, nama_tempat),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Dihapus dari favorit"})


# RIWAYAT KUNJUNGAN (PROTECTED)
@app.route("/riwayat", methods=["GET"])
def get_riwayat():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    user_id = session["user_id"]
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT nama_tempat, kategori, kabupaten, rating, tanggal_kunjungan, catatan "
                "FROM riwayat_kunjungan WHERE user_id = %s ORDER BY tanggal_kunjungan DESC",
                (user_id,),
            )
            rows = c.fetchall()
    finally:
        conn.close()
    # Convert date to string
    for r in rows:
        if r.get("tanggal_kunjungan"):
            r["tanggal_kunjungan"] = str(r["tanggal_kunjungan"])
    return jsonify(rows)


@app.route("/riwayat", methods=["POST"])
def tambah_riwayat():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    data = request.get_json(silent=True) or {}
    nama_tempat = data.get("nama_tempat", "").strip()
    kategori = data.get("kategori", "").strip()
    kabupaten = data.get("kabupaten", "").strip()
    rating = data.get("rating", 0)
    catatan = data.get("catatan", "").strip()
    if not nama_tempat:
        return jsonify({"message": "nama_tempat wajib diisi"}), 400
    user_id = session["user_id"]
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO riwayat_kunjungan (user_id, nama_tempat, kategori, kabupaten, rating, catatan) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, nama_tempat, kategori, kabupaten, rating, catatan),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Riwayat kunjungan berhasil disimpan"})


@app.route("/riwayat/<int:riwayat_id>", methods=["DELETE"])
def hapus_riwayat(riwayat_id):
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    user_id = session["user_id"]
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "DELETE FROM riwayat_kunjungan WHERE id = %s AND user_id = %s",
                (riwayat_id, user_id),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Riwayat dihapus"})


# CHATBOT (PROTECTED)
@app.route("/chatbot", methods=["POST"])
def chatbot():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401

    try:
        data = request.get_json(silent=True) or {}
        pesan = data.get("pesan", "").strip()
        riwayat = data.get("riwayat", [])

        if not pesan:
            return jsonify({"balasan": "Pesan tidak boleh kosong."}), 400

        # Batasi panjang pesan untuk cegah abuse
        if len(pesan) > 500:
            return (
                jsonify({"balasan": "Pesan terlalu panjang (maks 500 karakter)."}),
                400,
            )

        conn = get_db()
        try:
            with conn.cursor() as c:
                c.execute(
                    "SELECT age_range, hobbies, mood_preferences, budget_level, trip_type, mobility_level, preferred_locations "
                    "FROM user_preferences WHERE user_id = %s",
                    (session["user_id"],),
                )
                pref_row = c.fetchone()
        finally:
            conn.close()

        preferences = normalize_preferences_row(pref_row)
        balasan = chat_response(pesan, riwayat, preferences)
        return jsonify({"balasan": balasan})

    except Exception as e:
        print("CHATBOT ERROR:", e)
        return jsonify({"balasan": "Maaf, layanan pesan sementara tidak tersedia."}), 500


@app.route("/chatbot/session", methods=["GET"])
def get_chatbot_session():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    user_id = session["user_id"]
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT has_visited_dashboard FROM chatbot_sessions WHERE user_id = %s",
                (user_id,),
            )
            row = c.fetchone()
            if not row:
                c.execute(
                    "INSERT INTO chatbot_sessions (user_id, has_visited_dashboard) VALUES (%s, %s)",
                    (user_id, 0),
                )
                conn.commit()
                row = {"has_visited_dashboard": 0}
    finally:
        conn.close()
    return jsonify({"has_visited_dashboard": bool(row.get("has_visited_dashboard"))})


@app.route("/chatbot/session", methods=["PUT"])
def update_chatbot_session():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}
    has_visited_dashboard = bool(data.get("has_visited_dashboard", False))
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO chatbot_sessions (user_id, has_visited_dashboard)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE has_visited_dashboard = VALUES(has_visited_dashboard)
                """,
                (user_id, int(has_visited_dashboard)),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Status sesi chatbot diperbarui"})


@app.route("/chatbot/history", methods=["GET"])
def get_chatbot_history():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    user_id = session["user_id"]
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT role, content FROM chatbot_messages WHERE user_id = %s ORDER BY id ASC",
                (user_id,),
            )
            rows = c.fetchall()
    finally:
        conn.close()
    return jsonify(rows)


@app.route("/chatbot/history", methods=["POST"])
def save_chatbot_history():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}
    riwayat = data.get("riwayat", [])
    if not isinstance(riwayat, list):
        return jsonify({"message": "Format riwayat tidak valid"}), 400
    sanitized = []
    for item in riwayat[-100:]:
        role = str(item.get("role", "")).strip()
        content = str(item.get("content", "")).strip()
        if role not in ("user", "assistant") or not content:
            continue
        if len(content) > 2000:
            content = content[:2000]
        sanitized.append((user_id, role, content))

    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute("DELETE FROM chatbot_messages WHERE user_id = %s", (user_id,))
            if sanitized:
                c.executemany(
                    "INSERT INTO chatbot_messages (user_id, role, content) VALUES (%s, %s, %s)",
                    sanitized,
                )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Riwayat chatbot tersimpan"})


@app.route("/preferences", methods=["GET"])
def get_preferences():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT age_range, hobbies, mood_preferences, budget_level, trip_type, mobility_level, preferred_locations "
                "FROM user_preferences WHERE user_id = %s",
                (session["user_id"],),
            )
            row = c.fetchone()
    finally:
        conn.close()
    return jsonify(normalize_preferences_row(row))


@app.route("/preferences", methods=["PUT"])
def update_preferences():
    if "user_id" not in session:
        return jsonify({"message": "Harus login dulu"}), 401

    data = request.get_json(silent=True) or {}
    age_range = str(data.get("age_range", "")).strip()
    hobbies = data.get("hobbies", [])
    mood_preferences = data.get("mood_preferences", [])
    budget_level = str(data.get("budget_level", "")).strip()
    trip_type = str(data.get("trip_type", "")).strip()
    mobility_level = str(data.get("mobility_level", "")).strip()
    preferred_locations = data.get("preferred_locations", [])

    if (
        not isinstance(hobbies, list)
        or not isinstance(mood_preferences, list)
        or not isinstance(preferred_locations, list)
    ):
        return jsonify({"message": "Format preferensi tidak valid"}), 400

    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO user_preferences (
                    user_id, age_range, hobbies, mood_preferences, budget_level, trip_type, mobility_level, preferred_locations
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    age_range = VALUES(age_range),
                    hobbies = VALUES(hobbies),
                    mood_preferences = VALUES(mood_preferences),
                    budget_level = VALUES(budget_level),
                    trip_type = VALUES(trip_type),
                    mobility_level = VALUES(mobility_level),
                    preferred_locations = VALUES(preferred_locations)
                """,
                (
                    session["user_id"],
                    age_range,
                    json.dumps(hobbies, ensure_ascii=True),
                    json.dumps(mood_preferences, ensure_ascii=True),
                    budget_level,
                    trip_type,
                    mobility_level,
                    json.dumps(preferred_locations, ensure_ascii=True),
                ),
            )
            conn.commit()
    finally:
        conn.close()
    return jsonify({"message": "Preferensi berhasil diperbarui"})


# RUN
if __name__ == "__main__":
    # debug=False di production!
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
