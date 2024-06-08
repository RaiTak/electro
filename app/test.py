import requests

url = "http://127.0.0.1:8000/buildings/delete/4"  # Замените 4 на нужный вам идентификатор здания
response = requests.delete(url)
print(response.status_code)  # Проверяем статус ответа
