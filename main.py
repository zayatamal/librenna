import pypandoc
from pathlib import Path

from jinja2 import Template

book_path = Path("book")
rendered_path = Path("rendered_book")
rendered_path.mkdir(exist_ok=True)

if not book_path.is_dir():
    print("book is not a directory")
    exit(1)

for chapter_path in book_path.glob("*.md"):
    with chapter_path.open() as f:
        template = Template(f.read())

    rendered = template.render(pagebreak='<div style="page-break-after:always;"></div>')
    new_chapter_path = rendered_path / chapter_path.name
    new_chapter_path.write_text(rendered)

with (book_path / "title.md").open() as f:
    for line in f.readlines():
        if line.startswith("title:"):
            title = line.strip().removeprefix("title: ")
print(f"{title}.epub")
pypandoc.convert_file(
    source_file="rendered_book/*.md",
    format="markdown",
    to="epub",
    outputfile=f"{title}.epub",
    extra_args=["--toc", "--toc-depth=5"],
)
