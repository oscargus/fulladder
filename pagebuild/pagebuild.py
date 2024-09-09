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


def find_failure(test):
    for child in test:
        if child.tag == "failure":
            return child.attrib["message"]


with (html / 'index.html').open(mode='w') as f:
    f.write(
        """
<!DOCTYPE html>
<html>
<head>
<style>
.failTest {
  margin-top: 10px;
  padding: 2px 2px 2px 2px;
  border: 3px outset red;
  background-color: lightgray;
  width: 800px;  
}
.passTest {
  margin-top: 10px;
  padding: 2px 2px 2px 2px;
  border: 3px outset green;
  background-color: lightgray;
  width: 800px;  
}
.testDetails {
  overflow-x: auto;
  overflow-y: auto;
  max-height: 100px;
}

</style>
<title>Simulation wave forms</title>
</head>
<body>
""")
    f.write(f"<p>{root.attrib['tests']} test(s) ({root.attrib['failures']} failure(s), {root.attrib['skipped']} skipped)")
    for filename in glob('test_output/**/*.vcd', recursive=True):
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
            failure = find_failure(test)
            if failure:
                f.write(f'<div class="failTest">')
            else:
                f.write(f'<div class="passTest">')
            if testname == "all":
                f.write(f'{match.group(1)} <a title="Download" href={filename}>&#11015;</a> <a title="Open in Surfer (new tab)" href=https://app.surfer-project.org/?{url} target="_blank">&#127940;</a>\n')
            else:
                f.write(f'{match.group(1)} - {testname} <a title="Download" href={filename}>&#11015;</a> <a title="Open in Surfer (new tab)" href=https://app.surfer-project.org/?{url} target="_blank">&#127940;</a>\n')
            if sysout:
                f.write('<div class="testDetails">')
                f.write('<details>\n')
                f.write("<summary>System output</summary>\n")
                f.write(f'<p><pre>\n{sysout}\n</pre></p>\n')
                f.write("</details>\n")
                f.write('</div>\n')
            f.write('</div>\n')
        else:
            f.write(f'<div class="passTest"> {maindir} <a title="Download" href={filename}>&#11015;</a> <a title="Open in Surfer (new tab)" href=https://app.surfer-project.org/?{url} target="_blank">&#127940;</a></div>\n')
        (html / path.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy(filename, html / filename)
    f.write("</body>\n")
    f.write("</html>\n")
