import json


# Функция для чтения настроек
def read_settings():
    with open('settings.json', 'r') as f:
        settings_file = json.load(f)
        return settings_file


# Функция для записи настроек
def write_settings(id, new_value):
    with open('settings.json', 'r') as f:
        settings_file = json.load(f)
        settings_file[id] = new_value
        with open('settings.json', 'w') as w:
            json.dump(settings_file, w, indent=4, ensure_ascii=False)