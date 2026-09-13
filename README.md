# WeChat Article Hunter

一套面向微信公众号的模块化 AI 内容生产 Skills。它将选题、事实研究、大纲、成文、审校、配图、排版与草稿箱交付拆成独立阶段，并由总编排 Skill 统一管理中间产物和质量门槛。

## 能力地图

| Skill | 作用 | 核心产物 |
|---|---|---|
| `wechat-article-hunter` | 全流程编排与断点续作 | `article-brief.json`、阶段状态 |
| `wechat-topic-hunter` | 热点发现、选题评分、标题方向 | `topic-cards.json` |
| `wechat-content-research` | 多源研究、证据账本、观点缺口 | `research-pack.md`、`source-ledger.json` |
| `wechat-article-outline` | 论点结构、叙事节奏、配图点位 | `outline.md` |
| `wechat-article-writer` | 按内容类型生成公众号初稿 | `draft.md` |
| `wechat-originality-gate` | 来源溯源、结构复刻与新增价值检查 | `originality-report.json` |
| `wechat-article-editor` | 事实、逻辑、文风与传播性审校 | `review-report.md`、`article.md` |
| `wechat-image-director` | 封面与正文配图策划/生成 | `image-plan.md`、`images/` |
| `wechat-layout` | 微信友好 HTML 与纯文本导出 | `article.html`、`article.txt` |
| `wechat-draft-publisher` | 草稿箱发布准备与受控提交 | `publish-receipt.json` |

## 设计原则

- **选题优先**：先判断受众价值、时效窗口和差异化，再投入长文生产。
- **证据驱动**：重要事实必须进入来源账本；事实、推断和观点明确分开。
- **中间产物可恢复**：每一步都有固定输入、输出和门禁，可单步重跑。
- **内容路由**：新闻、GitHub 项目、论文、产品评测、教程和观点文章采用不同研究与叙事结构。
- **发布受控**：默认只生成草稿或写入草稿箱；公开发布、群发和付费操作必须另行明确授权。
- **低耦合**：不绑定单一模型、搜索引擎、图片服务或内容平台客户端。
- **不以反爬或洗稿为能力**：不绕过访问控制，不通过同义改写规避原创检测；输入必须来自公开、授权或用户提供的材料。

## 安装

将整个仓库复制到支持 Skills 的环境，或只安装所需目录。以 Codex 为例：

```bash
git clone https://github.com/big86car/wechat-article-hunter.git
cp -R wechat-article-hunter/skills/* ~/.codex/skills/
```

建议安装全部 Skill，以便总编排器可以按阶段调用；单个 Skill 也可独立使用。

## 快速开始

```text
使用 $wechat-article-hunter，面向企业 AI 与数字化负责人，
从过去 7 天的全球信息源中提出 5 个公众号选题。
先输出选题卡让我选择，不要直接写正文。
```

选题确认后可继续：

```text
继续刚才选择的选题，完成研究、大纲、3000 字左右正文、配图方案和微信 HTML。
```

默认工作目录为 `wechat-articles/YYYY-MM-DD-<slug>/`。也可先初始化：

```bash
python skills/wechat-article-hunter/scripts/init_article.py \
  --title "AI Agent 的真正拐点" \
  --audience "企业 CIO 与数字化负责人" \
  --objective "建立专业认知并引发讨论"
```

## 典型产物

```text
wechat-articles/2026-09-13-agent-turning-point/
├── article-brief.json
├── topic-cards.json
├── research-pack.md
├── source-ledger.json
├── outline.md
├── draft.md
├── originality-report.json
├── review-report.md
├── article.md
├── image-plan.md
├── images/
├── article.html
├── article.txt
└── publish-receipt.json
```

## 本地工具

- `init_article.py`：初始化文章目录与 brief。
- `validate_topic_cards.py`：校验选题卡字段和评分范围。
- `validate_article.py`：检查标题、引用占位符、段落和基础质量信号。
- `validate_originality_report.py`：阻止没有新增价值或来源风险未解决的文章进入终审。
- `markdown_to_wechat_html.py`：将定稿 Markdown 转成内联样式 HTML。
- `publish_draft.py`：校验发布包；只有显式传入 `--commit` 才提交草稿箱。

排版脚本需要 `python -m pip install -r requirements.txt`。

## 安全与边界

任何 Skill 都不得把密码、Cookie、AppSecret、access token 或私有素材写入仓库。发布 Skill 仅在用户明确要求提交草稿、完成凭据检查并确认目标账号后执行；默认 dry-run，不公开发布、不群发。访问令牌缓存写入用户缓存目录而不是项目目录。

## License

MIT
