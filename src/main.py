import os
import pathlib
import shutil
import markdown


path = 'C:/Harrix/GitHub/harrix.dev-blog-2019/2019-07-23-add-2-num-android/2019-07-23-add-2-num-android.md'
output_path = '../dist'

# shutil.rmtree(output_path)

p = pathlib.Path(path)
print(p.parents[0])
destination = shutil.copytree(str(p.parents[0]) + "/img", output_path + "/img", dirs_exist_ok=True)

with open(path, 'r', encoding='utf8') as markdown_file:
    s = markdown_file.read()

html = markdown.markdown(s)

with open(output_path + "/output.html", 'w', encoding='utf8') as html_file:
    html_file.write(html)
