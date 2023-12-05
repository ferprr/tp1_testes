from django.test import TestCase
from selenium import webdriver
import time

class Logine2eTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
      self.driver.get('http://127.0.0.1:8000/accounts/login')

      time.sleep(4)

      username_input = self.driver.find_element('name', 'username')
      password_input = self.driver.find_element('name','password')
      login_button = self.driver.find_element('name','login_button')

      username_input.send_keys('Admin')
      password_input.send_keys('adm@2023')

      login_button.click()

      time.sleep(2)

      self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/')