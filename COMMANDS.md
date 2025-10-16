# AI PHS News 命令行快速参考

## 📚 目录
- [基本命令](#基本命令)
- [爬虫命令](#爬虫命令)
- [微信发布命令](#微信发布命令)
- [工作流命令](#工作流命令)
- [常用组合](#常用组合)

---

## 基本命令

### 查看帮助
```bash
# 主帮助
python -m ai_phs_news --help

# 模块帮助
python -m ai_phs_news spider --help
python -m ai_phs_news wechat --help
python -m ai_phs_news workflow --help

# 命令帮助
python -m ai_phs_news spider papers --help
python -m ai_phs_news wechat draft --help
```

---

## 爬虫命令

### 爬取论文
```bash
# 基本用法（文本输出）
python -m ai_phs_news spider papers

# JSON 格式输出
python -m ai_phs_news spider papers --format json

# 保存到文件
python -m ai_phs_news spider papers --format json > papers.json
```

### 爬取模型
```bash
# 爬取 Hugging Face 最新模型
python -m ai_phs_news spider models

# JSON 格式
python -m ai_phs_news spider models --format json
```

### 爬取新闻
```bash
# 爬取所有来源
python -m ai_phs_news spider news

# 指定来源
python -m ai_phs_news spider news --source aibot
python -m ai_phs_news spider news --source duckduckgo
python -m ai_phs_news spider news --source google

# JSON 格式
python -m ai_phs_news spider news --format json
```

### 爬取所有资讯
```bash
# 一次爬取所有类型（论文、模型、新闻）
python -m ai_phs_news spider all

# JSON 格式保存
python -m ai_phs_news spider all --format json > all_news.json
```

### 生成每日寄语
```bash
python -m ai_phs_news spider warm-words
```

---

## 微信发布命令

### 创建草稿文章
```bash
# 最简单的用法
python -m ai_phs_news wechat draft \
  --title "标题" \
  --author "作者" \
  --content "<p>HTML内容</p>"

# 使用本地封面图片
python -m ai_phs_news wechat draft \
  --title "每日AI资讯" \
  --author "AI小助手" \
  --content "<p>内容</p>" \
  --thumb_image "./cover.jpg"

# 使用已有 media_id
python -m ai_phs_news wechat draft \
  --title "每日AI资讯" \
  --author "AI小助手" \
  --content "<p>内容</p>" \
  --thumb_image "MvcyvW-8y3M9zOIu1qlEL..."

# 完整参数
python -m ai_phs_news wechat draft \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --content "<p>文章内容</p>" \
  --thumb_image "./cover.jpg" \
  --digest "今日最新AI领域资讯汇总" \
  --content_source_url "https://example.com" \
  --show_cover_pic 1 \
  --need_open_comment 1 \
  --only_fans_can_comment 0
```

### AI 生成文章
```bash
# AI 自动将纯文本转换为 HTML
python -m ai_phs_news wechat generate \
  --title "每日AI资讯" \
  --author "AI小助手" \
  --content "最新论文: xxx\n最新模型: yyy\n最新资讯: zzz"

# 带封面
python -m ai_phs_news wechat generate \
  --title "每日AI资讯" \
  --author "AI小助手" \
  --content "原始内容..." \
  --thumb_image "./cover.jpg"
```

### 上传图片
```bash
# 上传为永久素材（用作封面）
python -m ai_phs_news wechat upload --image_path "./cover.jpg"

# 上传为临时素材
python -m ai_phs_news wechat upload --image_path "./cover.jpg" --permanent False
```

---

## 工作流命令

### 每日资讯工作流（推荐）
```bash
# 默认配置（爬取 -> 生成 -> 发布）
python -m ai_phs_news workflow daily

# 自定义标题和作者
python -m ai_phs_news workflow daily \
  --title "今日AI速递" \
  --author "技术小编"

# 使用封面图片
python -m ai_phs_news workflow daily \
  --title "今日AI速递" \
  --author "技术小编" \
  --thumb_image "./cover.jpg"

# 仅生成内容，不发布（预览）
python -m ai_phs_news workflow daily --publish False
```

### 自定义工作流
```bash
# 只爬取论文和模型
python -m ai_phs_news workflow custom \
  --sources "papers,models" \
  --title "今日学术前沿" \
  --max_items 10

# 只爬取新闻
python -m ai_phs_news workflow custom \
  --sources "news" \
  --title "AI行业动态" \
  --max_items 15

# 完整配置
python -m ai_phs_news workflow custom \
  --sources "papers,models,news" \
  --title "AI全方位资讯" \
  --author "资讯小助手" \
  --thumb_image "./cover.jpg" \
  --max_items 20
```

---

## 常用组合

### 场景1: 每日定时发布
```bash
# 添加到 crontab
# 每天早上 8:00 自动发布
0 8 * * * cd /path/to/ai-phs-news && python -m ai_phs_news workflow daily --title "AI早报" --thumb_image "./covers/morning.jpg"

# 每天晚上 20:00 自动发布
0 20 * * * cd /path/to/ai-phs-news && python -m ai_phs_news workflow daily --title "AI晚报" --thumb_image "./covers/evening.jpg"
```

### 场景2: 先预览再发布
```bash
# 1. 先预览内容
python -m ai_phs_news workflow daily --publish False

# 2. 确认无误后发布
python -m ai_phs_news workflow daily
```

### 场景3: 爬取保存备用
```bash
# 1. 爬取所有资讯并保存
python -m ai_phs_news spider all --format json > data.json

# 2. 后续根据需要手动编写发布
python -m ai_phs_news wechat draft \
  --title "精选内容" \
  --author "编辑" \
  --content "$(cat content.html)"
```

### 场景4: 分类发布
```bash
# 周一: 学术论文专题
python -m ai_phs_news workflow custom \
  --sources "papers" \
  --title "本周学术前沿" \
  --max_items 10

# 周三: 开源模型专题
python -m ai_phs_news workflow custom \
  --sources "models" \
  --title "本周开源精选" \
  --max_items 10

# 周五: 行业新闻专题
python -m ai_phs_news workflow custom \
  --sources "news" \
  --title "本周行业动态" \
  --max_items 15
```

### 场景5: 批量上传封面
```bash
# 上传多个封面图片
for img in covers/*.jpg; do
    echo "上传: $img"
    python -m ai_phs_news wechat upload --image_path "$img"
done
```

---

## 参数说明

### Spider 参数
| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `format` | 输出格式 | `text` | `text`, `json` |
| `source` | 新闻来源 | `all` | `all`, `aibot`, `duckduckgo`, `google` |

### WeChat 参数
| 参数 | 说明 | 类型 | 必需 |
|------|------|------|------|
| `title` | 文章标题 | string | ✓ |
| `author` | 作者 | string | ✓ |
| `content` | 文章内容 | string | ✓ |
| `thumb_image` | 封面图片 | string | ✗ |
| `digest` | 摘要 | string | ✗ |
| `content_source_url` | 原文链接 | string | ✗ |
| `show_cover_pic` | 显示封面 | 0/1 | ✗ |
| `need_open_comment` | 开启评论 | 0/1 | ✗ |
| `only_fans_can_comment` | 仅粉丝评论 | 0/1 | ✗ |

### Workflow 参数
| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `title` | 文章标题 | "每日AI资讯精华" | 任意字符串 |
| `author` | 作者 | "AI小助手" | 任意字符串 |
| `thumb_image` | 封面图片 | None | "./cover.jpg" |
| `publish` | 是否发布 | True | True/False |
| `sources` | 资讯来源 | "all" | "papers,models,news" |
| `max_items` | 每类最大数量 | 20 | 任意正整数 |

---

## 技巧与提示

### 1. 使用别名简化命令
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
alias ai-news="python -m ai_phs_news"
alias ai-spider="python -m ai_phs_news spider"
alias ai-wechat="python -m ai_phs_news wechat"
alias ai-daily="python -m ai_phs_news workflow daily"

# 使用别名
ai-spider papers
ai-daily
```

### 2. 使用配置文件
将常用参数保存到脚本中：
```bash
#!/bin/bash
# daily_publish.sh

python -m ai_phs_news workflow daily \
  --title "每日AI资讯精华" \
  --author "AI小助手" \
  --thumb_image "./covers/daily.jpg"

# 运行
chmod +x daily_publish.sh
./daily_publish.sh
```

### 3. 日志记录
```bash
# 记录输出日志
python -m ai_phs_news workflow daily 2>&1 | tee logs/$(date +%Y%m%d).log
```

### 4. 错误处理
```bash
# 使用 || 处理失败情况
python -m ai_phs_news workflow daily || echo "发布失败，请检查日志"
```

### 5. 测试配置
```bash
# 先测试爬取
python -m ai_phs_news spider papers

# 再测试预览
python -m ai_phs_news workflow daily --publish False

# 最后正式发布
python -m ai_phs_news workflow daily
```

---

## 环境变量

可以通过环境变量覆盖配置：
```bash
# 临时设置
CHAT_TYPE=duckduckgo python -m ai_phs_news workflow daily

# 批量设置
export OPENAI_API_KEY=your_key
export CHAT_TYPE=openai
python -m ai_phs_news workflow daily
```

---

**提示**: 更多详细信息请查看 [README.MD](README.MD)

