from selenium import webdriver


class Driversettings(object):
    def set_driver(self):
        driver = webdriver.Chrome()  # 启动浏览器
        driver.implicitly_wait(20)
        return driver

    def login(self,driver):
        loginurl = "http://jira.intretech.com:8080/login.jsp"
        driver.get(loginurl)
        driver.find_element_by_id('login-form-username').send_keys('10324')
        driver.find_element_by_id('login-form-password').send_keys('123aaa')
        driver.find_element_by_id('login-form-submit').click()

    def get_url(self,jiraid):
        url = ("http://jira.intretech.com:8080/browse/" + jiraid)
        return url



