# AI PHS News - AI 资讯聚合与发布工具

![](./ai.png)

一个功能强大的 AI 资讯聚合工具，支持自动爬取最新的 AI 论文、模型和新闻，并通过 AI 生成精美的公众号文章。

## 🌟 主要功能

- **📰 资讯爬取**: 自动爬取多个来源的 AI 资讯
  - 最新论文（来自 BAAI Hub）
  - 最新模型（来自 Hugging Face）
  - AI 新闻（来自 AI Bot、DuckDuckGo、Google）
  
- **✍️ AI 文章生成**: 使用 LLM 自动生成精美的公众号文章
  - 智能排版，符合微信公众号风格
  - 自动添加 HTML 样式
  - 支持自定义标题、作者等信息

- **📱 多平台发布**: 一键发布到多个平台
  - **微信公众号**: 支持草稿模式（推荐）、封面图片上传、评论设置
  - **企业微信**: 支持群机器人推送（Markdown 格式）

- **🤖 完整工作流**: 端到端自动化
  - 每日资讯自动汇总
  - 自定义资讯来源
  - 支持多平台同时发布
  - 一键完成爬取、生成、发布

## 📦 安装

### 克隆仓库
```bash
git clone https://github.com/your-repo/ai-phs-news.git
cd ai-phs-news
```

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件，配置以下环境变量：

```bash
# OpenAI API 配置（用于文章生成）
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini

# 聊天类型 (openai 或 duckduckgo)
CHAT_TYPE=openai

# 微信公众号配置
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret

# 默认封面图片 media_id（可选）
WECHAT_MEDIA_ID=your_media_id

# SerpAPI 配置（用于 Google 搜索，可选）
SERPAPI_KEY=your_serpapi_key

# 企业微信机器人 Keys（可选，支持多个，用逗号分隔）
WEIXIN_ROBOT_KEYS=key1,key2,key3
```

## 🚀 快速开始

### 第一步: 配置环境

```bash
# 复制配置文件模板
cp env.example .env

# 编辑 .env 文件，填入你的配置
# 至少需要配置:
# - CHAT_TYPE (可以先使用 duckduckgo，无需 API Key)
# - WECHAT_APP_ID 和 WECHAT_APP_SECRET (如果需要发布到微信公众号)
# - WEIXIN_ROBOT_KEYS (如果需要发布到企业微信群)
```

### 第二步: 运行示例

```bash
# 运行 Python API 示例（推荐新手）
python examples.py

# 或者直接使用命令行工具
python -m ai_phs_news spider all
```

### 方式1: 命令行工具（推荐）

```bash
# 查看帮助
python -m ai_phs_news --help

# 爬取资讯
python -m ai_phs_news spider papers
python -m ai_phs_news spider models
python -m ai_phs_news spider news
python -m ai_phs_news spider all

# 发布文章
python -m ai_phs_news wechat draft --title "标题" --author "作者" --content "<p>内容</p>"

# 完整工作流（一键完成）
# 发布到微信公众号
python -m ai_phs_news workflow daily --publish_wechat True

# 发布到企业微信
python -m ai_phs_news workflow daily --publish_wxwork True
```

### 方式2: 直接运行模块

```bash
# 爬虫模块
python -m ai_phs_news.spider papers
python -m ai_phs_news.spider models
python -m ai_phs_news.spider news

# 微信发布模块
python -m ai_phs_news.wechat_article draft --title "标题" --author "作者" --content "<p>内容</p>"
```

### 方式3: Python API

查看 `examples.py` 文件获取详细的 Python API 使用示例。

```python
from ai_phs_news.spider import Spider
from ai_phs_news.wechat_article import WeChatArticlePublisher

# 创建爬虫并爬取资讯
spider = Spider()
papers = spider.paper()
news = spider.ai_bot()

# 发布文章
publisher = WeChatArticlePublisher()
media_id = publisher.create_draft_article(
    title="每日AI资讯",
    author="AI小助手",
    content="<p>文章内容</p>"
)
```

## 📖 详细用法

> 💡 **快速参考**: 查看 [COMMANDS.md](COMMANDS.md) 获取所有命令的快速参考指南和常用组合

