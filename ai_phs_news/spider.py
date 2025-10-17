from datetime import datetime
from duckduckgo_search import DDGS
from pydantic import BaseModel
from .config import global_config
from openai import OpenAI
import requests
from loguru import logger
from bs4 import BeautifulSoup
import json
from daily_basic_function import logger_execute_time
import serpapi
from .llm import LLMClient
import fire
from .data_format import Result, ResultContent, ResultSection

class Spider(LLMClient):

    def generate_warm_words(self, max_length=4096, temperature=1.4):
        messages = [{"role": "system", "content": "你是一个有用的助手"},
                    {
            "role": "user", "content": "给我写一个每日寄语，要求简短，但是要温暖人心，或者俏皮，引用名人名言， 这个寄语要非常简单,仅一句话表达即可，不要换行, 格式要求:   xxxx--名人"}]
        info = self.chat(messages=messages)
        return info

    @logger_execute_time(doc="论文 搜索")
    def paper(self):
        """https://hub.baai.ac.cn/papers?label=ai&model=newest"""
        url = "https://hub-api.baai.ac.cn/api/v3/paper/list"
        data = requests.post(
            url, json={"page": 1, "type": "newest", "area": "agent,nlp,multimodal"}).json().get("data", [])
        out = []
        for item in data:
            try:
                introduction = self.chat(
                    [{"role": "user", "content": f"{item['title']} \n 请你将上诉文本简要翻译成中文，仅一句话"}])
            except Exception as e:
                logger.warning(str(e))
                if len(item["introduction"]) > 40:
                    introduction = item["introduction"][:40] + "..."
                else:
                    introduction = item["introduction"]
            out.append(Result(title=item["title"],
                       url=item["source"], text=introduction))
        logger.success(f"爬取完成: 论文 {len(out)} 篇")
        return out

    @logger_execute_time(doc="Ai Bot 搜索")
    def ai_bot(self):
        """https://ai-bot.cn/"""
        url = "https://ai-bot.cn/daily-ai-news/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        news_items = soup.find_all('div', class_='news-item')
        out = []
        for item in news_items:
            title_tag = item.find('h2').find('a')
            title = title_tag.text
            href = title_tag['href']
            out.append(Result(title=title, text=title,
                       url=href))
        logger.success(f"爬取完成: 新闻 {len(out)} 条")
        return out

    @logger_execute_time(doc="Hugging Face 搜索")
    def hugging_face(self):
        url = "https://hf-mirror.com/models"
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', class_='overview-card-wrapper')
        out = []
        for article in articles:
            link = article.find('a')
            href = link['href'] if link else None
            title = link.find('header')['title'] if link and link.find(
                'header') else None
            out.append(Result(title=title, text=title,
                       url="https://huggingface.co"+href))
        logger.success(f"爬取完成: 模型 {len(out)} 个")
        return out

    @logger_execute_time(doc="Duckduckgo 搜索")
    def duckduckgo(self):
        try:
            results = DDGS().text("大模型新闻事件 绘图模型新闻事件 ai新闻事件 芯片新闻事件", max_results=10, timelimit="d")
        except Exception as e:
            logger.warning(f"{str(e)}")
            return []
        out = []
        for data in results:
            out.append(Result(title=data['title'],
                       text=data['title'], url=data['href']))
        logger.success(f"爬取完成: 新闻 {len(out)} 条")
        return out

    @logger_execute_time(doc="google 搜索")
    def google(self):
        try:
            client = serpapi.Client(api_key=global_config.SERPAPI_KEY)
            data = client.search(q="ai 芯片 大模型",
                        engine="google", hl="zh-cn", gl="cn", tbs="qdr:d,sbd:1", tbm="nws",num=100,filter=1)
            
        except Exception as e:
            logger.warning(f"{str(e)}")
            return []
        out = []
        news_results = data.get("news_results")
        for news_result in news_results:
            out.append(Result(title=news_result["title"],text=news_result["title"], url=news_result["link"]))
        logger.success(f"爬取完成: 新闻 {len(out)} 条")
        return out

    def make_spider_content(self) -> ResultContent:
        papers = self.paper()
        papers_slice = papers[:5] if papers else papers

        models = self.hugging_face()
        models_slice = models[:5] if models else models

        aibot = self.ai_bot()
        aibot_slice = aibot[:5] if aibot else aibot

        duck_news = self.duckduckgo()
        duck_slice = duck_news[:5] if duck_news else duck_news

        google_news = self.google()
        google_slice = google_news[:5] if google_news else google_news

        results = []
        
        
        if aibot_slice:
            results += aibot_slice
        if duck_slice:
            results += duck_slice
        if google_slice:
            results += google_slice
        if models_slice:
            results += models_slice
        if papers_slice:
            results += papers_slice

        # Section slices based on the actual available data
        sections = []

        

        model_items = [Result(title=result.title, url=result.url, text=result.text) for result in models_slice] if models_slice else []
        if model_items:
            sections.append(ResultSection(title="模型", items=model_items))

        # 新闻项，包括 aibot, duckduckgo, google 三个来源合并
        news_items = []
        if aibot_slice:
            news_items += [Result(title=result.title, url=result.url, text=result.text) for result in aibot_slice]
        if duck_slice:
            news_items += [Result(title=result.title, url=result.url, text=result.text) for result in duck_slice]
        if google_slice:
            news_items += [Result(title=result.title, url=result.url, text=result.text) for result in google_slice]
        if news_items:
            sections.append(ResultSection(title="新闻", items=news_items))
            
        paper_items = [Result(title=result.title, url=result.url, text=result.text) for result in papers_slice] if papers_slice else []
        if paper_items:
            sections.append(ResultSection(title="论文", items=paper_items))
            
        return ResultContent(
            title=f"每日AI资讯快报",
            warm_words=self.generate_warm_words(),
            sections=sections
        )


class CLI:
    """AI 资讯爬虫命令行工具
    
    使用示例:
        # 爬取论文
        python -m ai_phs_news.spider papers
        
        # 爬取模型
        python -m ai_phs_news.spider models
        
        # 爬取新闻
        python -m ai_phs_news.spider news
        
        # 爬取所有资讯
        python -m ai_phs_news.spider all
        
        # 生成每日寄语
        python -m ai_phs_news.spider warm-words
    """
    
    def __init__(self):
        """初始化爬虫"""
        self.spider = Spider()
    
    def papers(self, format='text'):
        """
        爬取最新论文
        
        Args:
            format: 输出格式 (text/json)，默认 text
        """
        logger.info("开始爬取最新论文...")
        results = self.spider.paper()
        return self._format_output(results, format, "最新论文")
    
    def models(self, format='text'):
        """
        爬取 Hugging Face 最新模型
        
        Args:
            format: 输出格式 (text/json)，默认 text
        """
        logger.info("开始爬取最新模型...")
        results = self.spider.hugging_face()
        return self._format_output(results, format, "最新模型")
    
    def news(self, source='all', format='text'):
        """
        爬取 AI 相关新闻
        
        Args:
            source: 新闻来源 (all/aibot/duckduckgo/google)，默认 all
            format: 输出格式 (text/json)，默认 text
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
            format: 输出格式 (text/json)，默认 text
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


if __name__ == '__main__':
    fire.Fire(CLI)

