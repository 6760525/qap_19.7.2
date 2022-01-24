import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='The Holiday Armadillo', animal_type='armadillo',
                                     age='1', pet_photo='images/armadillo.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Игорь", "iguana", "2", "images/iguana.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Рождественский Броненосец', animal_type='armadillo', age=1):
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


"""
19.7.2
"""


def test_failed_get_api_key_for_invalid_user(email="g326%^w354", password="invalid"):
    # 1. invalid e-mail
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_failed_get_api_key_for_invalid_password(email=valid_email, password="invalid"):
    # 2. invalid password
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_failed_get_api_key_for_invalid_user(email="", password=""):
    # 3. empty email
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_failed_get_api_key_for_valid_user(email=valid_email, password=""):
    # 4. empty  password
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_failed_get_all_pets_with_invalid_key(filter=''):
    # 5. invalid key
    auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae720"}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


def test_failed_add_new_pet_with_wrong_data(name='Test name',
                                            animal_type='test type',
                                            age='-10',
                                            pet_photo='images/iguana.jpg'):
    # 6. invalid data add
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['age'] == '-10'


def test_failed__add_new_pet_with_wrong_file(name='Кенга', animal_type='валлаби', age='0',
                                             pet_photo='images/wallaby.txt'):
    # 7. Wrong file type
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 500


def test_failed_add_new_pet_with_wrong_image(name='Кенга', animal_type='валлаби', age='0',
                                             pet_photo='images/wallaby.bmp'):
    # 8. Wrong image file type
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200


def test_successful_create_pet_simple(name='Игемон', animal_type='игуана', age='99'):
    # 9. Wrong image file type
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_successful_set_photo(pet_photo='images/iguana.jpg'):
    # 10. Update image
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 200
