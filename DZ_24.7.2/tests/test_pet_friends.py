from api import PetFriends #импортируем из файла библиотеку PetFriends

from settings import valid_email,valid_password #импортируем регистрационные данные в приложение

import os

pf = PetFriends() #инициализируем библиотеку

def test_get_api_key_for_valid_user(email=valid_email,password=valid_password):
    """ Проверяем, что запрос API ключа возвращает status 200, и в result содержится key"""
    status,result = pf.get_api_key(email,password) # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем API ключ, сохраняем в переменную auth_key. Далее, используя этого ключ, запрашиваем список всех питомцев и проверяем, что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _,auth_key = pf.get_api_key(valid_email,valid_password) #получаем api ключ и сохраняем в переменную auth_key. Статус не нужен, ставим _
    status,result = pf.get_list_of_pets(auth_key,filter) # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 200
    assert len(result['pets'])>0

def test_add_new_pet_with_valid_data(name='Федот', animal_type='Метис',
                                     age='10', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)# Запрашиваем ключ api и сохраняем в переменую auth_key

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Морекот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets") # запрашиваем список своих питомцев

    assert status == 200
    assert pet_id not in my_pets.values()     # Проверяем, что в списке питомцев нет id удалённого питомца

def test_successful_update_self_pet_info(name='Мавродий', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то обновляем имя, тип, возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name # Проверяем, что имена питомцев соответствуют
    else:
        raise Exception('There is no my pets') # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев

# Тест №1
def test_add_new_pet_without_photo_valid_data(name='Костик', animal_type='бой',
                                     age='1'):
    """Проверяем возможность добавления питомца с корректными данными без фотографии"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

# Тест №2
def test_successful_add_photo_of_pet(pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления фотографии питомцу"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    # Если список не пустой, то берем первого питомца и добавляем фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] != ''# Проверяем, что фотография добавлена
    else:
        raise Exception('There is no my pets')

# Тест №3
def test_get_api_key_for_empty_password(email=valid_email, password=''):
    """ Проверяем, если не ввести пароль, запрос API ключа не удается, и возвращается статус 403"""

    status, result = pf.get_api_key(email, password) # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 403

# Тест №4
def test_get_api_key_for_invalid_password(email=valid_email, password='555'):
    """ Проверяем, что при вводе неверного пароля, запрос API ключа не удается, и возвращается статус 403"""

    status, result = pf.get_api_key(email, password) # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 403

# Тест №5
def test_add_new_pet_with_empty_type(name='Маркиза', animal_type='',
                                     age='7', pet_photo='images/P1040103.jpg'):
    """Проверяем, что питомец может быть создан без указания типа"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)# Запрашиваем ключ api и сохраняем в переменую auth_key

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# Тест №6
def test_get_api_key_for_invalid_data(email='!', password='555'):
    """ Проверяем, что при вводе неверных регитсрационных данных, запрос API ключа не удается, и возвращается статус 403"""

    status, result = pf.get_api_key(email, password) # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 403

# Тест №7
def test_add_new_pet_with_no_data(name='', animal_type='', age=''):
    """Проверяем возможность добавления нового питомца без данных"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == ''

# Тест №8
def test_get_api_key_for_empty_email(email='', password=valid_password):
    """ Проверяем, если не ввести почту, запрос API ключа не удается, и возвращается статус 403"""

    status, result = pf.get_api_key(email, password) # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 403

# Тест №9
def test_get_api_key_for_invalid_email(email='ddshgl', password=valid_password):
    """ Проверяем, что при вводе неверной почты, запрос API ключа не удается, и возвращается статус 403"""

    status, result = pf.get_api_key(email, password) # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 403

# Тест №10
def test_add_new_pet_with_invalid_pet_photo(name='Элизабэт', animal_type='принцесса',
                                            age='1000',
                                            pet_photo=' '):
    """Проверяем, что нельзя добавить питомца, если не указан путь до файла с фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except PermissionError:
        print("Specify the path to the file") # Укажите путь к файлу