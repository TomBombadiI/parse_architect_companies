import csv, json

def json_to_csv(json_data, csv_file_path, encoding='utf-8'):
    """Преобразует JSON-данные в CSV-файл.

    Args:
        json_data (dict or list): JSON-данные для преобразования.
        csv_file_path (str): Путь к CSV-файлу.
        encoding (str, optional): Кодировка для CSV-файла. По умолчанию 'utf-8'.
    """

    # Проверяем, является ли json_data списком или словарем
    if isinstance(json_data, list):
        # Если это список, преобразуем его в список словарей
        json_data = [item for item in json_data]
    elif isinstance(json_data, dict):
        # Если это словарь, преобразуем его в список словарей
        json_data = [json_data]
    else:
        raise TypeError("json_data должен быть списком или словарем.")

    # Создаем файл CSV
    with open(csv_file_path, 'w', encoding=encoding, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=json_data[0].keys())
        # Записываем заголовок
        writer.writeheader()
        # Записываем строки
        writer.writerows(json_data)

json_data = json.load(open('results.json', 'r', encoding='utf-8'))
json_to_csv(json_data, 'results.csv')