## 继续教育网络刷课脚本（Mac 版）

### 脚本说明

本脚本用于自动化完成 **继续教育网络学习平台** 的课程学习，支持自动登录、自动播放视频、智能等待视频完成并循环处理所有未完成课程。

**目标网站**: http://jxjy.gdlink.net.cn/Elearning.GDLink.Student//Home/Index

**适用平台**: Mac OS X

---

### 环境要求

#### 系统环境
- **操作系统**: Mac OS X
- **Python 版本**: Python 3.x
- **浏览器**: Google Chrome

#### Python 依赖
```bash
pip install selenium
```

注意：tkinter 通常在 Mac 的 Python 中已预装，如果没有可通过以下方式安装：
```bash
brew install python-tk
```

#### ChromeDriver

需要下载与 Chrome 浏览器版本匹配的 ChromeDriver。

1. **查看 Chrome 版本**：Chrome 菜单 > 关于 Google Chrome
2. **下载 ChromeDriver**：https://googlechromelabs.github.io/chrome-for-testing/#stable
3. **当前脚本使用版本**：143.0.7499.40
4. **放置位置**：将 `chromedriver` 文件放在与脚本同一目录下

**Mac 安全设置**：
首次使用时，可能需要移除 macOS 的隔离标记：
```bash
cd book_only_mac_can_use
xattr -d com.apple.quarantine ./chromedriver
```

---

### 配置文件说明

#### credentials.txt

在 `book_only_mac_can_use` 目录下创建 `credentials.txt` 文件，格式如下：

```
账号
密码
```

示例：
```
xxxxxxx
MyPassword123
```

**注意**：
- 第一行为账号（身份证号）
- 第二行为密码
- 文件采用 UTF-8 编码
- 请勿将此文件提交到版本控制系统

---

### 使用步骤

1. **准备环境**
   ```bash
   # 安装依赖
   pip install selenium
   
   # 确保 chromedriver 在正确位置
   ls -la chromedriver
   
   # 如需要，移除隔离标记
   xattr -d com.apple.quarantine ./chromedriver
   ```

2. **配置账号密码**
   ```bash
   # 创建并编辑 credentials.txt
   vim credentials.txt
   # 输入账号（第一行）和密码（第二行）
   ```

3. **运行脚本**
   ```bash
   python book.py
   ```

4. **手动操作**
   - 脚本会自动打开浏览器并进入登录页面
   - 会自动填写账号密码
   - **弹出输入框时，请手动输入验证码**
   - 之后脚本会自动完成所有课程学习

5. **等待完成**
   - 脚本会自动处理所有未完成课程
   - 每个视频播放完成后自动进入下一个
   - 所有课程完成后会显示完成提示

---

### 功能特点

#### 1. 智能课程处理
- 自动检测"未完成课程"列表
- 智能循环处理所有小课（不限数量）
- 持续查找"进入学习"按钮直到全部完成

#### 2. 自动视频播放
- 自动点击播放按钮
- 使用 JavaScript 直接获取视频时长
- 精确计算剩余播放时间并智能等待

#### 3. 多窗口管理
- 自动处理新标签页的打开和关闭
- 智能窗口切换
- 自动刷新页面获取最新课程列表

#### 4. iframe 处理
- 自动检测页面中的 iframe
- 智能切换到正确的 iframe 中查找元素

#### 5. 友好的用户交互
- 使用 tkinter 弹出式输入框输入验证码
- 实时打印进度日志
- 详细的错误信息提示

---

### 脚本执行流程

1. 初始化浏览器（最大化窗口）
2. 访问目标网站
3. 自动点击"进入站点"
4. 自动点击"登录"按钮
5. 自动填写账号密码
6. **手动输入验证码**（弹出输入框）
7. 自动点击登录
8. 进入"个人中心"
9. 进入"未完成课程"
10. 循环处理每个课程：
    - 查找"进入学习"按钮
    - 点击进入学习（打开新标签页）
    - 点击视频播放按钮
    - 获取视频时长并等待播放完成
    - 关闭当前标签页
    - 刷新页面
    - 继续查找下一个课程
11. 所有课程完成后显示完成提示

---

### 注意事项

#### 安全性
- `credentials.txt` 包含敏感信息，请勿上传到公开仓库
- 建议在 `.gitignore` 中添加 `credentials.txt`
- 使用完成后建议删除或清空 `credentials.txt`

#### 运行时注意
- 脚本运行期间请勿手动操作浏览器窗口
- 请勿最小化浏览器窗口
- 确保网络连接稳定
- 视频播放期间可能会有广告或提示，脚本会尝试自动处理

#### 异常处理
- 如果脚本卡住不动，请检查页面元素是否发生变化
- 如果验证码输入错误，请重新运行脚本
- 如果遇到网络问题，脚本会打印详细错误信息

#### 性能说明
- 处理速度取决于视频实际时长
- 建议在网络较好的环境下运行
- 长时间运行可能需要保持设备不休眠

---

### 常见问题

**Q: ChromeDriver 报错 "Permission denied"**  
A: 执行 `chmod +x chromedriver` 添加执行权限，或执行 `xattr -d com.apple.quarantine ./chromedriver` 移除隔离标记

**Q: 找不到元素报错**  
A: 网站页面结构可能发生变化，需要更新脚本中的元素定位选择器

**Q: 验证码输入框不显示**  
A: 检查 tkinter 是否正确安装，可尝试重装：`brew reinstall python-tk`

**Q: 脚本提示"所有课程已完成"但实际还有课程**  
A: 可能是页面加载问题，建议刷新页面后重新运行脚本

**Q: 视频播放不完整就跳到下一个**  
A: 脚本会自动计算剩余播放时间，如果出现此问题可能是网络延迟，建议检查网络连接

---

### 技术说明

- **Selenium WebDriver**: 浏览器自动化框架
- **显式等待**: 使用 `WebDriverWait` 和 `expected_conditions` 提高稳定性
- **JavaScript 执行**: 直接从 video 元素获取播放信息
- **多种定位策略**: 支持 LINK_TEXT、XPATH、CSS_SELECTOR、ID 等多种元素定位方式
- **智能循环**: 基于异常捕获的智能循环，无需预知课程数量

---

### 更新日志

**2024-12-15**
- 优化循环逻辑，支持智能处理任意数量的小课
- 改进进度提示信息
- 添加安全上限防止无限循环

**2024-12-10**
- 初始版本
- 实现基本的自动刷课功能
- 支持自动登录和视频播放
- 使用 JavaScript 获取视频时长

---

### 免责声明

本脚本仅供学习和研究使用，使用者应遵守相关网站的使用条款和法律法规。作者不对使用本脚本造成的任何后果承担责任。

---

### 参考资料

- [Selenium Python 文档](https://selenium-python.readthedocs.io/)
- [ChromeDriver 下载](https://googlechromelabs.github.io/chrome-for-testing/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
