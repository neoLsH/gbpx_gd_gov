# 在线课程自动化学习脚本集合

本项目包含两个针对不同在线学习平台的自动化刷课脚本，帮助自动完成课程学习任务。

---

## 📚 脚本列表

### 1. 广东省干部培训网络刷课脚本（Windows 版）

**目录**: `gd_training_script/`

**目标平台**: [广东省干部培训网络学习平台](https://gbpx.gd.gov.cn/)

**适用系统**: Windows

**主要功能**:
- 自动登录（密码登录）
- 自动进入我的选课
- 循环播放所有选课内容
- 智能计算视频剩余时长并等待
- 自动处理课程列表分页

**快速开始**:
```bash
cd gd_training_script
# 配置 credentials.txt（账号密码）
# 更新 chromedriver 路径
python test.py
```

**详细文档**: [gd_training_script/README.md](gd_training_script/README.md)

---

### 2. 继续教育网络刷课脚本（Mac 版）

**目录**: `book_only_mac_can_use/`

**目标平台**: [继续教育网络学习平台](http://jxjy.gdlink.net.cn/)

**适用系统**: Mac OS X

**主要功能**:
- 自动登录（身份证号+密码）
- 智能处理 iframe 嵌套页面
- 自动进入个人中心和未完成课程
- 智能循环处理所有小课（不限数量）
- 使用 JavaScript 精确获取视频时长
- 多窗口智能管理
- tkinter 图形界面输入验证码

**快速开始**:
```bash
cd book_only_mac_can_use
# 配置 credentials.txt（账号密码）
# 确保 chromedriver 有执行权限
xattr -d com.apple.quarantine ./chromedriver
python book.py
```

**详细文档**: [book_only_mac_can_use/README.md](book_only_mac_can_use/README.md)

---

## 🛠️ 通用环境要求

### 必备软件
- **Python**: 3.x 版本
- **Google Chrome**: 最新版本
- **ChromeDriver**: 与 Chrome 版本匹配

### Python 依赖
```bash
pip install selenium
pip install pyautogui  # Windows 版需要
```

### ChromeDriver 下载
访问 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/#stable) 下载与你的 Chrome 版本匹配的 ChromeDriver。

**查看 Chrome 版本**:
- Windows: Chrome 菜单 > 帮助 > 关于 Google Chrome
- Mac: Chrome 菜单 > 关于 Google Chrome

---

## 📝 配置说明

### credentials.txt 格式

两个脚本都使用 `credentials.txt` 文件存储账号密码，格式统一为：

```
账号（第一行）
密码（第二行）
```

**示例**:
```
xxxxxxx
MyPassword123
```

**安全提示**:
- ⚠️ 请勿将 `credentials.txt` 提交到版本控制系统
- ✅ 已在 `.gitignore` 中忽略此文件
- 🔒 使用完成后建议删除或清空此文件

---

## 🎯 使用流程对比

| 步骤 | 广东省干部培训（Windows） | 继续教育网络（Mac） |
|------|--------------------------|---------------------|
| 1. 启动 | 运行 `test.py` | 运行 `book.py` |
| 2. 登录 | 自动填写账号密码 | 自动填写账号密码 |
| 3. 验证码 | pyautogui 弹窗输入 | tkinter 弹窗输入 |
| 4. 进入课程 | 自动进入"我的选课" | 自动进入"未完成课程" |
| 5. 播放视频 | 循环播放并计算时长 | 智能循环处理所有小课 |
| 6. 完成 | 手动关闭浏览器 | 自动提示完成 |

---

## 🔧 常见问题

### ChromeDriver 相关

**Q: ChromeDriver 版本不匹配怎么办？**  
A: 访问 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/#stable) 下载对应版本

**Q: Mac 提示 "chromedriver cannot be opened"**  
A: 执行 `xattr -d com.apple.quarantine ./chromedriver` 移除隔离标记

**Q: Windows 提示权限错误**  
A: 右键 chromedriver.exe → 属性 → 解除锁定

### 运行问题

**Q: 找不到页面元素**  
A: 网站可能更新了页面结构，需要更新脚本中的元素选择器

**Q: 脚本卡住不动**  
A: 检查网络连接，确保页面完全加载，不要手动操作浏览器

**Q: 视频没有播放完就跳到下一个**  
A: 可能是网络延迟或时长计算问题，建议检查网络状况

### 账号安全

**Q: credentials.txt 安全吗？**  
A: 此文件仅存储在本地，不会上传。建议使用后立即删除或清空

**Q: 会被检测到自动化操作吗？**  
A: 两个脚本都包含了反检测机制，但仍建议合理使用

---

## 📁 项目结构

```
gbpx_gd_gov/
├── README.md                          # 本文件（总说明）
├── .gitignore                         # Git 忽略配置
├── credentials.txt                    # 根目录账号配置（已忽略）
│
├── gd_training_script/                # 广东省干部培训脚本（Windows）
│   ├── README.md                      # 详细说明文档
│   ├── test.py                        # 主脚本
│   └── credentials.txt                # 账号密码配置（已忽略）
│
└── book_only_mac_can_use/             # 继续教育网络脚本（Mac）
    ├── README.md                      # 详细说明文档
    ├── book.py                        # 主脚本
    ├── chromedriver                   # ChromeDriver 143.0.7499.40
    ├── credentials.txt                # 账号密码配置（已忽略）
    ├── LICENSE.chromedriver           # ChromeDriver 许可证
    └── THIRD_PARTY_NOTICES.chromedriver  # 第三方声明
```

---

## ⚠️ 注意事项

### 运行时注意
1. 脚本运行期间**请勿手动操作浏览器**
2. 确保**网络连接稳定**
3. 建议在**空闲时段运行**，避免影响正常使用
4. 长时间运行需保持**设备不休眠**

### 合规使用
1. 本脚本仅供**学习和个人使用**
2. 请遵守相关网站的**使用条款**
3. 不建议用于**商业目的**
4. 使用者需自行承担**使用风险**

### 功能限制
- 无法处理需要**人工答题**的考试环节
- 对于**防作弊机制较强**的平台可能失效
- 网站**页面改版**后需要更新脚本
- 部分**特殊课程格式**可能不支持

---

## 🔄 更新日志

### 2024-12-15
- ✨ 新增继续教育网络刷课脚本（Mac 版）
- 🎯 优化课程循环逻辑，支持智能处理任意数量小课
- 📝 完善项目文档结构
- 🗂️ 重组项目目录，分离不同平台脚本

### 2024-11-02
- 🎉 初始版本
- ✅ 实现广东省干部培训网络自动刷课
- 🔧 添加自动登录和视频播放功能

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这些脚本。

**改进建议**:
- 增加更多平台支持
- 优化验证码识别（OCR）
- 改进异常处理机制
- 添加日志记录功能
- 支持配置文件自定义

---

## 📄 免责声明

本项目中的所有脚本**仅供学习和研究使用**。使用者应当：

1. 遵守相关法律法规和网站使用条款
2. 不得将脚本用于商业目的
3. 不得影响平台正常运营
4. 自行承担使用产生的一切后果

**作者不对使用本项目脚本造成的任何直接或间接后果承担责任。**

---

## 📚 参考资料

- [Selenium Python 官方文档](https://selenium-python.readthedocs.io/)
- [ChromeDriver 下载](https://googlechromelabs.github.io/chrome-for-testing/)
- [PyAutoGUI 文档](https://pyautogui.readthedocs.io/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

---

## 📧 联系方式

如有问题或建议，请通过 Issue 联系。

---

**⭐ 如果这个项目对你有帮助，欢迎 Star！**
