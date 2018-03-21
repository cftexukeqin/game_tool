import re
from threading import Timer
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


def main():
    try:
        print('正在登录网页...')
        opt = webdriver.ChromeOptions()
        opt.set_headless()

        driver = webdriver.Chrome(options=opt)
        wait = WebDriverWait(driver, 10)
        url = "http://sw.hxzoo.com/UserCenter/Login.php"
        driver.get(url)
        usernameInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#u_name")))
        pwdInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#u_pas')))

        usernameInput.send_keys('ohyescnm')
        pwdInput.send_keys('ohyescnm')

        login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#reg_sub')))
        login_btn.click()
        print('登录成功！')
        cmt_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="jquery-jmodal"]/table/tbody/tr[2]/td[2]/div[3]/a[1]')))
        cmt_btn.click()
        print('正在领取游戏积分...')
        get_money_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                               '#loadding > div.center.clearfix.mt10 > div > div.center_right.ml10 > div.basicInfo > font > div > ul > li:nth-child(2) > a')))
        get_money_btn.click()

        tips = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#jmodal-container-content > b'))).text
        pattern = re.compile(u'-?[1-9]\d*')
        rest_time = int(pattern.search(tips).group(0))
        if rest_time and rest_time != 10:
            print('积分领取失败,%d 分钟后才能领取积分！脚本将在%d分钟后重新启动！' % (rest_time,rest_time))
            Timer((rest_time+1)*60,main).start()
        elif rest_time == 10:
            print('领取积分成功!,脚本将在60分钟后再次启动！')
            Timer(60*60,main).start()

        driver.refresh()
        point = driver.find_element_by_css_selector('#loadding > div.center.clearfix.mt10 > div > div.center_right.ml10 > div.basicInfo > font > div > ul > li:nth-child(1) > span:nth-child(4)')
        print('当前积分为：',point.text)

        driver.close()
        with open('log_success.txt','a+') as f:
            f.write('已经领取成功！'+  str(datetime.datetime.now()))

    except TimeoutException:
        with open('log_fail.txt','a+') as f:
            f.write('已经失败成功！'+ str(datetime.datetime.now()))
        main()

if __name__ == '__main__':
    main()
    print('-'*80)