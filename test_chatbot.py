from chatbot import chat_response

# Test chatbot tanpa database
print("Testing chatbot recommendations...")

# Test 1: Rekomendasi umum
result1 = chat_response("saya mau rekomendasi wisata di bali")
print("Test 1 - General recommendation:")
print(result1[:500] + "...")
print("\n" + "="*50 + "\n")

# Test 2: Rekomendasi pantai
result2 = chat_response("saya suka pantai")
print("Test 2 - Beach recommendation:")
print(result2[:500] + "...")
print("\n" + "="*50 + "\n")

# Test 3: Rekomendasi terbaik
result3 = chat_response("tempat terbaik di bali")
print("Test 3 - Best places:")
print(result3[:500] + "...")
print("\n" + "="*50 + "\n")

print("Test completed!")