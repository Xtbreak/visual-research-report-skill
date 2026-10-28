import argparse
import html
import json
from pathlib import Path


def escape(value):
    return html.escape(str(value)).replace("\n", "<br>")


def badge(value):
    text = str(value)
    for level in ("P0", "P1", "P2"):
        if text == level or text.startswith(level + " ") or text.startswith(level + " ·"):
            return f'<span class="badge {level.lower()}">{level}</span>' + escape(text[2:])
    return escape(text)


def render(data, output):
    assets = Path(__file__).resolve().parent.parent / "assets"
    css = (assets / "report.css").read_text()
    js = (assets / "report.js").read_text()
    title = data["title"]
    nav, chapters = [], []
    markdown = [f"# {title}\n", data.get("meta", ""), data.get("abstract", "")]
    for index, chapter in enumerate(data["chapters"], 1):
        anchor = f"chapter-{index}"
        current = ' aria-current="page"' if index == 1 else ''
        nav.append(f'<a href="#{anchor}"{current}><span>{index:02}</span>{escape(chapter["title"])}</a>')
        parts = [f'<section class="report-chapter" id="{anchor}"><header class="chapter-heading"><span class="chapter-number">{index:02}</span><div><h2>{escape(chapter["title"])}</h2><p>{escape(chapter.get("intro", ""))}</p></div></header>']
        markdown.extend([f'\n## {chapter["title"]}\n', chapter.get("intro", "")])
        for block_index, block in enumerate(chapter["blocks"], 1):
            parts.append(f'<section class="report-block" id="{anchor}-{block_index}"><h3>{escape(block["title"])}</h3>')
            markdown.append(f'\n### {block["title"]}\n')
            if block.get("intro"):
                parts.append(f'<p class="block-intro">{escape(block["intro"])}</p>')
                markdown.append(block["intro"])
            for paragraph in block.get("paragraphs", []):
                parts.append(f'<p>{escape(paragraph)}</p>')
                markdown.append(paragraph)
            if block.get("flow"):
                nodes = [f'<div>{escape(node)}</div>' for node in block["flow"]]
                parts.append('<div class="flow" aria-label="流程">' + '<span class="arrow" aria-hidden="true">→</span>'.join(nodes) + '</div>')
                markdown.append(' → '.join(block["flow"]))
            if block.get("findings"):
                parts.append('<dl class="findings">')
                for label, content in block["findings"]:
                    parts.append(f'<div><dt>{badge(label)}</dt><dd>{escape(content)}</dd></div>')
                    markdown.append(f'**{label}**：{content}\n')
                parts.append('</dl>')
            if block.get("table"):
                columns = block["table"]["columns"]
                rows = block["table"]["rows"]
                parts.append('<div class="table-wrap" tabindex="0" aria-label="可横向滚动的对照表"><table><thead><tr>' + ''.join(f'<th scope="col">{escape(column)}</th>' for column in columns) + '</tr></thead><tbody>')
                def cell(value):
                    return str(value).replace('|', '\|').replace('\n', '<br>')
                markdown.append('| ' + ' | '.join(cell(column) for column in columns) + ' |\n| ' + ' | '.join('---' for column in columns) + ' |')
                for row in rows:
                    if len(row) != len(columns):
                        raise ValueError(f'Table row width does not match columns: {block["title"]}')
                    parts.append('<tr>' + ''.join(f'<td>{badge(value)}</td>' for value in row) + '</tr>')
                    markdown.append('| ' + ' | '.join(cell(value) for value in row) + ' |')
                parts.append('</tbody></table></div>')
            if block.get("note"):
                parts.append(f'<p class="note">{escape(block["note"])}</p>')
                markdown.append('\n' + block["note"])
            parts.append('</section>')
        parts.append('</section>')
        chapters.append(''.join(parts))
    header = f'<header class="report-header"><div class="eyebrow">{escape(data.get("kind", "方案调研报告"))}</div><h1>{escape(title)}</h1><div class="meta">{escape(data.get("meta", ""))}</div><p class="abstract">{escape(data.get("abstract", ""))}</p>'
    if data.get("overview"):
        header += '<div class="overview">' + ''.join(f'<div><strong>{escape(label)}</strong><span>{escape(content)}</span></div>' for label, content in data["overview"]) + '</div>'
    if data.get("legend"):
        header += '<div class="legend">' + escape(data["legend"]) + '</div>'
        markdown.append('\n' + data["legend"])
    header += '</header>'
    footer = escape(data.get("footer", ""))
    page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + escape(title) + '</title><style>' + css + '</style></head><body><aside><div class="brand">' + escape(data.get("nav_title", title)) + '</div><div class="brand-sub">' + escape(data.get("meta", "")) + '</div><nav aria-label="章节导航">' + ''.join(nav) + '</nav><div class="nav-foot"><a href="report.md" download>Markdown</a><a href="#" id="print">打印 / PDF</a></div></aside><main><article class="document">' + header + ''.join(chapters) + '<footer class="report-footer">' + footer + '</footer></article></main><script>' + js + '</script></body></html>'
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.html").write_text(page, encoding="utf-8")
    (output / "report.md").write_text('\n'.join(markdown) + '\n', encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a visual research report from JSON.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render(json.loads(args.input.read_text(encoding="utf-8")), args.output)
