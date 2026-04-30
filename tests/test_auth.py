import time

from app import app


def unique_name(prefix: str = "pytest_user") -> str:
    return f"{prefix}_{int(time.time() * 1000)}"


def test_register_login_and_ui_success():
    client = app.test_client()
    nama = unique_name()
    gmail = f"{nama}@example.com"
    password = "rahasia123"

    register_res = client.post("/register", json={"nama": nama, "gmail": gmail, "password": password})
    assert register_res.status_code == 200
    assert register_res.get_json()["message"] == "Register berhasil"

    login_res = client.post("/login", json={"nama": nama, "password": password})
    assert login_res.status_code == 200
    assert login_res.get_json()["message"] == "Login berhasil"

    ui_res = client.get("/ui", follow_redirects=False)
    assert ui_res.status_code == 200


def test_register_duplicate_name_rejected():
    client = app.test_client()
    nama = unique_name("pytest_dup")
    gmail = f"{nama}@example.com"
    password = "rahasia123"

    first = client.post("/register", json={"nama": nama, "gmail": gmail, "password": password})
    assert first.status_code == 200

    duplicate = client.post("/register", json={"nama": nama, "gmail": f"other_{gmail}", "password": password})
    assert duplicate.status_code == 400
    assert duplicate.get_json()["message"] == "Nama sudah digunakan"


def test_login_wrong_password_rejected():
    client = app.test_client()
    nama = unique_name("pytest_wrong")
    gmail = f"{nama}@example.com"
    password = "rahasia123"

    register_res = client.post("/register", json={"nama": nama, "gmail": gmail, "password": password})
    assert register_res.status_code == 200

    wrong_login = client.post("/login", json={"nama": nama, "password": "salah123"})
    assert wrong_login.status_code == 401
    assert wrong_login.get_json()["message"] == "Nama atau password salah"


def test_ui_without_login_redirects_to_login_page():
    client = app.test_client()
    ui_res = client.get("/ui", follow_redirects=False)

    assert ui_res.status_code == 302
    assert ui_res.headers["Location"] == "/login-page"


def test_empty_input_returns_400_for_register_and_login():
    client = app.test_client()

    register_empty = client.post("/register", json={})
    assert register_empty.status_code == 400
    assert register_empty.get_json()["message"] == "Semua field wajib diisi"

    login_empty = client.post("/login", json={})
    assert login_empty.status_code == 400
    assert login_empty.get_json()["message"] == "Nama dan password wajib diisi"
