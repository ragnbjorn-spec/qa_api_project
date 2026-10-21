import pytest
import requests

# базовый URL для всех запросов
base_url = "https://jsonplaceholder.typicode.com"

# --- НАЧАЛО ФИКСТУРЫ ---
@pytest.fixture
def created_post_id():
    # Эта часть выполняется ДО теста (создаем пост)
    data = {
        "title": "Пост для фикстуры",
        "body": "Текст",
        "userId": 1
    }
    response = requests.post(f"{base_url}/posts", json=data, timeout=10)
    
    # Забираем ID из ответа
    post_id = response.json().get("id")
    
    # Передаем ID в тест
    yield post_id
    
    # Эта часть выполняется ПОСЛЕ теста (если нужно что-то удалить, пишут здесь)
    # Но мы пока оставим пусто
# --- КОНЕЦ ФИКСТУРЫ ---

def test_get_post(created_post_id):
    # Внутри функции created_post_id уже содержит ID (например, 101)
    print(f"\nПроверяем пост с ID: {created_post_id}")
    
    # Отправляем GET-запрос
    response = requests.get(f"{base_url}/posts/{created_post_id}", timeout=10)
    
    # Проверяем, что сервер ответил 404 (наша особенность jsonplaceholder)
    assert response.status_code == 404

# --- ТЕСТ НА ОБНОВЛЕНИЕ (PUT) ---
def test_update_post(created_post_id):
    print(f"\nОбновляем пост с ID: {created_post_id}")
    
    data_put = {
        "title": "Обновленный заголовок",
        "body": "Новый текст",
        "userId": 1
    }
    
    response = requests.put(f"{base_url}/posts/{created_post_id}", json=data_put, timeout=10)
    
    # На jsonplaceholder PUT на несуществующий пост дает 500
    assert response.status_code == 500

# --- ТЕСТ НА УДАЛЕНИЕ (DELETE) ---
def test_delete_post(created_post_id):
    print(f"\nУдаляем пост с ID: {created_post_id}")
    
    response = requests.delete(f"{base_url}/posts/{created_post_id}", timeout=10)
    
    # Проверяем, что удаление прошло (200 или 204)
    assert response.status_code in [200, 204]
