import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import harrixpyssg as hsg


def main():
    markdown_paths = ['C:/Harrix/GitHub/harrix.dev-blog-2017/']
    output_path = './dist'
    hsg.StaticSiteGenerator(markdown_paths, output_path).start()


if __name__ == '__main__':
    main()
