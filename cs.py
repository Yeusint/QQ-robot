from selenium import webdriver
driver = webdriver.Chrome(executable_path=execute_path)
url = 'https://www.baidu.com/'
driver.get(url)