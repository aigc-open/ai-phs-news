

from re import T
from .config import global_config
from WorkWeixinRobot.work_weixin_robot import WWXRobot
from loguru import logger
from .data_format import PlatformArticlePublisher



class WxworkArticlePublisher(PlatformArticlePublisher):
    """企业微信文章发布器"""
    
    def __init__(self):
        """
        初始化企业微信客户端
        """
        self.keys = global_config.WEIXIN_ROBOT_KEYS.split(",")
    
    def publish(self, content: str, title: str = "每日AI资讯精华", author: str = "AI小助手"):
        """
        发布企业微信文章
        
        Args:
            content: 文章内容(支持 markdown、文本等多种格式)
            title: 文章标题（企业微信markdown消息无显式标题，仅用于日志或后续扩展）
            author: 作者（未用，保留与 wechat_article 接口一致性）
        """

        for key in self.keys:
            try:
                wwxrbt = WWXRobot(key=key)
                wwxrbt.send_markdown(content=content)
                logger.success(f"企业微信推送成功: {key}")
            except Exception as e:
                logger.error(f"企业微信推送失败: {key}, error: {e}")
                
        return True
    
    
    
