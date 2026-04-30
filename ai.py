import requests

def chat_rekomendasi(prompt_user):

    teks = prompt_user.lower()

    if "pantai" in teks:
        tempat = "Pantai Medewi"
    elif "gunung" in teks:
        tempat = "Gunung Batur"
    elif "air terjun" in teks:
        tempat = "Air Terjun Sekumpul"
    else:
        tempat = "Pantai Kuta"

    print("Tempat hasil AI (fallback):", tempat)

    url = f"http://127.0.0.1:5000/rekomendasi?tempat={tempat}"
    hasil = requests.get(url).json()

    return {
        "input_user": prompt_user,
        "tempat": tempat,
        "rekomendasi": hasil
    }


if __name__ == "__main__":
    print(chat_rekomendasi("Saya ingin wisata gunung"))