from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import tkinter as tk
from tkinter import simpledialog

def main():
    print("start......")

    # 初始化 Chrome WebDriver
    print("正在初始化浏览器...")

    # 获取 chromedriver 的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(current_dir, 'chromedriver')

    try:
        # 使用本地的 chromedriver
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)
        # 最大化窗口
        driver.maximize_window()
    except Exception as e:
        print(f"初始化浏览器失败: {e}")
        print(f"\nChromeDriver 路径: {chromedriver_path}")
        print("\n请确保：")
        print("1. chromedriver 文件存在于项目目录")
        print("2. chromedriver 有执行权限")
        print("3. 已安装 Chrome 浏览器")
        return

    try:
        # 访问目标 URL
        url = "http://jxjy.gdlink.net.cn/Elearning.GDLink.Student//Home/Index"
        print(f"正在访问: {url}")
        driver.get(url)

        # 等待页面基本加载
        time.sleep(3)
        print(f"当前页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")

        # 等待页面加载，设置最大等待时间为 20 秒
        wait = WebDriverWait(driver, 20)

        # 检查是否有 iframe
        print("检查页面中的 iframe...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"找到 {len(iframes)} 个 iframe")

        # 如果有 iframe，尝试切换到每个 iframe 中查找元素
        enter_link = None
        if len(iframes) > 0:
            for i, iframe in enumerate(iframes):
                try:
                    print(f"尝试切换到第 {i+1} 个 iframe...")
                    driver.switch_to.frame(iframe)
                    print(f"已切换到第 {i+1} 个 iframe，当前 URL: {driver.current_url}")

                    # 在 iframe 中查找链接
                    print("在 iframe 中查找'进入站点'链接...")
                    enter_link = wait.until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "进入站点"))
                    )
                    print(f"在第 {i+1} 个 iframe 中找到'进入站点'链接！")
                    break
                except Exception as e:
                    print(f"在第 {i+1} 个 iframe 中未找到: {e}")
                    # 切换回主页面
                    driver.switch_to.default_content()

        # 如果在 iframe 中没找到，在主页面中查找
        if enter_link is None:
            print("在主页面中查找'进入站点'链接...")
            try:
                # 尝试通过链接文本查找
                enter_link = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "进入站点"))
                )
                print("在主页面找到'进入站点'链接！")
            except Exception as e:
                print(f"通过链接文本查找失败: {e}")
                print("尝试通过 XPath 查找...")
                # 尝试通过 XPath 查找
                enter_link = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '进入站点')]"))
                )
                print("通过 XPath 找到'进入站点'链接！")

        # 点击链接
        print("点击'进入站点'...")
        enter_link.click()

        # 等待点击后页面跳转
        time.sleep(2)
        driver.switch_to.default_content()  # 切换回主页面
        print(f"点击后URL: {driver.current_url}")

        # 查找并点击登录按钮
        print("\n正在查找'登录'按钮...")
        time.sleep(2)  # 等待页面加载

        try:
            # 尝试通过链接文本查找
            login_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "您好，请登录"))
            )
            print("通过链接文本找到'登录'按钮！")
        except Exception as e:
            print(f"通过链接文本查找登录失败: {e}")
            try:
                # 尝试通过 class 查找
                login_link = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.signIn"))
                )
                print("通过 CSS 选择器找到'登录'按钮！")
            except Exception as e2:
                print(f"通过 CSS 选择器查找登录失败: {e2}")
                # 尝试通过 XPath 查找
                login_link = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '登录')]"))
                )
                print("通过 XPath 找到'登录'按钮！")

        print("点击'登录'按钮...")
        login_link.click()

        # 等待登录页面加载
        time.sleep(2)
        print(f"点击登录后URL: {driver.current_url}")

        # 读取账号密码
        print("\n正在读取账号密码...")
        credentials_path = os.path.join(current_dir, 'credentials.txt')
        with open(credentials_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            username = lines[0].strip()
            password = lines[1].strip()
        print(f"账号: {username}")

        # 填写登录表单
        print("\n正在填写登录表单...")

        # 输入账号
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.clear()
        username_input.send_keys(username)
        print("已输入账号")

        # 输入密码
        password_input = wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.clear()
        password_input.send_keys(password)
        print("已输入密码")

        # 使用 tkinter 弹出输入框获取验证码
        print("\n请在弹出的输入框中输入验证码...")

        # 创建一个隐藏的主窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        root.attributes('-topmost', True)  # 确保对话框在最前面

        # 弹出输入框
        captcha = simpledialog.askstring(
            "验证码输入",
            "请输入验证码:",
            parent=root
        )

        root.destroy()  # 销毁窗口

        if captcha is None or captcha == '':
            print("未输入验证码，取消登录")
            return

        print(f"已获取验证码: {captcha}")

        # 输入验证码
        captcha_input = wait.until(
            EC.presence_of_element_located((By.ID, "validateCode"))
        )
        captcha_input.clear()
        captcha_input.send_keys(captcha)
        print("已输入验证码")

        # 点击登录按钮
        print("\n正在点击登录按钮...")
        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "signBtn"))
        )
        login_button.click()
        print("已点击登录按钮")

        # 等待登录完成
        time.sleep(3)
        print(f"登录后URL: {driver.current_url}")

        # 查找并点击"个人中心"
        print("\n正在查找'个人中心'链接...")
        time.sleep(2)  # 等待页面加载

        try:
            # 尝试通过链接文本查找
            personal_center_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "个人中心"))
            )
            print("通过链接文本找到'个人中心'链接！")
        except Exception as e:
            print(f"通过链接文本查找失败: {e}")
            try:
                # 尝试通过 CSS 选择器查找
                personal_center_link = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.bluestyle"))
                )
                print("通过 CSS 选择器找到'个人中心'链接！")
            except Exception as e2:
                print(f"通过 CSS 选择器查找失败: {e2}")
                # 尝试通过 href 属性查找
                personal_center_link = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Elearning.GDLink.Student/StudentCourse/All']"))
                )
                print("通过 href 属性找到'个人中心'链接！")

        print("点击'个人中心'...")
        personal_center_link.click()

        # 等待页面跳转
        time.sleep(2)
        print(f"点击个人中心后URL: {driver.current_url}")

        # 查找并点击"未完成课程"
        print("\n正在查找'未完成课程'链接...")
        time.sleep(2)  # 等待页面加载

        try:
            # 尝试通过链接文本查找
            unfinished_course_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "未完成课程"))
            )
            print("通过链接文本找到'未完成课程'链接！")
        except Exception as e:
            print(f"通过链接文本查找失败: {e}")
            try:
                # 尝试通过 href 属性查找
                unfinished_course_link = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/Elearning.GDLink.Student/StudentCourse/Studying']"))
                )
                print("通过 href 属性找到'未完成课程'链接！")
            except Exception as e2:
                print(f"通过 href 属性查找失败: {e2}")
                # 尝试通过 XPath 查找
                unfinished_course_link = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '未完成课程')]"))
                )
                print("通过 XPath 找到'未完成课程'链接！")

        print("点击'未完成课程'...")
        unfinished_course_link.click()

        # 等待页面跳转
        time.sleep(2)
        print(f"点击未完成课程后URL: {driver.current_url}")

        # 循环播放所有未完成的课程（包括大课中的所有小课）
        # 持续查找"进入学习"按钮，直到找不到为止
        course_count = 0
        max_courses = 1000  # 设置安全上限，防止无限循环

        print("\n开始自动学习所有未完成课程（包括所有小课）...")
        print("=" * 60)

        for _ in range(max_courses):
            course_count += 1
            print(f"\n{'='*60}")
            print(f"正在处理第 {course_count} 个视频课程")
            print(f"{'='*60}")

            # 查找"进入学习"按钮
            print("\n正在查找'进入学习'按钮...")
            time.sleep(2)  # 等待课程列表加载

            try:
                # 尝试通过链接文本查找第一个"进入学习"按钮
                enter_study_link = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "进入学习"))
                )
                print("通过链接文本找到'进入学习'按钮！")
            except Exception as e:
                print(f"通过链接文本查找失败: {e}")
                try:
                    # 尝试通过 XPath 查找
                    enter_study_link = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '进入学习')]"))
                    )
                    print("通过 XPath 找到'进入学习'按钮！")
                except Exception as e2:
                    print(f"通过 XPath 查找失败: {e2}")
                    try:
                        # 尝试通过 CSS 选择器查找 table-operate 下的链接
                        enter_study_link = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, ".table-operate a"))
                        )
                        print("通过 CSS 选择器找到'进入学习'按钮！")
                    except Exception as e3:
                        print(f"所有方法都失败了: {e3}")
                        print(f"\n🎉 恭喜！所有课程（包括所有小课）已完成！")
                        print(f"共完成 {course_count - 1} 个视频课程的学习")
                        break  # 没有更多课程，退出循环

            # 记录当前窗口句柄
            current_window = driver.current_window_handle
            print(f"当前窗口句柄: {current_window}")

            print("点击'进入学习'...")
            enter_study_link.click()

            # 等待新窗口打开
            time.sleep(3)

            # 获取所有窗口句柄
            all_windows = driver.window_handles
            print(f"所有窗口句柄: {all_windows}")
            print(f"窗口数量: {len(all_windows)}")

            # 切换到新打开的窗口
            for window in all_windows:
                if window != current_window:
                    driver.switch_to.window(window)
                    print(f"已切换到新窗口")
                    break

            # 等待播放页面加载
            time.sleep(2)
            print(f"进入学习后URL: {driver.current_url}")

            # 查找并点击播放按钮
            print("\n正在查找视频播放按钮...")
            time.sleep(2)  # 等待视频加载

            try:
                # 尝试点击大的播放按钮
                play_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".vjs-big-play-button"))
                )
                print("找到大播放按钮！")
            except Exception as e:
                print(f"查找大播放按钮失败: {e}")
                try:
                    # 尝试点击控制栏的播放按钮
                    play_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".vjs-play-control"))
                    )
                    print("找到控制栏播放按钮！")
                except Exception as e2:
                    print(f"查找控制栏播放按钮失败: {e2}")
                    # 尝试通过 aria-label 查找
                    play_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='play video']"))
                    )
                    print("通过 aria-label 找到播放按钮！")

            print("点击播放按钮...")
            play_button.click()

            # 等待视频开始播放
            time.sleep(3)
            print("视频已开始播放！")

            # 获取视频播放时长
            print("\n正在获取视频时长信息...")
            time.sleep(3)  # 等待视频完全加载

            try:
                # 使用 JavaScript 直接从 video 元素获取时长信息
                current_seconds = driver.execute_script("""
                    var video = document.getElementById('study_video_html5_api');
                    return video ? Math.floor(video.currentTime) : 0;
                """)

                duration_seconds = driver.execute_script("""
                    var video = document.getElementById('study_video_html5_api');
                    return video ? Math.floor(video.duration) : 0;
                """)

                print(f"当前播放时间: {current_seconds} 秒 ({current_seconds // 60} 分 {current_seconds % 60} 秒)")
                print(f"视频总时长: {duration_seconds} 秒 ({duration_seconds // 60} 分 {duration_seconds % 60} 秒)")

                remaining_seconds = duration_seconds - current_seconds

                print(f"剩余播放时间: {remaining_seconds} 秒 ({remaining_seconds // 60} 分 {remaining_seconds % 60} 秒)")

                if remaining_seconds > 0:
                    print(f"\n等待视频播放完成...")
                    time.sleep(remaining_seconds + 5)  # 多等待5秒确保播放完成
                    print("视频播放完成！")
                else:
                    print("视频已播放完成或时间解析错误")
                    print("使用默认等待时间 60 秒")
                    time.sleep(60)

            except Exception as e:
                print(f"获取视频时长失败: {e}")
                print("使用默认等待时间 60 秒")
                time.sleep(60)

            # 关闭当前 tab
            print("\n正在关闭当前播放页面...")
            driver.close()

            # 切换回主窗口
            driver.switch_to.window(current_window)
            print("已切换回主窗口")

            # 刷新页面
            print("正在刷新页面...")
            driver.refresh()
            time.sleep(3)
            print(f"刷新后URL: {driver.current_url}")

            print(f"\n✅ 第 {course_count} 个视频课程已完成！")
            print("准备查找下一个课程...")
            # 继续循环，查找下一个"进入学习"按钮

        # 如果循环正常结束（达到上限）
        print("\n" + "="*60)
        print(f"⚠️ 已达到处理上限（{max_courses}个视频）")
        print(f"实际完成 {course_count} 个视频课程")
        print("="*60)

    except Exception as e:
        print(f"发生错误: {e}")
        print(f"当前URL: {driver.current_url}")
        import traceback
        traceback.print_exc()

    finally:
        # 可选：关闭浏览器（如果需要保持浏览器打开，注释掉下面这行）
        # driver.quit()
        print("脚本执行结束")
        pass

if __name__ == '__main__':
    main()