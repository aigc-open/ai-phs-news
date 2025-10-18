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
        <section style="padding: 16px 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 16px; box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);">
            <h1 style="text-align: left; color: #ffffff; font-size: 22px; font-weight: bold; margin: 0; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); letter-spacing: 0.5px;">✨ {self.title}</h1>
        </section>
        """
        for section in self.sections:
            html += f"""
            <section style="margin: 16px 0; padding: 14px 0px; background: #ffffff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #667eea;">
                <h2 style="color: #667eea; font-size: 17px; font-weight: bold; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 1px solid #e8ebff;">
                    {section.title}
                </h2>
                <div>
            """
            for item in section.items:
                if "https://mp.weixin.qq.com" in item.url:
                    html += f'''<div style="margin: 0 0 14px 0; padding: 0; color: #2c3e50; line-height: 1.5;">
                        <div style="margin-bottom: 5px; line-height: 1.6;">
                            <a href="{item.url}" target="_blank" style="color: #5a67d8; text-decoration: none; font-weight: 500; font-size: 15px;">
                                👉 {item.text}
                            </a>
                        </div>
                    </div>'''
                else:
                    html += f'''<div style="margin: 0 0 14px 0; padding: 0; color: #2c3e50; line-height: 1.5;">
                        <div style="margin-bottom: 5px; line-height: 1.6;">
                            <span style="color: #5a67d8; text-decoration: none; font-weight: 500; font-size: 15px;">👉 {item.text}</span>
                        </div>
                        <div style="font-size: 11px; color: #aaa; word-break: break-all; line-height: 1.4; background: #f7f9fc; padding: 6px 8px; border-radius: 4px; margin-top: 4px;">{item.url}</div>
                    </div>'''
            html += f"""
                </div>
            </section>
            """
        html += f"""
        <section style="margin-top: 16px; padding: 16px 12px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 10px; text-align: left; box-shadow: 0 3px 10px rgba(240, 147, 251, 0.3);">
            <h1 style="color: #ffffff; font-size: 18px; font-weight: 600; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); line-height: 1.6;">
                {self.warm_words}
            </h1>
        </section>
        """
        # 移除HTML中的换行符和多余空格，避免产生&nbsp;
        html = ''.join(line.strip() for line in html.split('\n') if line.strip())
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