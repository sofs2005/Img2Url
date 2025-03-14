# Img2Url

Img2Url 是一款适用于 dify-on-wechat 的图片处理插件，能够将用户上传到微信的图片转换为在线URL链接，方便对图片以其他途径进行后续处理。

该插件使用起来非常容易，只需按以下步骤简单操作即可。

# 一. 配置图床服务
支持两种图床服务，可以选择其中之一进行配置：

## 方式1：ImgBB图床
1. 注册并登录图床服务网站 https://imgbb.com/
2. 点击个人主页左上角的关于➡️API，点击Add API Key，复制备用

## 方式2：Lsky Pro图床
1. 准备你的 Lsky Pro 信息：
   - API Token（在 Lsky Pro 管理后台获取）
   - API地址（通常格式为：`http://your-domain/api/v1`）

# 二. 安装插件和配置config文件
1. 在微信机器人聊天窗口输入命令：
   ```
   #installp https://github.com/sofs2005/Img2Url.git
   ```

2. 进入 config.json 文件，根据选择的图床服务配置相应参数：

   方式1：使用 ImgBB 图床
   ```json
   {
       "imgbb_api_key": "your_imgbb_api_key",
       "upload_service": "imgbb"
   }
   ```

   方式2：使用 Lsky Pro 图床
   ```json
   {
       "lsky_api_url": "http://your.lsky.pro/api/v1",
       "lsky_token": "your_api_token",
       "upload_service": "lsky"
   }
   ```

3. 重启 dify-on-wechat 项目

4. 在微信机器人聊天窗口输入 #scanp 命令扫描新插件是否已添加至插件列表

5. 输入 #help Img2Url 查看帮助信息，正常返回则表示插件安装成功

# 三. 使用说明
1. 发送'图转链接'，收到反馈消息后再发送图片，机器人会自动将图片上传并返回可访问的URL链接

2. 支持的图片格式：
   - PNG
   - JPG/JPEG
   - GIF
   - BMP
   - WebP

3. 图片大小限制：
   - ImgBB：单个文件不超过32MB
   - Lsky Pro：取决于服务器配置，一般不超过10MB

# 四. 常见问题
1. 如果上传失败，请检查：
   - ImgBB：
     - API Key 是否正确
   - Lsky Pro：
     - API 地址是否正确（必须包含 /api/v1）
     - API Token 是否正确
     - 账号是否有上传权限
   - 通用检查：
     - 网络连接是否正常
     - 图片大小是否超限
     - 配置文件中的 upload_service 是否正确设置

2. 如遇到其他问题，请在 GitHub 仓库提交 Issue

# 五. 版本信息
- 版本：1.3
- 更新内容：
  - 优化 Lsky Pro 图床支持
  - 简化认证流程，直接使用 API Token
  - 改进错误处理和日志记录
  - 优化配置文件结构
- 作者：sofs2005
- 最后更新：2025-01-07
- Github个人主页：https://github.com/sofs2005

本插件基于Lingyuzhou的Img2Url插件修改，另本插件中连续发送图片功能由深蓝老大提供代码支持，感谢两位大佬的贡献。

# 六. 打赏支持

如果您觉得这个插件对您有帮助，欢迎扫描下方二维码进行打赏支持，让我能够持续改进和开发更多实用功能。

![微信打赏码](https://github.com/sofs2005/difytask/raw/main/img/wx.png?raw=true)