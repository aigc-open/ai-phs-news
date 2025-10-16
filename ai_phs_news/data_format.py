from pydantic import BaseModel


class Result(BaseModel):
    title: str
    url: str
    text: str
    
class ResultSection(BaseModel):
    title: str
    items: list[Result]
    
class ResultContent(BaseModel):
    title: str
    warm_words: str
    sections: list[ResultSection]
    
    
    def create_wechat_article_content(self):
        """
        创建微信公众号文章内容
        """
        html = f"""
        <section>
            <h1 style="text-align: center; color: #2c3e50; font-size: 24px; margin-bottom: 20px;">
                {self.title}
            </h1>
        """
        for section in self.sections:
            html += f"""
            <section style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #3498db;">
                <h2 style="color: #3498db; font-size: 18px; margin-bottom: 10px;">
                    {section.title}
                </h2>
                <ul style="margin: 10px 0; padding-left: 20px;">
            """
            for item in section.items:
                html += f'<li style="margin: 8px 0; color: #2c3e50; line-height: 1.6;"><a href="{item.url}" target="_blank">{item.title}</a></li>'
            html += f"""
            </ul>
            </section>
            """
        html += f"""
        <section>
            <h1 style="text-align: center; color: #2c3e50; font-size: 24px; margin-bottom: 20px;">{self.warm_words}</h1>
        </section>
        """
        return html

    @staticmethod
    def format_weixin(type_, url, title="查看详情"):
        return f"""
> {type_}: <font color="comment"> [{title}]({url}) </font>
"""

    def create_wxwork_article_content(self):
        """
        创建企业微信文章内容(markdown格式)
        """
        data = ""
        # 按 sections 分组组织
        for section in self.sections:
            # section.title 作为 type_
            type_ = section.title
            for item in section.items:
                msg = self.format_weixin(type_=type_, url=item.url, title=item.text)
                # 单条消息不能超过3400字节
                if len((data+msg).encode("utf-8")) > 3400:
                    break
                data += msg
        return data

class PlatformArticlePublisher:
    
    def publish(self, content: str, title: str = "每日AI资讯精华", author: str = "AI小助手"):
        """
        发布文章
        """
        raise NotImplementedError("Subclasses must implement this method")