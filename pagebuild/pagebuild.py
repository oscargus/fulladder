from glob import glob
from pathlib import Path
import shutil

html = Path('html')

html.mkdir(exist_ok = True)



with (html / 'index.html').open(mode='w') as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<head>\n")
    f.write("<title>Simulation wave forms</title>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<ul>")
    for filename in glob('test_output/**/*.ghw', recursive=True):
        path = Path(filename)
        f.write(f"<li> {filename}: <a href={filename}>Download</a>, <a href=https://app.surfer-project.org/?https://oscargus.github.io/fulladder/{filename}>Open in Surfer</a></li>\n")
        (html / path.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy(filename, html / filename)
    f.write("</ul>\n")
    f.write("</body>\n")
    f.write("</html>\n")
