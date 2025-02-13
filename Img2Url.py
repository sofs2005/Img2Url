# encoding:utf-8
import os
import json
import base64
import requests
import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *

@plugins.register(
    name="Img2Url",
    desire_priority=200,
    hidden=False,
    desc="图片转链接插件",
    version="1.3",
    author="sofs2005",
)
class Img2Url(Plugin):
    def __init__(self):
        super().__init__()
        # 加载配置
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                self.imgbb_api_key = config.get("imgbb_api_key", "")
                # Lsky Pro 配置
                self.lsky_api_url = config.get("lsky_api_url", "")
                self.lsky_token = config.get("lsky_token", "")  # 直接使用配置的 token
                self.upload_service = config.get("upload_service", "imgbb")
        except Exception as e:
            logger.error(f"[Img2Url] 加载配置文件失败: {e}")
            self.imgbb_api_key = None
            self.lsky_api_url = None
            self.lsky_token = None
            self.upload_service = "imgbb"

        if not (self.imgbb_api_key or (self.lsky_api_url and self.lsky_token)):
            logger.error("[Img2Url] 请在config.json中配置图床API信息")

        # 设置触发词和状态标记
        self.trigger_word = "传图"
        self.waiting_for_image = {}  # 修改为字典，值可以是URL列表
        
        # 注册消息处理器
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Img2Url] 插件初始化成功")

    def upload_to_imgbb(self, base64_image: str) -> str:
        """上传base64图片到ImgBB"""
        try:
            data = {
                'key': self.imgbb_api_key,
                'image': base64_image
            }
            
            response = requests.post(
                'https://api.imgbb.com/1/upload',
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    logger.info("[Img2Url] 图片上传到ImgBB成功")
                    return result['data']['url']
                else:
                    logger.error(f"[Img2Url] 上传到ImgBB失败: {result.get('error', {}).get('message', '未知错误')}")
            else:
                logger.error(f"[Img2Url] 上传到ImgBB请求失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"[Img2Url] 上传到ImgBB时发生错误: {e}")
        return None

    def upload_to_lsky(self, base64_image: str) -> str:
        """上传图片到Lsky Pro"""
        try:
            # 解码base64图片数据
            image_data = base64.b64decode(base64_image)
            
            # 准备请求头
            headers = {
                "Authorization": f"Bearer {self.lsky_token}",  # 直接使用配置的 token
                "Accept": "application/json"
            }
            
            # 准备文件数据
            files = {
                'file': ('image.png', image_data, 'image/png')
            }
            
            # 发送上传请求
            api_url = self.lsky_api_url.rstrip('/')  # 移除末尾的斜杠
            upload_url = f"{api_url}/upload"
            
            logger.debug(f"[Img2Url] 开始上传图片到: {upload_url}")
            
            response = requests.post(
                upload_url,
                headers=headers,
                files=files
            )
            
            logger.debug(f"[Img2Url] 上传响应状态码: {response.status_code}")
            logger.debug(f"[Img2Url] 上传响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status'):
                    logger.info("[Img2Url] 图片上传到Lsky Pro成功")
                    return result['data']['links']['url']
                else:
                    logger.error(f"[Img2Url] 上传到Lsky Pro失败: {result.get('message', '未知错误')}")
            else:
                logger.error(f"[Img2Url] 上传到Lsky Pro请求失败: {response.status_code}")
                logger.error(f"[Img2Url] 响应内容: {response.text}")
                
        except Exception as e:
            logger.error(f"[Img2Url] 上传到Lsky Pro时发生错误: {e}")
        return None

    def get_image_data(self, msg, content):
        """获取图片数据的辅助函数"""
        try:
            # 1. 尝试从msg.prepare()获取图片路径
            if hasattr(msg, 'prepare'):
                try:
                    msg.prepare()
                    if isinstance(content, str) and os.path.exists(content):
                        with open(content, 'rb') as f:
                            image_data = f.read()
                        logger.debug("[Img2Url] 成功从msg.prepare()获取图片数据")
                        return base64.b64encode(image_data).decode('utf-8')
                except Exception as e:
                    logger.warning(f"[Img2Url] 使用msg.prepare()获取图片失败: {e}")

            # 2. 尝试从原始消息的download方法获取
            if hasattr(msg, '_rawmsg') and hasattr(msg._rawmsg, 'download'):
                try:
                    file_name = msg._rawmsg.get('FileName', 'temp.png')
                    temp_path = os.path.join(os.getcwd(), 'tmp', file_name)
                    msg._rawmsg.download(temp_path)
                    
                    if os.path.exists(temp_path):
                        with open(temp_path, 'rb') as f:
                            image_data = f.read()
                        try:
                            os.remove(temp_path)
                        except:
                            pass
                        return base64.b64encode(image_data).decode('utf-8')
                except Exception as e:
                    logger.warning(f"[Img2Url] 使用_rawmsg.download获取图片失败: {e}")

            # 3. 尝试从Text属性获取
            if hasattr(msg, '_rawmsg') and 'Text' in msg._rawmsg:
                try:
                    text_fn = msg._rawmsg['Text']
                    if callable(text_fn):
                        temp_path = os.path.join(os.getcwd(), 'tmp', 'temp.png')
                        text_fn(temp_path)
                        
                        if os.path.exists(temp_path):
                            with open(temp_path, 'rb') as f:
                                image_data = f.read()
                            try:
                                os.remove(temp_path)
                            except:
                                pass
                            return base64.b64encode(image_data).decode('utf-8')
                except Exception as e:
                    logger.warning(f"[Img2Url] 从Text获取图片数据失败: {e}")

            logger.error("[Img2Url] 所有获取图片数据的方法都失败了")
            return None

        except Exception as e:
            logger.error(f"[Img2Url] 获取图片数据时发生错误: {e}")
            return None

    def on_handle_context(self, e_context: EventContext):
        """处理消息"""
        content = e_context['context'].content
        msg = e_context['context']['msg']
        
        if not msg.from_user_id:
            return
            
        user_id = msg.from_user_id

        # 处理文本消息中的触发词
        if e_context['context'].type == ContextType.TEXT:
             if self.trigger_word in content:
                 self.waiting_for_image[user_id] = []  # 初始化用户上传列表
                 e_context['reply'] = Reply(ReplyType.TEXT, "请发送需要转换的图片")
                 e_context.action = EventAction.BREAK_PASS
                 return
             elif user_id in self.waiting_for_image:
                 # 如果用户发送的是非图片消息，则发送已上传的图片链接
                 if self.waiting_for_image[user_id]:
                     image_urls = self.waiting_for_image[user_id]
                     
                     # 组装所有图片的URL到一个字符串中
                     url_text = "====== 图片链接汇总 ======\n"
                     for index, url in enumerate(image_urls, start=1):
                         url_text += f"{index}. {url}\n"
                     url_text += "====================="

                     e_context['reply'] = Reply(ReplyType.TEXT, url_text)
                     e_context['context'].kwargs['no_image_parse'] = True
                     e_context.action = EventAction.BREAK_PASS
                 del self.waiting_for_image[user_id] # 清除等待状态
                 return

        # 处理图片消息
        if e_context['context'].type == ContextType.IMAGE and user_id in self.waiting_for_image:
            try:
                logger.debug(f"[Img2Url] 开始处理图片消息: {msg}")
                
                # 获取图片数据
                base64_data = self.get_image_data(msg, content)
                if not base64_data:
                    logger.error("[Img2Url] 无法获取图片数据")
                    e_context['reply'] = Reply(ReplyType.ERROR, "无法获取图片数据，请重试")
                    return

                logger.debug("[Img2Url] 成功获取图片数据，准备上传")
                
                # 根据配置选择上传服务
                if self.upload_service == "lsky" and self.lsky_api_url:
                    image_url = self.upload_to_lsky(base64_data)
                else:
                    image_url = self.upload_to_imgbb(base64_data)

                if not image_url:
                    e_context['reply'] = Reply(ReplyType.ERROR, "上传图片失败")
                    return
                
                # 获取当前图片的序号
                current_index = len(self.waiting_for_image[user_id]) + 1
                
                # 将图片URL添加到用户列表
                self.waiting_for_image[user_id].append(image_url)
                
                # 立即返回包含 URL 的消息, 并带上当前序号
                url_text = f"====== 图片上传成功 ======\n{current_index}. {image_url}\n====================="
                e_context['reply'] = Reply(ReplyType.TEXT, url_text)
                e_context['context'].kwargs['no_image_parse'] = True
                e_context.action = EventAction.BREAK_PASS
            
            except Exception as e:
                logger.error(f"[Img2Url] 处理图片时发生错误: {e}")
                e_context['reply'] = Reply(ReplyType.ERROR, f"处理图片时发生错误: {e}")
    
    def get_help_text(self, **kwargs):
        help_text = "图片转链接插件使用说明：\n"
        help_text += "1. 发送'图转链接'，收到反馈消息后再发送图片\n"
        help_text += "2. 插件会自动上传图片并返回可访问的URL\n"
        help_text += "3. 您可以连续发送图片，插件会立即返回每张图片的链接，发送其他文本消息将会结束图片上传并返回所有链接的汇总\n"
        return help_text
