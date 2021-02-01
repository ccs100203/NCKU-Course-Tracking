import requests
from selenium import webdriver
import time
import sys
import getpass

mode = 1
dept = 'F7'
course = '160'
account = '123'
password = '123'
line_token = '123'

# send line message
def lineNotifyMessage(msg):
    global line_token
    headers = {
      "Authorization": "Bearer " + line_token, 
      "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

# find remain course and use same driver
def find_remain_only(driver):
    global mode, dept, course
    # goto course main page
    driver.get('https://course.ncku.edu.tw/index.php?c=qry_all')
    time.sleep(0.5)
    driver.find_element_by_css_selector(f'li[data-dept="{dept}"]').click()
    
    time.sleep(2)
    
    isRemain = False
    # already into subject page
    for i in range(1, 10000):
        text = driver.find_element_by_css_selector(f'#A9-table > tbody > tr:nth-child({i}) > td:nth-child(2) > div').text
        if(text == dept+'-'+course):
            ele = driver.find_element_by_xpath(f'//*[@id="A9-table"]/tbody/tr[{i}]/td[8]').text
            if(ele.find('額滿') < 0):
                isRemain = True
            break
    
    if isRemain: 
        if mode == 1:
            message = dept+'-'+course +' 有餘額'
            lineNotifyMessage(message)
        elif mode == 2:
            # login and choose course
            login(driver)
            message = dept+'-'+course +' 選課成功'
            lineNotifyMessage(message)
        driver.close()
        sys.exit()

# choose course
def choose(driver):
    global dept, course
    # goto 預排選課 page
    # COS NUMBER MAYBE GET SOME ERROR BUT I CANNOT RECOGNIZE
    driver.get('https://course.ncku.edu.tw/index.php?c=cos21322')
    time.sleep(2)
    s = dept+course
    try:
        driver.find_element_by_css_selector(f'#main-table > tbody > tr.course_tr.course_{s}.td_bg1 > td:nth-child(10) > button').click()
    except:
        pass
    time.sleep(0.5)
    try:
        driver.find_element_by_css_selector(f'#main-table > tbody > tr.course_tr.course_{s}.td_bg2 > td:nth-child(10) > button').click()
    except:
        pass

# login course website
def login(driver):
    global account, password
    driver.set_window_size(1400, 800)
    driver.get('https://course.ncku.edu.tw/index.php?c=auth')
    driver.find_element_by_xpath('//*[@id="loginbg"]/div/div/div[2]/a').click()

    time.sleep(2)
    # input username && passsword
    driver.find_element_by_xpath('//*[@id="userNameInput"]').send_keys(account)
    driver.find_element_by_xpath('//*[@id="passwordInput"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="submitButton"]').click()
    time.sleep(2)

    # force login
    try:
        driver.find_element_by_xpath('//*[@id="error"]/div/form/span/div/div[2]/p/a').click()
    except:
        pass
    time.sleep(2)
    choose(driver)
    
def main():
    global mode, dept, course, account, password, line_token
    # mode 1: remain tracking
    # mode 2: auto choosing course
    mode = eval(input("choose mode, 1 is notify, 2 is auto: "))
    dept = input('department number: ')
    course = input('course number: ')
    line_token = input('line_token: ')
    if mode == 2:
        account = input('account: ')
        password = getpass.getpass('password: ')

    # create a chrome driver
    driver = webdriver.Chrome()
    driver.set_window_size(1400, 800)
    time.sleep(0.5)

    if mode == 1:
        # track course remain
        while True:
            find_remain_only(driver)
            time.sleep(5)
    else:
        # track course remain && auto choose
        while True:
            find_remain_only(driver)
            time.sleep(5)
    
main()