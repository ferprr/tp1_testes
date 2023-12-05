from django.test import TestCase
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

class Poste2eTest(TestCase):
    def setUp(self):
      self.driver = webdriver.Chrome()

    def tearDown(self):
      self.driver.quit()

    def test_read_post_in_list(self):
      self.driver.get('http://127.0.0.1:8000/')

      time.sleep(4)

      post_input = self.driver.find_element('name', 'post-9')
      link_post = post_input.find_element(By.TAG_NAME, 'a')

      link_post.click()

      time.sleep(2)

      self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/post/9/')

      post_title  = self.driver.find_element(By.CLASS_NAME, 'postTitle')
      title  = post_title.find_element(By.TAG_NAME, 'h2')
  
      self.assertEqual(title.text, 'Pentest: Descobrindo Vulnerabilidades para Reforçar a Segurança')