### 1. 资讯爬取模块 (spider)

#### 爬取最新论文
```bash
# 文本格式输出
python -m ai_phs_news spider papers

# JSON 格式输出
python -m ai_phs_news spider papers --format json
```

#### 爬取最新模型
```bash
python -m ai_phs_news spider models
```

#### 爬取 AI 新闻
```bash
# 爬取所有来源的新闻
python -m ai_phs_news spider news

# 指定来源
python -m ai_phs_news spider news --source aibot
python -m ai_phs_news spider news --source duckduckgo
python -m ai_phs_news spider news --source google
```

#### 爬取所有资讯
```bash
python -m ai_phs_news spider all
```

#### 生成每日寄语
```bash
python -m ai_phs_news spider warm-words
```

### 2. 微信发布模块 (wechat)

#### 创建草稿文章（推荐）
```bash
# 基本用法
python -m ai_phs_news wechat draft \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --content "<p>这是文章内容</p>"

# 使用本地封面图片
python -m ai_phs_news wechat draft \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --content "<p>这是文章内容</p>" \
  --thumb_image "./cover.jpg"

# 使用已有的 media_id 作为封面
python -m ai_phs_news wechat draft \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --content "<p>这是文章内容</p>" \
  --thumb_image "MvcyvW-8y3M9zOIu1qlEL..."

# 完整参数
python -m ai_phs_news wechat draft \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --content "<p>这是文章内容</p>" \
  --thumb_image "./cover.jpg" \
  --digest "今日最新AI领域资讯汇总" \
  --content_source_url "https://example.com" \
  --show_cover_pic 1 \
  --need_open_comment 1 \
  --only_fans_can_comment 0
```

#### 使用 AI 生成文章（自动转换为 HTML）
```bash
# AI 会自动将纯文本转换为精美的 HTML 格式
python -m ai_phs_news wechat generate \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --content "最新论文: xxx\n最新模型: yyy\n最新资讯: zzz" \
  --thumb_image "./cover.jpg"
```

#### 上传图片
```bash
# 上传为永久素材（封面图片）
python -m ai_phs_news wechat upload --image_path "./cover.jpg"

# 上传为临时素材
python -m ai_phs_news wechat upload --image_path "./cover.jpg" --permanent False
```

### 3. 完整工作流 (workflow)

#### 每日资讯工作流（推荐）

**功能说明**: 
- 自动爬取论文、模型、新闻资讯
- 每条资讯都包含标题和原始 URL 链接
- 使用 AI 自动生成精美的格式化文章
- 自动添加每日寄语
- 支持发布到微信公众号或企业微信

```bash
# 发布到微信公众号
python -m ai_phs_news workflow daily \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --publish_wechat True

# 发布到企业微信群
python -m ai_phs_news workflow daily \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --publish_wxwork True

# 同时发布到两个平台
python -m ai_phs_news workflow daily \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --publish_wechat True \
  --publish_wxwork True

# 定时任务（每天09:00自动执行）
python -m ai_phs_news workflow schdule_daily --publish_wxwork True
```


## 📋 命令参数说明

### Spider 参数

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `format` | 输出格式 | `text` | `text`, `json` |
| `source` | 新闻来源 | `all` | `all`, `aibot`, `duckduckgo`, `google` |

### WeChat 参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `title` | 文章标题 | - | `"每日AI资讯精华"` |
| `author` | 作者 | - | `"AI小助手"` |
| `content` | 文章内容 | - | `"<p>内容</p>"` |
| `thumb_image` | 封面图片 | `None` | `"./cover.jpg"` 或 `"media_id"` |
| `digest` | 摘要 | `""` | `"今日资讯汇总"` |
| `content_source_url` | 原文链接 | `""` | `"https://example.com"` |
| `show_cover_pic` | 显示封面 | `1` | `0`, `1` |
| `need_open_comment` | 开启评论 | `0` | `0`, `1` |
| `only_fans_can_comment` | 仅粉丝评论 | `0` | `0`, `1` |

