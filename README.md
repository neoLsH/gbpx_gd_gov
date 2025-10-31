## 广东省干部培训网络刷课脚本

___

Update Log:

2025.10.31

+ 更新登录时自动点击账号密码登录tab，解决因二维码无法输入账号密码而导致的报错

___

参考：
+ https://www.52pojie.cn/thread-1105553-1-1.html
+ https://199604.com/1401

### 环境准备

+ Windows 系统
+ python3.11
+ pip3.11
+ chrome浏览器
+ chromedriver.exe

### 注意 chromedriver 问题

随着 chrome 浏览器版本升级，本机的 chrome driver 并不适合。需要去进行更新

chrome 需要和 chromedriver 版本匹配，否则会报错

https://googlechromelabs.github.io/chrome-for-testing/#stable


[ChromeDriver 下载/安装详解（Windows / Mac / Linux）](https://blog.csdn.net/weixin_42969320/article/details/154204654)



### 配置文件说明

#### credentials.txt
用于存储账号密码，格式为：
```
用户名
密码
```
示例：
```
xx
xxxxxxx
```


### 使用步骤
+ 找到 `chromedriver.exe` 的位置，在**代码中填写**
+ `credentials.txt` 中输入账号密码
+ 启动程序
+ 验证码在额外的pyautogui输入
+ 程序启动后请勿擅自点击页面，以防页面元素找不到导致运行失败
+ 如果课程播放完成后有考试无法跳过，需手动完成

### 效果
+ 自动打开页面，全屏。
+ 自动点击账号密码登录
+ 自动输入账号密码
+ 自动勾选用户须知
+ 自动登录
+ 自动进入我的选课中循环播放所选课程，播放期间会计算当前时间戳和总视频时长的时间差距进行sleep

### 优化空间
+ 验证码自动识别、填充（考虑使用PIL图片处理+pytesseract图片转文字处理）
+ 自动选课：
  + 设置选课条件：Class_name维度或者XPath维度圈定选课范围，根据总时长、是否有课后答题判断是否需要继续选课，选课时根据条件进行判断

### Bug
+ 目前在刷课过程中会打印日志：该目录下还有xx个视频未学习。但因为xx是来源于js_list，又由于分页一页12项。所以当所选课程大于12时，恒展示为剩余12个视频未学习。且由于视频播放完成后会refresh页面，刷新未播放视频个数。所以不影响使用，只影响console打印。


### 踩坑点
+ 打开Chrome浏览器页面失败，且没有异常报错。可添加以下代码段防反爬
  ```python
  browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })
  ```
+ selenium 4.X以后``find_element``写法发生改变。如果不正确会报traceback
  + before：
    ```python
    browser.find_element_by_id('txtLoginName')
    ```
  + after：
    ```python
    # 引一个新包
    from selenium.webdriver.common.by import By
    
    
    browser.find_element(By.ID, 'txtLoginName')
    ```
+ 页面元素class_name或id更换名称导致selenium寻找失败报错，用console查看新的名称替换即可，测试下来最准确的还是class_name。多个class_name的情况下取第一个
