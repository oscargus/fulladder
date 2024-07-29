from glob import glob
from pathlib import Path
import re
import shutil
from html import escape

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
        url = escape(f"load_url=https://oscargus.github.io/fulladder/{filename}")
        maindir = path.parts[1]
        # Filter out the parts, taken fron VUnit
        match = re.search(r"(.+)\.([^.]+)$", maindir)
        if match:
            # Get rid of the trailing hash
            tmp_testname = match.group(2)
            namematch = re.search(r"(.+)_[a-f0-9]+$", tmp_testname)
            testname = namematch.group(1)
            if testname == "all":
                f.write(f"<li> {match.group(1)}. <a href={filename}>&#11015;</a> <a href=https://app.surfer-project.org/?{url}>&#127940;</a></li>\n")
            else:
                f.write(f"<li> {match.group(1)}, test: {testname}. <a href={filename}>&#11015;</a> <a href=https://app.surfer-project.org/?{url}>&#127940;</a></li>\n")
        else:
            f.write(f"<li> {maindir}. <a href={filename}>&#11015;</a> <a href=https://app.surfer-project.org/?{url}>&#127940;</a></li>\n")
        (html / path.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy(filename, html / filename)
    f.write("</ul>\n")
    f.write("</body>\n")
    f.write("</html>\n")