### Workflow 参数

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `title` | 文章标题 | `"每日AI资讯精华"` | 任意字符串 |
| `author` | 作者 | `"AI小助手"` | 任意字符串 |
| `publish_wechat` | 是否发布到微信公众号 | `False` | `True`, `False` |
| `publish_wxwork` | 是否发布到企业微信 | `False` | `True`, `False` |

## 🎯 使用场景

### 场景1: 每日定时发布 AI 资讯

**方式1: 使用内置定时任务**
```bash
# 每天早上 09:00 自动发布到企业微信
python -m ai_phs_news workflow schdule_daily --publish_wxwork True

# 每天早上 09:00 自动发布到微信公众号
python -m ai_phs_news workflow schdule_daily --publish_wechat True
```

**方式2: 使用 crontab 或其他定时任务工具**
```bash
# 每天早上 8 点发布到企业微信
0 8 * * * cd /path/to/ai-phs-news && python -m ai_phs_news workflow daily --publish_wxwork True

# 每天早上 8 点发布到微信公众号
0 8 * * * cd /path/to/ai-phs-news && python -m ai_phs_news workflow daily --publish_wechat True --title "每日AI早报"
```

**提示**: 如果在配置文件中设置了 `WECHAT_MEDIA_ID`，将自动使用该封面图片。

### 场景2: 手动精选资讯发布

```bash
# 1. 先爬取资讯查看
python -m ai_phs_news spider all

# 2. 手动编写内容
# 3. 发布到微信
python -m ai_phs_news wechat draft \
  --title "本周AI精选" \
  --author "技术编辑" \
  --content "<p>手动编写的精选内容</p>" \
  --thumb_image "./cover.jpg"
```

### 场景3: 企业微信群推送

```bash
# 快速推送到企业微信群（适合团队协作）
python -m ai_phs_news workflow daily --publish_wxwork True

# 配置多个企业微信机器人 Key，支持推送到多个群
# 在 .env 中配置: WEIXIN_ROBOT_KEYS=key1,key2,key3
```

## 🛠️ Python API 使用

除了命令行，也可以在 Python 代码中使用：

```python
from ai_phs_news.spider import Spider
from ai_phs_news.wechat_article import WeChatArticlePublisher
from ai_phs_news.wxwork_article import WxworkArticlePublisher

# 创建爬虫实例
spider = Spider()

# 爬取资讯并生成内容
content_data = spider.make_spider_content()

# 方式1: 发布到微信公众号
wechat_publisher = WeChatArticlePublisher()
wechat_content = content_data.create_wechat_article_content()
wechat_publisher.publish(
    content=wechat_content,
    title="每日AI资讯",
    author="AI小助手"
)

# 方式2: 发布到企业微信
wxwork_publisher = WxworkArticlePublisher()
wxwork_content = content_data.create_wxwork_article_content()
wxwork_publisher.publish(
    content=wxwork_content,
    title="每日AI资讯",
    author="AI小助手"
)

print("发布成功！")
```

## 📁 项目结构

```
ai-phs-news/
├── ai_phs_news/           # 主要代码目录
│   ├── __init__.py        # 包初始化
│   ├── __main__.py        # 命令行入口
│   ├── cli.py             # 主命令行工具（整合所有功能）
│   ├── config.py          # 配置管理
│   ├── data_format.py     # 数据格式与内容生成
│   ├── llm.py             # LLM 客户端（支持 OpenAI 和 DuckDuckGo）
│   ├── spider.py          # 资讯爬虫（论文、模型、新闻）
│   ├── wechat_article.py  # 微信公众号文章发布
│   └── wxwork_article.py  # 企业微信文章发布
├── examples.py            # Python API 使用示例
├── env.example            # 配置文件模板
├── requirements.txt       # 项目依赖
├── README.MD              # 项目文档（本文件）
├── COMMANDS.md            # 命令行快速参考
└── LICENSE                # 许可证
```

## 💡 核心模块说明

### 1. cli.py - 主命令行工具
整合了所有功能模块，提供统一的命令行接口：
- `spider` - 资讯爬取
- `wechat` - 微信公众号发布
- `workflow` - 完整工作流（支持多平台发布）

