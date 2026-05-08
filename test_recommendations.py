import pandas as pd
from chatbot import get_ranked_recommendations

# Load dataset
print("Loading dataset...")
df = pd.read_csv("dataset_wisata_bali.csv")
print(f"Dataset loaded: {len(df)} rows")

# Test get_ranked_recommendations
print("\nTesting get_ranked_recommendations...")

# Test dengan preferences kosong
preferences = {}
result = get_ranked_recommendations(preferences, top=10)
print(f"Recommendations with empty preferences: {len(result)} places")

for i, place in enumerate(result[:3], 1):
    print(f"{i}. {place['nama_tempat']} - {place['kategori']} - Rating: {place['rating']}")

# Test dengan kategori pantai
result_beach = get_ranked_recommendations(preferences, kategori_target="pantai", top=8)
print(f"\nBeach recommendations: {len(result_beach)} places")

for i, place in enumerate(result_beach[:3], 1):
    print(f"{i}. {place['nama_tempat']} - {place['kategori']} - Rating: {place['rating']}")

print("\nTest completed!")