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
        
        self.sections.insert(0, ResultSection(title="大模型API", items=[Result(
            title="ph8大模型，国内外全模型，官网模型价格基础上3折，充值在享折上折(ph8.co)", 
            url="https://ph8.co", 
            text="ph8大模型，国内外全模型，官网模型价格基础上3折，充值在享折上折(ph8.co)")]))
        
        
        html = f"""
        <section style="padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; margin-bottom: 15px;">
            <h1 style="text-align: left; color: #ffffff; font-size: 24px; font-weight: bold; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                ✨ {self.title} ✨
            </h1>
        </section>
        """
        for section in self.sections:
            html += f"""
            <section style="margin: 15px 0; padding: 0; background: linear-gradient(to right, #ffffff 0%, #f8f9ff 100%); border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid #667eea;">
                <h2 style="color: #667eea; font-size: 18px; font-weight: bold; margin: 0 0 10px 0; padding: 0; border-bottom: 2px solid #e8ebff;">
                    📌 {section.title}
                </h2>
                <ul style="margin: 0; padding: 0; list-style-type: none;">
            """
            for item in section.items:
                html += f'''<li style="margin: 8px 0; padding: 0 -5px; color: #2c3e50; line-height: 1.8;">
                    <a href="{item.url}" target="_blank" style="color: #5a67d8; text-decoration: none; font-weight: 500; transition: all 0.3s ease; border-bottom: 2px solid transparent;">▸ {item.text}</a>
                </li>'''
            html += f"""
                </ul>
            </section>
            """
        html += f"""
        <section style="margin-top: 15px; padding: 0; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 8px; text-align: left; box-shadow: 0 2px 4px rgba(0,0,0,0.15);">
            <h1 style="color: #ffffff; font-size: 20px; font-weight: 600; margin: 0; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); line-height: 1.6;">
                💖 {self.warm_words} 💖
            </h1>
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