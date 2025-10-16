#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI PHS News 命令行工具
整合资讯爬取、文章生成和微信发布功能
"""

import fire
from loguru import logger
from .spider import Spider
from .wechat_article import WeChatArticlePublisher
from .config import global_config
from .wxwork_article import WxworkArticlePublisher

class MainCLI:
    """AI PHS News - AI 资讯聚合与发布工具
    
    功能模块:
        spider   - 爬取 AI 资讯（论文、模型、新闻）
        wechat   - 微信公众号文章发布
        workflow - 完整工作流（爬取 + 生成 + 发布）
    
    使用示例:
        # 查看帮助
        ai-phs-news --help
        
        # 爬取资讯
        ai-phs-news spider papers
        ai-phs-news spider news
        
        # 发布文章
        ai-phs-news wechat draft --title "标题" --author "作者" --content "<p>内容</p>"
        
        # 完整工作流
        ai-phs-news workflow daily
    """
    
    def __init__(self):
        """初始化 CLI"""
        self.spider_cli = SpiderCLI()
        self.wechat_cli = WeChatCLI()
        self.workflow_cli = WorkflowCLI()
    
    @property
    def spider(self):
        """资讯爬取模块"""
        return self.spider_cli
    
    @property
    def wechat(self):
        """微信发布模块"""
        return self.wechat_cli
    
    @property
    def workflow(self):
        """工作流模块"""
        return self.workflow_cli


class SpiderCLI:
    """AI 资讯爬虫命令行工具"""
    
    def __init__(self):
        self.spider = Spider()
    
    def papers(self, format='text'):
        """
        爬取最新论文
        
        Args:
            format: 输出格式 (text/json)
        """
        logger.info("开始爬取最新论文...")
        results = self.spider.paper()
        return self._format_output(results, format, "最新论文")
    
    def models(self, format='text'):
        """
        爬取 Hugging Face 最新模型
        
        Args:
            format: 输出格式 (text/json)
        """
        logger.info("开始爬取最新模型...")
        results = self.spider.hugging_face()
        return self._format_output(results, format, "最新模型")
    
    def news(self, source='all', format='text'):
        """
        爬取 AI 相关新闻
        
        Args:
            source: 新闻来源 (all/aibot/duckduckgo/google)
            format: 输出格式 (text/json)
        """
        logger.info(f"开始爬取新闻 (来源: {source})...")
        
        results = []
        if source in ['all', 'aibot']:
            results.extend(self.spider.ai_bot())
        if source in ['all', 'duckduckgo']:
            results.extend(self.spider.duckduckgo())
        if source in ['all', 'google']:
            results.extend(self.spider.google())
        
        return self._format_output(results, format, "最新资讯")
    
    def all(self, format='text'):
        """
        爬取所有类型的资讯（论文、模型、新闻）
        
        Args:
            format: 输出格式 (text/json)
        """
        logger.info("开始爬取所有资讯...")
        
        all_results = {
            "论文": self.spider.paper(),
            "模型": self.spider.hugging_face(),
            "新闻": self.spider.ai_bot() + self.spider.duckduckgo() + self.spider.google()
        }
        
        if format == 'json':
            import json
            output = {}
            for category, results in all_results.items():
                output[category] = [r.dict() for r in results]
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return output
        else:
            output = []
            for category, results in all_results.items():
                output.append(f"\n{'='*50}")
                output.append(f"{category} ({len(results)} 条)")
                output.append(f"{'='*50}")
                for i, r in enumerate(results, 1):
                    output.append(f"{i}. {r.title}")
                    output.append(f"   URL: {r.url}")
                    if r.text != r.title:
                        output.append(f"   简介: {r.text}")
            
            result_text = '\n'.join(output)
            print(result_text)
            return result_text
    
    def warm_words(self):
        """生成每日温暖寄语"""
        logger.info("生成每日寄语...")
        words = self.spider.generate_warm_words()
        logger.success(f"每日寄语: {words}")
        return words
    
    def _format_output(self, results, format, category):
        """格式化输出"""
        if format == 'json':
            import json
            output = [r.dict() for r in results]
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return output
        else:
            output = [
                f"\n{'='*50}",
                f"{category} ({len(results)} 条)",
                f"{'='*50}"
            ]
            for i, r in enumerate(results, 1):
                output.append(f"{i}. {r.title}")
                output.append(f"   URL: {r.url}")
                if r.text != r.title:
                    output.append(f"   简介: {r.text}")
            
            result_text = '\n'.join(output)
            print(result_text)
            return result_text


class WeChatCLI:
    """微信公众号文章发布命令行工具"""
    
    def __init__(self):
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


class WorkflowCLI:
    """完整工作流命令行工具"""
    
    def __init__(self):
        self.spider = Spider()
        self.publisher = None
    
    def daily(self, title="每日AI资讯精华", author="AI小助手", 
             publish_wechat=False, publish_wxwork=False):
        """
        每日资讯完整工作流：爬取资讯 -> AI生成文章 -> 发布到微信公众号或企业微信
        
        Args:
            title: 文章标题
            author: 作者
            publish_wechat: 是否发布到微信公众号
            publish_wxwork: 是否发布到企业微信
        """
        
        logger.info("="*60)
        logger.info("开始执行每日资讯工作流")
        logger.info("="*60)
        
        logger.info("爬取资讯...")
        content_data = self.spider.make_spider_content()
        
        if publish_wechat:
            self.publisher = WeChatArticlePublisher()
            content = content_data.create_wechat_article_content()
            self.publisher.publish(content=content, title=title, author=author)
        if publish_wxwork:
            self.publisher = WxworkArticlePublisher()
            content = content_data.create_wxwork_article_content()
            self.publisher.publish(content=content, title=title, author=author)
        else:
            raise ValueError(f"不支持的发布平台: {publish_wechat} 和 {publish_wxwork}")


    def schdule_daily(self, publish_wechat=False, publish_wxwork=False):
        """
        定时每日资讯完整工作流：爬取资讯 -> AI生成文章 -> 发布到微信公众号或企业微信
        """
        import schedule
        import time
        schedule.every().day.at("09:00").do(self.daily, publish_wechat=publish_wechat, publish_wxwork=publish_wxwork)
        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    """主入口函数"""
    fire.Fire(MainCLI)


if __name__ == '__main__':
    main()

