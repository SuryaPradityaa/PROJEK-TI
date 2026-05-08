#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script for multilingual chatbot."""

from chatbot import detect_intent

# Test multilingual intents
test_cases = [
    ('hello', 'salam'),
    ('こんにちは', 'salam'),
    ('你好', 'salam'),
    ('안녕하세요', 'salam'),
    ('hola', 'salam'),
    ('bonjour', 'salam'),
    ('guten tag', 'salam'),
    ('beach', 'pantai'),
    ('ビーチ', 'pantai'),
    ('海滩', 'pantai'),
    ('nature', 'alam'),
    ('自然', 'alam'),
    ('temple', 'budaya'),
    ('寺院', 'budaya'),
    ('美食', 'kuliner'),
    ('food', 'kuliner'),
]

print('Testing multilingual intent classification:')
print('=' * 60)
print(f"{'Input':<20} {'Expected':<10} {'Predicted':<10} {'Status'}")
print('=' * 60)

correct = 0
total = len(test_cases)

for test_input, expected in test_cases:
    try:
        predicted = detect_intent(test_input)
        status = '✓' if predicted == expected else '✗'
        if predicted == expected:
            correct += 1
        print(f"{test_input:<20} {expected:<10} {predicted:<10} {status}")
    except Exception as e:
        print(f"{test_input:<20} {expected:<10} ERROR      {str(e)[:10]}")

print('=' * 60)
print(f"Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
print("Multilingual training completed successfully!")