import json
import os
import requests
import tkinter as tk

from tkinter import ttk
from config import *

graphql_url = stratz_graphql_url  # URL для GraphQL API Stratz
api_key = your_api_key

hero_id = hero_id

def on_submit(hero_id, graphql_url, api_key):
    hero_name = hero_entry.get()

    def hero_id_to_name(hero_id, hero_id_dict):
        for key, value in hero_id_dict.items():
            if value == hero_id:
                return key
        return None

    hero_id_value = hero_id.get(hero_name)

    query = f"""
    {{
      heroStats {{
        heroVsHeroMatchup(heroId: {hero_id_value}) {{
          disadvantage {{
            vs {{
              heroId1
              heroId2
              synergy
              matchCount
            }}
          }}
        }}
      }}
    }}
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {"query": query}

    # Создайте путь к файлу в папке data
    file_path = os.path.join("data", f"{hero_name}.json")

    if not os.path.exists(file_path):
        response = requests.post(graphql_url, headers=headers, json=data)
        result = response.json()
        disadvantage_data = result['data']['heroStats']['heroVsHeroMatchup']['disadvantage']

        # Если файл не существует, сохраните данные в новом файле JSON
        with open(file_path, 'w') as f:
            json.dump(disadvantage_data, f, ensure_ascii=False, indent=4)
    else:
        print(f"Файл {file_path} уже существует, пропускаем запрос к API")

    # Открываем файл для чтения
    with open(f'data/{hero_name}.json', 'r') as f:
        # Загружаем JSON-данные из файла
        data = json.load(f)

    for item in data:
        for vs_item in item['vs']:
            # Получаем значения полей "heroId1", "synergy" и "matchCount"
            heroId1 = vs_item.get('heroId1')
            heroId2 = vs_item.get('heroId2')
            synergy = vs_item.get('synergy')
            matchCount = vs_item.get('matchCount')

            # Получаем имена героев по их hero_id
            hero_name_1 = hero_id_to_name(heroId1, hero_id)
            hero_name_2 = hero_id_to_name(heroId2, hero_id)

            # Печатаем полученные данные
            print(f"Hero 1: {hero_name_1}, Hero 2: {hero_name_2}, Synergy: {synergy}, Match Count: {matchCount}")


root = tk.Tk()
root.title("Dota 2 Counter Picker")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

hero_label = ttk.Label(main_frame, text="Введите имя героя:")
hero_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

hero_entry = ttk.Entry(main_frame)
hero_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))

submit_button = ttk.Button(main_frame, text="Показать контрпики", command=lambda: on_submit(hero_id, graphql_url, api_key))
submit_button.grid(row=1, column=0, columnspan=2, pady=(0, 10))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

root.mainloop()
