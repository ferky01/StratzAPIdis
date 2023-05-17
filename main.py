import json
import os
import tkinter as tk
from tkinter import ttk

import requests

from config import *

graphql_url = stratz_graphql_url  # URL для GraphQL API Stratz
api_key = your_api_key

hero_id = hero_id


def hero_id_to_name(hero_id, hero_id_dict):
    for key, value in hero_id_dict.items():
        if value == hero_id:
            return key
    return None


def on_submit(team1_entries, team2_entries, graphql_url, api_key):
    team1_hero_names = [entry.get() for entry in team1_entries]
    team2_hero_names = [entry.get() for entry in team2_entries]

    for hero_name in team1_hero_names + team2_hero_names:
        if hero_name:  # Проверяем, ввел ли пользователь имя героя
            hero_id_value = hero_id.get(hero_name)
            if not hero_id_value:
                print(f"Неизвестный герой: {hero_name}")
                continue

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
                    print(
                        f"Hero 1: {hero_name_1}, Hero 2: {hero_name_2}, Synergy: {synergy}, Match Count: {matchCount}")


root = tk.Tk()
root.title("Dota 2 Team Synergy")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

team1_labels = []
team1_entries = []
for i in range(5):
    team1_label = ttk.Label(main_frame, text=f"Введите имя героя для команды 1 (Герой {i + 1}):")
    team1_label.grid(row=i, column=0, sticky=tk.W, pady=(0, 10))
    team1_labels.append(team1_label)

    team1_entry = ttk.Entry(main_frame)
    team1_entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
    team1_entries.append(team1_entry)

team2_labels = []
team2_entries = []
for i in range(5, 10):
    team2_label = ttk.Label(main_frame, text=f"Введите имя героя для команды 2 (Герой {i - 4}):")
    team2_label.grid(row=i, column=0, sticky=tk.W, pady=(0, 10))
    team2_labels.append(team2_label)

    team2_entry = ttk.Entry(main_frame)
    team2_entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
    team2_entries.append(team2_entry)

submit_button = ttk.Button(main_frame, text="Показать синергию",
                           command=lambda: on_submit(team1_entries, team2_entries, graphql_url, api_key))
submit_button.grid(row=10, column=0, columnspan=2, pady=(0, 10))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

root.mainloop()
