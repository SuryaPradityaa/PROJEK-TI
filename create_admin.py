import pymysql
import bcrypt
import os

# Konfigurasi database (sama seperti di app.py)
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "wisata_bali"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def create_admin_account(nama, gmail, password_plain):
    # Hash password dengan bcrypt
    hashed = bcrypt.hashpw(password_plain.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    # Connect ke DB
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as c:
            # Cek apakah nama atau gmail sudah ada
            c.execute(
                "SELECT id FROM users WHERE nama = %s OR gmail = %s", (nama, gmail)
            )
            if c.fetchone():
                print(f"Akun dengan nama '{nama}' atau gmail '{gmail}' sudah ada.")
                return

            # Insert akun admin
            c.execute(
                "INSERT INTO users (nama, gmail, password, role) VALUES (%s, %s, %s, %s)",
                (nama, gmail, hashed, "admin"),
            )
            conn.commit()
            print(f"Akun admin '{nama}' berhasil dibuat!")
    finally:
        conn.close()


if __name__ == "__main__":
    # Ganti nilai ini sesuai keinginan
    nama = "admin"
    gmail = "admin@example.com"
    password_plain = "AdminPassword123"

    create_admin_account(nama, gmail, password_plain)
