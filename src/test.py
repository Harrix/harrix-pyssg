import harrixpyssg as hsg


def main():
    pass
    # markdown_filename = 'C:/Harrix/GitHub/harrix.dev-blog-2019/2019-07-23-add-2-num-android/2019-07-23-add-2-num-android.md'
    # output_path = '../dist'
    # hsg.MarkdownToHtml(markdown_filename, output_path).start()
    markdown_path = 'C:/Harrix/GitHub/harrix.dev-blog-2019/'
    output_path = '../dist'
    hsg.Dir(markdown_path, output_path).start()


if __name__ == '__main__':
    main()
