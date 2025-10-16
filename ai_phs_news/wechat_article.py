#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章发布模块
使用 wechatpy 实现公众号图文消息的创建和发布

功能特性:
  - 支持创建草稿文章（推荐）
  - 支持直接发布为永久素材
  - 封面图片支持三种方式：
    1. 本地图片路径（自动上传）
    2. 已有的 media_id
    3. None（不设置封面）
  
使用示例:
from ai_phs_news.wechat_article import WeChatArticlePublisher, create_html_content

# 创建发布器
publisher = WeChatArticlePublisher(app_id, app_secret)

# 方式1: 使用本地图片
publisher.create_draft_article(
    title="标题",
    author="作者",
    content="<p>内容</p>",
    thumb_image="cover.png"  # 本地图片路径
)

# 方式2: 使用已有 media_id
publisher.create_draft_article(
    title="标题",
    author="作者", 
    content="<p>内容</p>",
    thumb_image="MvcyvW-8y3M9zOIu1qlEL..."  # media_id
)
"""

import os
import fire
from loguru import logger
from .config import global_config
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMedia, WeChatMaterial
from .llm import LLMClient
from pydantic import BaseModel
from .data_format import PlatformArticlePublisher

class WeChatArticlePublisher(LLMClient, PlatformArticlePublisher):
    """微信公众号文章发布器"""
    
    def __init__(self):
        """
        初始化微信客户端
        """
        self.client = WeChatClient(global_config.WECHAT_APP_ID, global_config.WECHAT_APP_SECRET)
        self.media = WeChatMedia(self.client)
        self.material = WeChatMaterial(self.client)
    
    def upload_image(self, image_path):
        """
        上传图片到微信服务器
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            str: 图片的 media_id
        """
        logger.info(f"正在上传图片: {image_path}")
        
        with open(image_path, 'rb') as f:
            result = self.media.upload('image', f)
        
        media_id = result['media_id']
        logger.success(f"图片上传成功，media_id: {media_id}")
        return media_id
    
    def upload_thumb_image(self, image_path):
        """
        上传封面图片（永久素材）
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            str: 图片的 media_id
        """
        logger.info(f"正在上传封面图片: {image_path}")
        
        with open(image_path, 'rb') as f:
            result = self.material.add('image', f)
        
        media_id = result['media_id']
        logger.success(f"封面图片上传成功，media_id: {media_id}")
        return media_id
    
    def create_article(self, title, author, content, thumb_media_id=None, 
                      content_source_url='', digest='', show_cover_pic=1):
        """
        创建图文消息
        
        Args:
            title: 文章标题
            author: 作者
            content: 文章内容（HTML格式）
            thumb_media_id: 封面图片的 media_id（可选）
            content_source_url: 原文链接（可选）
            digest: 摘要（可选，不填则自动生成）
            show_cover_pic: 是否显示封面，1为显示，0为不显示
            
        Returns:
            dict: 创建结果
        """
        logger.info("正在创建图文消息...")
        
        # 构建文章数据
        article_data = {
            'title': title,
            'author': author,
            'digest': digest,
            'show_cover_pic': show_cover_pic,
            'content': content,
            'content_source_url': content_source_url
        }
        
        # 只有提供了封面图片才添加 thumb_media_id
        if thumb_media_id:
            article_data['thumb_media_id'] = thumb_media_id
        
        result = self.material.add_articles([article_data])
        logger.success(f"图文消息创建成功，media_id: {result['media_id']}")
        return result
    
    def publish_article(self, title, author, content, thumb_image=None,
                       content_source_url='', digest='', show_cover_pic=1):
        """
        发布文章的完整流程
        
        Args:
            title: 文章标题
            author: 作者
            content: 文章内容（HTML格式）
            thumb_image: 封面图片，支持三种方式：
                        - None: 不设置封面
                        - str (以.jpg/.png结尾): 本地图片路径，将自动上传
                        - str (其他): 已有的 media_id
            content_source_url: 原文链接（可选）
            digest: 摘要（可选）
            show_cover_pic: 是否显示封面
            
        Returns:
            dict: 发布结果
        """
        logger.info("="*50)
        logger.info("开始发布微信公众号文章")
        logger.info("="*50)
        
        # 1. 处理封面图片
        thumb_media_id = self._process_thumb_image(thumb_image)
        
        # 2. 创建图文消息
        result = self.create_article(
            title=title,
            author=author,
            content=content,
            thumb_media_id=thumb_media_id,
            content_source_url=content_source_url,
            digest=digest,
            show_cover_pic=show_cover_pic
        )
        
        logger.success("="*50)
        logger.success("文章发布完成！")
        logger.success(f"Media ID: {result['media_id']}")
        logger.success("="*50)
        
        return result
    
    def _process_thumb_image(self, thumb_image):
        """
        处理封面图片，支持多种输入方式
        
        Args:
            thumb_image: None / 本地路径 / media_id
            
        Returns:
            str: media_id 或 None
        """
        if thumb_image is None:
            logger.warning("未提供封面图片")
            return global_config.WECHAT_MEDIA_ID
        
        # 判断是本地路径还是 media_id
        if isinstance(thumb_image, str):
            # 如果是图片文件路径（包含常见图片扩展名）
            if any(thumb_image.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                if os.path.exists(thumb_image):
                    logger.info(f"检测到本地图片路径: {thumb_image}")
                    return self.upload_thumb_image(thumb_image)
                else:
                    logger.warning(f"图片文件不存在: {thumb_image}")
                    return None
            else:
                # 假定是 media_id
                logger.info(f"使用已有的 media_id: {thumb_image[:20]}...")
                return thumb_image
        
        return None
    
    def create_draft_article(self, title, author, content, thumb_image=None,
                            content_source_url='', digest='', show_cover_pic=1,
                            need_open_comment=0, only_fans_can_comment=0):
        """
        创建草稿文章（推荐使用，可在后台预览）
        
        Args:
            title: 文章标题
            author: 作者
            content: 文章内容（HTML格式）
            thumb_image: 封面图片，支持三种方式：
                        - None: 不设置封面
                        - str (以.jpg/.png结尾): 本地图片路径，将自动上传
                        - str (其他): 已有的 media_id
            content_source_url: 原文链接（可选）
            digest: 摘要（可选）
            show_cover_pic: 是否显示封面
            need_open_comment: 是否打开评论，0不打开，1打开
            only_fans_can_comment: 是否粉丝才可评论，0所有人可评论，1粉丝才可评论
            
        Returns:
            str: 草稿的 media_id
        """
        logger.info("="*50)
        logger.info("开始创建草稿文章")
        logger.info("="*50)
        
        # 1. 处理封面图片
        thumb_media_id = self._process_thumb_image(thumb_image)
        logger.debug(f"thumb_media_id: {thumb_media_id}")
        
        # 2. 创建草稿
        logger.info("正在创建草稿...")
        
        # 构建文章数据
        article_data = {
            'title': title,
            'author': author,
            'digest': digest,
            'content': content,
            'content_source_url': content_source_url,
            'show_cover_pic': show_cover_pic,
            'need_open_comment': need_open_comment,
            'only_fans_can_comment': only_fans_can_comment
        }
        
        # 只有提供了封面图片才添加 thumb_media_id
        if thumb_media_id:
            article_data['thumb_media_id'] = thumb_media_id

        
        articles = {
            'articles': [article_data]
        }
        
        try:
            result = self.client.post(
                'draft/add',
                data=articles
            )
            
            media_id = result['media_id']
            logger.success(f"草稿创建成功，media_id: {media_id}")
            logger.success("="*50)
            logger.success("草稿创建完成！请到公众号后台查看并发布")
            logger.success("="*50)
            
            return media_id
        except Exception as e:
            logger.error(f"创建草稿失败，详细错误: {e}")
            # 如果草稿接口不可用，尝试使用永久素材方式
            logger.info("尝试使用永久素材方式...")
            return self._create_permanent_article(title, author, content, thumb_media_id, 
                                                  content_source_url, digest, show_cover_pic)
    
    def _create_permanent_article(self, title, author, content, thumb_media_id=None,
                                  content_source_url='', digest='', show_cover_pic=1):
        """
        创建永久图文素材（备用方案）
        
        Returns:
            str: 永久素材的 media_id
        """
        logger.info("正在创建永久图文素材...")
        
        article_data = {
            'title': title,
            'author': author,
            'digest': digest,
            'show_cover_pic': show_cover_pic,
            'content': content,
            'content_source_url': content_source_url
        }
        
        # 只有提供了封面图片才添加 thumb_media_id
        if thumb_media_id:
            article_data['thumb_media_id'] = thumb_media_id
            
        result = self.material.add_articles([article_data])
        media_id = result['media_id']
        logger.success(f"永久图文素材创建成功，media_id: {media_id}")
        logger.success("="*50)
        logger.success("图文素材创建完成！")
        logger.success("="*50)
        
        return media_id

    def generate_article(self, content, title="", author="", thumb_image=None,
                            content_source_url='', digest='', show_cover_pic=1,
                            need_open_comment=0, only_fans_can_comment=0):
        """
        生成文章
        """
        messages = [{"role": "system", "content": "你是一个有用的助手"},
                    {
            "role": "user", "content": f"""{content} 
            - 将上诉内容使用 html 的渲染出来
            - 符合微信公众号风格，样式颜色合理，边框合理
            - 该用标题的使用标题
            - 该使用列表的使用列表
            - 该使用段落的使用段落
            - 该使用图片的使用图片
            - 该使用超级链接的加上链接点击可以跳转
            - 使用section 进行布局，样式现代科技， 演示精美，科技感十足，有超级链接的加上链接点击可以跳转
            - 返回结构如下：
            ```html 
            <section>
                <p>文章内容</p>
            </section>
            ```
            """}]
        html_content = self.chat(messages=messages)
        # 提取html_content中的section标签内容
        html_content = html_content.split("```html")[1].split("```")[0]
        media_id = self.create_draft_article(title=title, author=author, content=html_content, thumb_image=thumb_image,
                                  content_source_url=content_source_url, digest=digest, show_cover_pic=show_cover_pic,
                                  need_open_comment=need_open_comment, only_fans_can_comment=only_fans_can_comment)
        return media_id

    def publish(self, content: str, title: str = "每日AI资讯精华", author: str = "AI小助手", digest: str = "", data_type: str = "markdown"):
        """
        发布微信公众号文章
        """
        media_id = self.create_draft_article(title=title, author=author, content=content)
        return media_id

__all__ = ['WeChatArticlePublisher']

publisher = WeChatArticlePublisher()


class CLI:
    """微信公众号文章发布命令行工具
    
    使用示例:
        # 创建草稿文章
        python -m ai_phs_news.wechat_article draft --title "标题" --author "作者" --content "内容" --thumb_image "封面.jpg"
        
        # 使用AI生成文章
        python -m ai_phs_news.wechat_article generate --title "标题" --author "作者" --content "原始内容" --thumb_image "media_id"
        
        # 上传图片
        python -m ai_phs_news.wechat_article upload --image_path "封面.jpg"
        
        # 运行示例
        python -m ai_phs_news.wechat_article example
    """
    
    def __init__(self):
        """初始化发布器"""
        self.publisher = WeChatArticlePublisher()
    
    def draft(self, title, author, content, thumb_image=None, 
              content_source_url='', digest='', show_cover_pic=1,
              need_open_comment=0, only_fans_can_comment=0):
        """
        创建草稿文章
        
        Args:
            title: 文章标题
            author: 作者
            content: 文章内容（HTML格式）
            thumb_image: 封面图片（本地路径或media_id）
            content_source_url: 原文链接
            digest: 摘要
            show_cover_pic: 是否显示封面 (0或1)
            need_open_comment: 是否打开评论 (0或1)
            only_fans_can_comment: 是否仅粉丝可评论 (0或1)
        """
        media_id = self.publisher.create_draft_article(
            title=title,
            author=author,
            content=content,
            thumb_image=thumb_image,
            content_source_url=content_source_url,
            digest=digest,
            show_cover_pic=show_cover_pic,
            need_open_comment=need_open_comment,
            only_fans_can_comment=only_fans_can_comment
        )
        return media_id
    
    def generate(self, content, title="每日AI资讯精华", author="AI小助手", 
                thumb_image=None, content_source_url='', digest='', 
                show_cover_pic=1, need_open_comment=0, only_fans_can_comment=0):
        """
        使用AI生成并创建文章
        
        Args:
            content: 原始内容（将通过AI转换为HTML格式）
            title: 文章标题
            author: 作者
            thumb_image: 封面图片（本地路径或media_id）
            content_source_url: 原文链接
            digest: 摘要
            show_cover_pic: 是否显示封面 (0或1)
            need_open_comment: 是否打开评论 (0或1)
            only_fans_can_comment: 是否仅粉丝可评论 (0或1)
        """
        media_id = self.publisher.generate_article(
            content=content,
            title=title,
            author=author,
            thumb_image=thumb_image,
            content_source_url=content_source_url,
            digest=digest,
            show_cover_pic=show_cover_pic,
            need_open_comment=need_open_comment,
            only_fans_can_comment=only_fans_can_comment
        )
        return media_id
    
    def upload(self, image_path, permanent=True):
        """
        上传图片到微信服务器
        
        Args:
            image_path: 图片文件路径
            permanent: 是否作为永久素材 (True为封面图片，False为临时素材)
        """
        if permanent:
            media_id = self.publisher.upload_thumb_image(image_path)
        else:
            media_id = self.publisher.upload_image(image_path)
        
        logger.success(f"图片上传成功: {media_id}")
        return media_id
    
    def publish(self, title, author, content, thumb_image=None,
               content_source_url='', digest='', show_cover_pic=1):
        """
        发布文章（创建永久素材）
        
        Args:
            title: 文章标题
            author: 作者
            content: 文章内容（HTML格式）
            thumb_image: 封面图片（本地路径或media_id）
            content_source_url: 原文链接
            digest: 摘要
            show_cover_pic: 是否显示封面 (0或1)
        """
        result = self.publisher.publish_article(
            title=title,
            author=author,
            content=content,
            thumb_image=thumb_image,
            content_source_url=content_source_url,
            digest=digest,
            show_cover_pic=show_cover_pic
        )
        return result
    
    def example(self):
        """运行示例：使用AI生成并发布示例文章"""
        # 文章信息
        article_title = "每日AI资讯精华"
        article_author = "AI小助手"
        
        thumb_image = "MvcyvW-8y3M9zOIu1qlELyFsdZmT-hDZymVqSPW6r-pSwrzl_9aD2tW3tJGqVn9L"
        
        content = """
        每日AI资讯精华 
        最新论文:  VisCoP：面向视觉语言模型视频领域自适应的视觉探测技术。 
        最新论文:  通过世界中的基础实现空间推理。 
        最新论文:  Bee：一个高质量语料库与全栈套件，旨在解锁先进的完全开放多模态大语言模型。 
        最新模型:  Qwen/Qwen3-VL-8B-Thinking 
        最新模型:  lightx2v/Wan2.2-I2V-A14B-Moe-Distill-Lightx2v 
        最新资讯:  "AI 泡沫"是否正在酝酿？——用数据说话 
        最新资讯:  后摩智能陶冶：M50 AI芯片处于可送测阶段拟年底量产 
        最新资讯:  云天励飞携全栈AI推理芯片产品亮相湾芯展，引领"推理时代"新赛道 
        最新资讯:  中国资产反攻，A、港AI蓄力领涨，电子ETF、港股互联网ETF劲升逾2.5%，资金高歌猛进，医药强势回血 
        最新资讯:  苹果M5芯片登场：10核CPU、10核GPU，AI性能飙到3.5倍 
        最新资讯:  自进化AI原生手机！荣耀Magic8系列发布，售价4499元起 
        最新资讯:  刚刚，荣耀整了个大活，掏出机器人手机！发最强AI搭子 
        最新资讯:  【2025年欧洲通讯展（NetworkX 2025）期间，广和通发布家庭智享融合CPE解决方案，以 "5G+AI+场景" 的融合创新，为全球5G FWA 行业提供AI解决方案，充分发挥AI Agent和AI大模型的无限潜力。】PjTime.COM 行业新闻 
        每日精选:  谷歌推出新款视频生成模型 Veo 3.1 
        每日精选:  Anthropic 发布了 Claude Haiku 4.5，速度翻倍价格大砍 
        活在当下，珍惜眼前。--林清玄 
        """
        
        return self.generate(
            title=article_title,
            author=article_author,
            content=content,
            thumb_image=thumb_image,
        )


if __name__ == '__main__':
    fire.Fire(CLI)