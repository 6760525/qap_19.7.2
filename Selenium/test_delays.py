import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('c:\\temp\\chromedriver.exe')
   pytest.driver.get('http://petfriends1.herokuapp.com/login')
   pytest.driver.implicitly_wait(5)
   pytest.driver.find_element(by=By.ID, value='email').send_keys('icosahedron@xxx.xxx')
   pytest.driver.find_element(by=By.ID, value='pass').send_keys('123')
   pytest.driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
   pytest.driver.get('http://petfriends1.herokuapp.com/my_pets')

   yield
   pytest.driver.quit()

def test_petfriends_mypets_count():
   # Объявленное число питомцев соответствует отображаемому
   WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located(('id', 'navbarNav')))
   pets_count = len(pytest.driver.find_elements_by_xpath('//tbody/tr'))
   my_pets_info = pytest.driver.find_element_by_xpath('//*[h2][1]').text.split()
   assert my_pets_info[2] == str(pets_count)

def test_petfriends_mypets_photo():
   # Неявные ожидания фото
   pytest.driver.get('http://petfriends1.herokuapp.com/my_pets')
   WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'navbarNav')))
   images = pytest.driver.find_elements(by=By.XPATH, value='//img[@src=""]')
   no_photo = len(images)
   assert no_photo == 0

def test_petfriends_mypets_name():
   # Неявные ожидания имени питомца
   WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//tbody/tr/td[1]')))
   pets_count = len(pytest.driver.find_elements_by_xpath('//tbody/tr'))
   names = pytest.driver.find_elements(by=By.XPATH, value='//tbody/tr/td[1]')
   with_name = len(names)
   assert pets_count == with_name

def test_petfriends_mypets_age():
   # Неявные ожидания возраста питомца
   pytest.driver.get('http://petfriends1.herokuapp.com/my_pets')
   WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//tbody/tr/td[3]')))
   pets_count = len(pytest.driver.find_elements_by_xpath('//tbody/tr'))
   ages = pytest.driver.find_elements(by=By.XPATH, value='//tbody/tr/td[3]')
   with_age = len([float(i.text) for i in ages if float(i.text) >= 0.0])
   assert pets_count == with_age
