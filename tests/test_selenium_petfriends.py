import re
import time

from selenium.webdriver.common.by import By

base_url = "https://petfriends.skillfactory.ru"

def test_petfriends(web_browser):
   driver = web_browser
   # Открыть домашнюю страницу PetFriends:
   driver.get(base_url)

   time.sleep(2)  # небольшая задержка, чисто ради эксперимента

   # Находим кнопку "Зарегистрироваться" и нажимаем на нее
   btn_newuser = driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
   btn_newuser.click()

   # Ищем надпись "У меня уже есть аккаунт" и нажимаем на нее
   btn_exist_acc = driver.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
   btn_exist_acc.click()

   # Ищем поле ввода электронной почты, очищаем его, а затем вводим свой email,
   # подставить вместо "<your_email>" свой email.
   field_email = driver.find_element(By.ID, "email")
   field_email.clear()
   field_email.send_keys("kramarenkoan562@gmail.com")

   # То же самое для поля с паролем
   field_pass = driver.find_element(By.ID, "pass")
   field_pass.clear()
   field_pass.send_keys("qwertyuio27")

   # Ищем кнопку "Войти" и нажимаем на нее
   btn_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
   btn_submit.click()

   time.sleep(3)  # небольшая задержка, чисто ради эксперимента

   # Ищем элемент меню "Мои питомцы" и нажимаем на него
   btn_submit = driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]')
   btn_submit.click()

   time.sleep(2)

   # Находим количество питомцев из статистики пользователя
   element_user_statistic = driver.find_element(By.CSS_SELECTOR, 'div.left')
   count_pets = int(re.findall(r'Питомцев: \d*', element_user_statistic.text)[0].split(' ')[1])

   pets = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
   count_pets_in_table = len(pets)
   # Проверяем соответствие количества питомцев из статистики пользователя количеству питомцев в таблице
   assert count_pets == count_pets_in_table

   # Находим количество картинок
   images = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr img')
   count_images = 0
   i=0
   while i < len(images):
      if images[i].get_attribute('src') != '':
         count_images+=1
      i+=1
   # Проверяем что хотя бы у половины есть картинки
   assert count_images >= count_pets / 2

   names = []
   data_pets = []
   for i in range(len(pets)):
      parts = pets[i].text.split(' ')
      assert len(parts) == 3
      if len(parts) == 3:
         name = parts[0]
         breed = parts[1]
         age = parts[2]
         # Проверяем наличие имени
         assert len(name) > 0
         # Проверяем наличие породы
         assert len(breed) > 0
         # Проверяем наличие возраста
         assert len(age) > 0
         # Проверяем имя на уникальность
         assert name not in names
         names.append(name)
         data_pet = name + '-' + breed + '-' + age
         # Проверяем питомца на уникальность
         assert data_pet not in data_pets
         data_pets.append(data_pet)
