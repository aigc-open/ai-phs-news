#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI PHS News 使用示例
展示如何在 Python 代码中使用各个模块
"""

from ai_phs_news.spider import Spider
from ai_phs_news.wechat_article import WeChatArticlePublisher


def example_1_crawl_news():
    """示例1: 爬取资讯"""
    print("\n" + "="*60)
    print("示例1: 爬取资讯")
    print("="*60)
    
    spider = Spider()
    
    # 爬取论文
    print("\n爬取最新论文...")
    papers = spider.paper()
    print(f"找到 {len(papers)} 篇论文")
    for i, paper in enumerate(papers[:3], 1):
        print(f"{i}. {paper.title}")
        print(f"   简介: {paper.text}")
    
    # 爬取模型
    print("\n爬取最新模型...")
    models = spider.hugging_face()
    print(f"找到 {len(models)} 个模型")
    for i, model in enumerate(models[:3], 1):
        print(f"{i}. {model.title}")
    
    # 爬取新闻
    print("\n爬取 AI 新闻...")
    news = spider.ai_bot()
    print(f"找到 {len(news)} 条新闻")
    for i, item in enumerate(news[:3], 1):
        print(f"{i}. {item.title}")


def example_2_generate_warm_words():
    """示例2: 生成每日寄语"""
    print("\n" + "="*60)
    print("示例2: 生成每日寄语")
    print("="*60)
    
    spider = Spider()
    warm_words = spider.generate_warm_words()
    print(f"\n今日寄语: {warm_words}")


def example_3_create_draft_article():
    """示例3: 创建草稿文章"""
    print("\n" + "="*60)
    print("示例3: 创建草稿文章")
    print("="*60)
    
    publisher = WeChatArticlePublisher()
    
    # 准备文章内容
    content = """
    <section style="padding: 20px;">
        <h2 style="color: #3498db;">今日AI要闻</h2>
        <p style="line-height: 1.8;">
            这是一篇测试文章，展示如何使用 AI PHS News 发布内容到微信公众号。
        </p>
        <ul>
            <li>支持自动爬取资讯</li>
            <li>支持 AI 生成文章</li>
            <li>支持一键发布到微信</li>
        </ul>
    </section>
    """
    
    # 创建草稿
    # 注意: 这会实际调用微信 API，确保已正确配置
    # media_id = publisher.create_draft_article(
    #     title="测试文章",
    #     author="AI小助手",
    #     content=content
    # )
    # print(f"\n草稿创建成功！Media ID: {media_id}")
    
    print("\n注意: 此示例需要正确配置微信公众号才能运行")
    print("取消注释上面的代码以实际创建草稿")


def example_4_ai_generate_article():
    """示例4: 使用 AI 生成文章"""
    print("\n" + "="*60)
    print("示例4: 使用 AI 生成文章")
    print("="*60)
    
    publisher = WeChatArticlePublisher()
    
    # 准备原始内容（纯文本）
    raw_content = """
    每日AI资讯精华
    
    最新论文:
    1. VisCoP：面向视觉语言模型视频领域自适应的视觉探测技术
    2. 通过世界中的基础实现空间推理
    3. Bee：一个高质量语料库与全栈套件
    
    最新模型:
    1. Qwen/Qwen3-VL-8B-Thinking
    2. lightx2v/Wan2.2-I2V-A14B-Moe-Distill-Lightx2v
    
    最新资讯:
    1. 苹果M5芯片登场：10核CPU、10核GPU，AI性能飙到3.5倍
    2. 自进化AI原生手机！荣耀Magic8系列发布
    
    活在当下，珍惜眼前。--林清玄
    """
    
    # AI 会自动将纯文本转换为精美的 HTML 格式
    # 注意: 这会实际调用 AI API 和微信 API
    # media_id = publisher.generate_article(
    #     content=raw_content,
    #     title="每日AI资讯精华",
    #     author="AI小助手"
    # )
    # print(f"\n文章生成并发布成功！Media ID: {media_id}")
    
    print("\n注意: 此示例需要正确配置 OpenAI API 和微信公众号才能运行")
    print("取消注释上面的代码以实际生成文章")


def example_5_complete_workflow():
    """示例5: 完整工作流"""
    print("\n" + "="*60)
    print("示例5: 完整工作流 - 爬取 -> 生成 -> 发布")
    print("="*60)
    
    # 步骤1: 爬取资讯
    print("\n步骤 1/4: 爬取资讯...")
    spider = Spider()
    papers = spider.paper()[:3]
    models = spider.hugging_face()[:3]
    news = spider.ai_bot()[:5]
    
    print(f"- 论文: {len(papers)} 篇")
    print(f"- 模型: {len(models)} 个")
    print(f"- 新闻: {len(news)} 条")
    
    # 步骤2: 生成寄语
    print("\n步骤 2/4: 生成每日寄语...")
    warm_words = spider.generate_warm_words()
    print(f"寄语: {warm_words}")
    
    # 步骤3: 组织内容
    print("\n步骤 3/4: 组织内容...")
    content_parts = ["每日AI资讯精华\n"]
    
    for paper in papers:
        content_parts.append(f"最新论文: {paper.text}")
    
    for model in models:
        content_parts.append(f"最新模型: {model.title}")
    
    for item in news:
        content_parts.append(f"最新资讯: {item.title}")
    
    content_parts.append(f"\n{warm_words}")
    
    content = "\n".join(content_parts)
    print("内容组织完成")
    print("\n预览内容:")
    print("-" * 60)
    print(content[:300] + "...")
    print("-" * 60)
    
    # 步骤4: 发布文章
    print("\n步骤 4/4: 发布文章...")
    # publisher = WeChatArticlePublisher()
    # media_id = publisher.generate_article(
    #     content=content,
    #     title="每日AI资讯精华",
    #     author="AI小助手"
    # )
    # print(f"发布成功！Media ID: {media_id}")
    
    print("\n注意: 完整工作流需要正确配置所有 API 才能运行")
    print("取消注释上面的代码以实际执行发布")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("AI PHS News 使用示例")
    print("="*60)
    print("\n提示: 某些示例需要正确配置 API 才能完整运行")
    print("请参考 env.example 文件配置你的环境变量\n")
    
    # 运行各个示例
    example_1_crawl_news()
    example_2_generate_warm_words()
    example_3_create_draft_article()
    example_4_ai_generate_article()
    example_5_complete_workflow()
    
    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60)


if __name__ == '__main__':
    main()

