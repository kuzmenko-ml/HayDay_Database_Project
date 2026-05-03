import pandas as pd
# Налаштування, щоб показувати всі колонки
pd.set_option('display.max_columns', None)
# Налаштування, щоб текст у колонках не обрізався за шириною
pd.set_option('display.width', 1000)
import os

file_path = os.path.join('..', 'DATA', 'ПершийФайл.xlsx')

try:
    df = pd.read_excel(file_path, sheet_name='Buildings')

    print("Файл знайдено! Ось перші рядки твоїх даних:")
    print(df.head())

except Exception as e:
    print(f"Щось пішло не так: {e}")