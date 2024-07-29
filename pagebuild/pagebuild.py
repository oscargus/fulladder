from glob import glob
from pathlib import Path
import re
import shutil
from html import escape
import xml.etree.ElementTree as ET

html = Path('html')

html.mkdir(exist_ok = True)

tree = ET.parse('test.xml')
root = tree.getroot()

def find_test(classname, testname):
    for child in root:
        if child.attrib["classname"] == classname and child.attrib["name"] == testname:
            return child


def find_sysout(test):
    for child in test:
        if child.tag == "system-out":
            return child.text


with (html / 'index.html').open(mode='w') as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<head>\n")
    f.write("<title>Simulation wave forms</title>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write(f"<p>{root.attrib['tests']} test(s) ({root.attrib['failure(s)']} failures, {root.attrib['skipped']} skipped)")
    f.write("<ul>")
    for filename in glob('test_output/**/*.ghw', recursive=True):
        path = Path(filename)
        url = escape(f"load_url=https://oscargus.github.io/fulladder/{filename}")
        maindir = path.parts[1]
        # Filter out the parts, taken fron VUnit
        match = re.search(r"(.+)\.([^.]+)$", maindir)
        if match:
            classname = match.group(1)
            # Get rid of the trailing hash
            tmp_testname = match.group(2)
            namematch = re.search(r"(.+)_[a-f0-9]+$", tmp_testname)
            testname = namematch.group(1)
            test = find_test(classname, testname)
            sysout = find_sysout(test)
            if testname == "all":
                f.write(f'<li> {match.group(1)} <a title="Download" href={filename}>&#11015;</a> <a title="Open in Surfer (new tab)" href=https://app.surfer-project.org/?{url} target="_blank">&#127940;</a></li>\n')
            else:
                f.write(f'<li> {match.group(1)} - {testname} <a title="Download" href={filename}>&#11015;</a> <a title="Open in Surfer (new tab)" href=https://app.surfer-project.org/?{url} target="_blank">&#127940;</a></li>\n')
            if sysout:
                f.write("<details>\n") 
                f.write("<summary>System output</summary>\n")
                f.write(f"<p><pre>{sysout}</pre></p>\n")
                f.write("</details>\n") 
        else:
            f.write(f'<li> {maindir} <a title="Download" href={filename}>&#11015;</a> <a title="Open in Surfer (new tab)" href=https://app.surfer-project.org/?{url} target="_blank">&#127940;</a></li>\n')
        (html / path.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy(filename, html / filename)
    f.write("</ul>\n")
    f.write("</body>\n")
    f.write("</html>\n")
