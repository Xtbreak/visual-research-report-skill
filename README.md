# Visual Research Report Skill

黑白灰配亮绿色的可视化方案调研报告 skill。连续向下阅读，主章节侧边导航，醒目章节序号，紧凑对比表和流程图；研究在前，技术选型与实施建议在后。

## 安装与使用

将本仓库复制到 `~/.codex/skills/visual-research-report`，或交给支持 SKILL.md 的工具加载。

示例提示词：

> 使用 $visual-research-report，把这些资料整理成方案调研报告。先比较候选方案，再给出技术选型，输出本地 HTML 和 Markdown。

也可直接生成示例：

```sh
python3 scripts/render_report.py assets/example.json --output output/example
```

打开 `output/example/report.html`。只需要 Python 3 标准库，无 npm、外部字体或 CDN 依赖。

## 包含内容

- `SKILL.md`：写作组织、视觉规格和生成流程。
- `assets/report.css`、`assets/report.js`：当前报告的样式与导航交互。
- `assets/example.json`：虚构主题示例和输入结构。
- `scripts/render_report.py`：生成自包含 HTML 与 Markdown。
- `agents/openai.yaml`：Codex 展示信息。

此包仅包含通用样式与虚构示例，不包含原始桌宠调研正文或私人对话。推荐方案和已验证结果需在实际报告中区分。
