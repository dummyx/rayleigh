import os
import re
import subprocess

from bs4 import BeautifulSoup as bs

AOZORA_PATH = './aozorabunko/cards/'
MAIN_TXT_PATH = './main_texts/'
TSV_PATH = './tsv/'


def process_aozora_card(card_path):
    for root, _, files in os.walk(card_path):
        for file in files:
            if file.endswith('.html'):
                process_aozora_html(os.path.join(root, file))


def process_aozora_html(html_path):
    cardname = os.path.basename(html_path.replace('.html', ''))
    txt_file_path = os.path.join(MAIN_TXT_PATH, cardname+'.txt')
    tsv_file_path = os.path.join(TSV_PATH, cardname+'.tsv')
    if os.path.exists(tsv_file_path):
        return
    try:
        with open(html_path, 'r', encoding='shift_jis') as f:
            html = f.read()
            html = strip_ruby(html)
            soup = bs(html, 'lxml')

            main_texts = soup.find_all('div', {'class': 'main_text'})
            for main_text in main_texts:
                write_main_text_txt(main_text.text, txt_file_path)
                generate_tsv(txt_file_path, tsv_file_path)
    except UnicodeDecodeError:
        with open('failed.txt', 'a', encoding='utf-8') as f:
            f.write(html_path+'\n')


def write_main_text_txt(main_text, txt_file_path):
    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(main_text)


def generate_tsv(text_file_path, tsv_file_path):
    command = ['ginza', '-p', '16', text_file_path]
    with open(tsv_file_path, 'w', encoding='utf-8') as f:
        subprocess.run(command, stdout=f)


def strip_ruby(text):
    pattern = re.compile(r'（?<\/rp><rt>.*<\/rt><rp>）?')
    return pattern.sub('', text)


def main():
    for root, dirs, _ in os.walk(AOZORA_PATH):
        for dir in dirs:
            if dir == 'files':
                process_aozora_card(os.path.join(root, dir))


if __name__ == '__main__':
    main()
