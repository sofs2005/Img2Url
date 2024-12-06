# Img2Url

Img2Url 是一款适用于 chatgpt-on-wechat 的图片处理插件，能够用户上传到微信的图片转换为在线URL链接，方便对图片以其他途径进行后续处理。

该插件使用起来非常容易，只需按以下步骤简单操作即可。

# 一. 获取图床API密钥
1. 注册并登录图床服务网站https://imgbb.com/

2. 点击个人主页左上角的关于→API，点击Add API Key，复制备用

# 二. 安装插件和配置config文件
1. 在微信机器人聊天窗口输入命令：
   ```
   #installp https://github.com/Lingyuzhou111/Img2Url.git
   ```

2. 进入 config.json 文件，配置第一步获取的图床 API Key

3. 重启 chatgpt-on-wechat 项目

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

3. 图片大小限制：单个文件不超过5MB

# 四. 常见问题
1. 如果上传失败，请检查：
   - API Key 是否正确
   - 网络连接是否正常
   - 图片大小是否超限

2. 如遇到其他问题，请在 GitHub 仓库提交 Issue

# 五. 版本信息
- 版本：1.0
- 作者：Lingyuzhou
- 最后更新：2024-12-06
- 如在使用时遇到问题请联系插件作者 
- Github个人主页https://github.com/Lingyuzhou111
