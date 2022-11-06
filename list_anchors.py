import argparse
import requests
from bs4 import BeautifulSoup
import sys
from tqdm import tqdm


def get_anchors_with_href(url):
    http_res = requests.get(url)
    html_document = http_res.text
    html_parser = BeautifulSoup(html_document, 'html.parser')
    return [a for a in html_parser.find_all('a') if a.has_attr('href')]


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='List anchors from HTML document')

    arg_parser.add_argument('url', metavar='URL', help='URL for HTML document')
    arg_parser.add_argument('-o', '--output', metavar='FILENAME', help='Filename to save results')

    args = arg_parser.parse_args()

    if args.output is None:
        output_file = sys.stdout
    else:
        output_file = open(args.output, 'w')

    try:
        for anchor in tqdm(get_anchors_with_href(args.url)):
            href = anchor.attrs['href']
            output_file.write(href + '\n')
            for inner_anchor in get_anchors_with_href(href):
                output_file.write('\t' + inner_anchor.attrs['href'] + '\n')
    finally:
        output_file.close()
