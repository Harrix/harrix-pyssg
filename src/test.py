from harrix_markdown_to_html import HarrixMarkdownToHtml


def main():
    markdown_filename = 'C:/Harrix/GitHub/harrix.dev-blog-2019/2019-07-23-add-2-num-android/2019-07-23-add-2-num-android.md'
    output_path = '../dist'
    h = HarrixMarkdownToHtml(markdown_filename, output_path)


if __name__ == '__main__':
    main()