### 2. spider.py - 资讯爬虫
支持爬取多个来源的 AI 资讯：
- **论文**: BAAI Hub 最新学术论文
- **模型**: Hugging Face 最新开源模型
- **新闻**: AI Bot、DuckDuckGo、Google 等多个新闻源
- **寄语**: 自动生成每日温暖寄语

### 3. data_format.py - 数据格式化
提供内容格式化和转换功能：
- 结构化数据模型（Result, ResultSection, ResultContent）
- 微信公众号 HTML 格式生成
- 企业微信 Markdown 格式生成
- 发布器基类定义

### 4. wechat_article.py - 微信公众号发布
提供微信公众号文章发布功能：
- 创建草稿文章（推荐）
- 上传封面图片
- AI 自动生成 HTML 格式文章

### 5. wxwork_article.py - 企业微信发布
提供企业微信群机器人推送功能：
- 支持 Markdown 格式内容
- 支持多机器人推送（多群同时发送）
- 自动处理消息长度限制

### 6. llm.py - LLM 客户端
支持多种 AI 接口：
- OpenAI API（需要 API Key）
- DuckDuckGo AI Chat（免费，无需 API Key）

## ❓ 常见问题

### Q1: 如何不使用 OpenAI API？
**A:** 将 `CHAT_TYPE` 设置为 `duckduckgo`，可以使用免费的 DuckDuckGo AI 聊天服务。

### Q2: 没有微信公众号可以使用吗？
**A:** 可以！你可以：
- 只使用爬虫功能爬取资讯
- 使用企业微信机器人推送（无需公众号）
- 使用 Python API 自定义处理内容

### Q3: 如何定时自动发布？
**A:** 有两种方式：
- **内置定时任务**: `python -m ai_phs_news workflow schdule_daily --publish_wxwork True`
- **crontab**: `0 8 * * * cd /path/to/ai-phs-news && python -m ai_phs_news workflow daily --publish_wxwork True`

### Q4: 爬取失败怎么办？
**A:** 
- 检查网络连接
- 某些网站可能需要代理
- DuckDuckGo 和 Google 搜索可能有频率限制

### Q5: 如何配置企业微信机器人？
**A:** 
1. 在企业微信群中添加群机器人，获取 Webhook Key
2. 在 `.env` 文件中配置 `WEIXIN_ROBOT_KEYS=your_key_here`
3. 支持配置多个 Key（用逗号分隔），实现多群推送

### Q6: 如何自定义文章格式？
**A:** 可以修改以下文件：
- `data_format.py`: 调整 HTML/Markdown 模板样式
- `wechat_article.py`: 修改 AI 生成 prompt（如果使用 AI 生成功能）

### Q7: 如何保存爬取的结果？
**A:** 使用 JSON 格式输出并重定向到文件：
```bash
python -m ai_phs_news spider all --format json > results.json
```

## 📝 注意事项

1. **API 配置**: 确保正确配置了 `.env` 文件中的 API 密钥
2. **微信公众号**: 需要认证的公众号才能使用草稿接口
3. **企业微信**: 
   - 需要在群中添加机器人获取 Webhook Key
   - 支持多个 Key 配置，实现多群推送
   - 消息长度限制为 3400 字节（自动处理）
4. **封面图片**（仅微信公众号）: 
   - 支持本地图片路径（自动上传）
   - 支持已有的 media_id
   - 图片格式支持：jpg, jpeg, png, gif, bmp
5. **内容格式**: 
   - 微信公众号：HTML 格式
   - 企业微信：Markdown 格式
   - 自动根据平台生成对应格式
6. **频率限制**: 注意 API 调用频率限制
7. **数据去重**: 项目使用 TinyDB 进行简单的 URL 去重，避免重复爬取

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🔗 相关链接

- [BAAI Hub](https://hub.baai.ac.cn/)
- [Hugging Face](https://huggingface.co/)
- [微信公众平台](https://mp.weixin.qq.com/)
- [企业微信群机器人](https://developer.work.weixin.qq.com/document/path/91770)
- [wechatpy 文档](https://wechatpy.readthedocs.io/)

## 📮 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。

---

**祝你使用愉快！🎉**

