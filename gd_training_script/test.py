from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import math



def read_credentials(file_path):
    """读取credentials.txt中的账号密码"""
    import os
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Credentials file not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError("Credentials file format error: expected at least 2 lines (username and password)")
    return lines[0], lines[1]

#
# This file is part of the App project.
# Copyright © NeoLs Technology Co., Ltd.
# All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
#
# Copyright 2024-11-02 NeoLsHuang huangleshu.hls@alibab-inc.com
# All rights reserved.
#



def switch2frame(par):
    par.switch_to.frame('secondIframe')
    par.switch_to.frame('thirdIframe')
    par.switch_to.frame('dataMainIframe')


def run_main(video_unstudy_num, browser):
    if int(video_unstudy_num) > 0:
        print("nonlocal--该目录下还有{}个视频未学习……".format(video_unstudy_num))
        js_click = 'document.getElementsByClassName("courseware-list-reed")[0].click()'
        browser.execute_script(js_click)
        time.sleep(3)
        # 拿到所有的窗口
        all_handles = browser.window_handles
        pre_window_handle = browser.current_window_handle
        for handle in all_handles:
            if handle != pre_window_handle:
                browser.switch_to.window(handle)
                browser.implicitly_wait(10)
                # time.sleep(10)
                # elem = browser.find_element_by_class_name("introjs-button")
                browser.switch_to.frame('course_frame')
                time.sleep(3)
                # 点击播放
                js_paused = 'return document.getElementById("my-video_html5_api").paused;'
                view_paused_status = browser.execute_script(js_paused)
                print('viewPaused：' + str(view_paused_status))
                # false 点击了播放  true 点击了暂停
                if view_paused_status:
                    elem = browser.find_element(By.CLASS_NAME, "vjs-play-control")
                    elem.click()
                    # 静音
                    elem = browser.find_element(By.CLASS_NAME, "vjs-mute-control")
                    elem.click()
                    print("click over")
                time.sleep(2)
                # 获取视频播放时长?
                js_duration_str = 'return document.getElementById("my-video_html5_api").duration;'
                view_time = browser.execute_script(js_duration_str)
                print('viewTime:' + str(view_time))
                time.sleep(1)
                js_current_time_str = 'return document.getElementById("my-video_html5_api").currentTime;'
                view_current_time = browser.execute_script(js_current_time_str);
                print('viewCurrentTime:' + str(view_current_time))

                if math.ceil(view_current_time) >= math.ceil(view_time):
                    print('1111')
                    browser.switch_to.default_content()
                    elem = browser.find_element(By.CLASS_NAME, 'instructions-close')
                    elem.click()
                    # 关闭视频网站页面 进入pre_window_handle页面
                    browser.switch_to.window(pre_window_handle)
                    browser.refresh()
                    browser.implicitly_wait(3)
                    switch2frame(browser)
                    js_list = 'return document.getElementsByClassName("courseware-list-reed").length;'
                    video_unstudy_num = browser.execute_script(js_list)
                    time.sleep(3)
                    # print("local--该目录下还有{}个视频未学习……".format(video_unstudy_num))
                    run_main(video_unstudy_num, browser)
                else:
                    print('2222')
                    time.sleep(math.ceil(view_time) - math.ceil(view_current_time))
                    print('当前sleep时间：', math.ceil(view_time) - math.ceil(view_current_time))
                    browser.switch_to.default_content()
                    elem = browser.find_element(By.CLASS_NAME, 'instructions-close')
                    elem.click()
                    # 关闭视频网站页面 进入pre_window_handle页面
                    browser.switch_to.window(pre_window_handle)
                    browser.refresh()
                    browser.implicitly_wait(3)
                    switch2frame(browser)
                    js_list = 'return document.getElementsByClassName("courseware-list-reed").length;'
                    video_unstudy_num = browser.execute_script(js_list)
                    time.sleep(3)
                    # print("local--该目录下还有{}个视频未学习……".format(video_unstudy_num))
                    run_main(video_unstudy_num, browser)
    else:
        print("该目录下还有视频已学习完毕……")


def main():

    # TODO: 用credentials.txt记录账号密码，.gitignore 忽略该文件提交上传git。保证数据安全问题
    # 从credentials.txt读取账号密码
    username, passwd = read_credentials("credentials.txt")
    # 输入账号
    # 输入密码
    login_url = 'https://gbpx.gd.gov.cn/gdceportal/index.aspx'
    option = webdriver.ChromeOptions()
    option.add_argument('--window-size=1920,1080')
    driver_url = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    service = Service(executable_path=driver_url)
    # 创建 Service 对象
    print("123123123")
    browser = webdriver.Chrome(service=service, options=option)
    print("321321312")
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })
    print("open chrome success")
    browser.get(login_url)
    browser.implicitly_wait(1)
    # 窗口最大化
    browser.maximize_window()
    elem = browser.find_element(By.CLASS_NAME, 'text-wrapper_12')
    elem.click()
    time.sleep(1)
    password_login_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='nav-items' and text()='密码登录']"))
    )
    password_login_button.click()
    elem = browser.find_element(By.ID, 'txtLoginName')
    elem.clear()
    elem.send_keys(username)
    time.sleep(1)
    elem = browser.find_element(By.ID, 'txtPassword')
    elem.clear()
    elem.send_keys(passwd)
    time.sleep(1)
    # TODO: 考虑使用PIL图片处理+pytesseract图片转文字处理
    # 验证码
    code_num = pyautogui.prompt("请输入验证码:")
    elem = browser.find_element(By.ID, 'txtValid')
    elem.clear()
    elem.send_keys(code_num)
    elem = browser.find_element(By.ID, 'cbAgree')
    elem.click()
    time.sleep(1)
    elem = browser.find_element(By.CLASS_NAME, 'loginBtnBox')
    elem.click()
    time.sleep(1)
    elem = browser.find_element(By.CLASS_NAME, 'title_more')
    elem.click()
    time.sleep(1)
    # browser.switch_to_frame('secondIframe')
    # browser.switch_to.frame('secondIframe')
    # browser.switch_to.frame('thirdIframe')
    # browser.switch_to.frame('dataMainIframe')
    switch2frame(browser)
    time.sleep(1)

    js_list = 'return document.getElementsByClassName("courseware-list-reed").length;'
    video_unstudy_num = browser.execute_script(js_list)
    time.sleep(3)
    run_main(video_unstudy_num, browser)
    browser.close()
    print("end......")


if __name__ == '__main__':
    main()