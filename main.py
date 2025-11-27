from pathlib import Path

import pypandoc
from jinja2 import Environment, FileSystemLoader

book_path = Path("book")
rendered_path = Path("rendered_book")
rendered_path.mkdir(exist_ok=True)

if not book_path.is_dir():
    print("book is not a directory")
    exit(1)  # Non-zero return is error

env = Environment(loader=FileSystemLoader(book_path))

for chapter_path in book_path.glob("*.md"):
    template = env.get_template(chapter_path.name)

    rendered = template.render(
        pagebreak='<div style="page-break-after:always;"></div>',
    )
    new_chapter_path = rendered_path / chapter_path.name
    new_chapter_path.write_text(rendered)

with (book_path / "title.md").open() as f:
    for line in f.readlines():
        if line.startswith("title:"):
            title = line.strip().removeprefix("title: ")

pypandoc.convert_file(
    source_file="rendered_book/*.md",
    format="markdown",
    to="epub",
    outputfile=f"{title}.epub",
    extra_args=["--toc", "--toc-depth=3"],
)

print(f"'{title}.epub' is created")