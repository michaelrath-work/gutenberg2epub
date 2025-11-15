import os
import pathlib
import pprint
import requests
import typing
import yaml


THIS_DIR = pathlib.Path(__file__).parent
RAW_DIR = THIS_DIR / '..' / 'raw'
PROCESSED_DIR = THIS_DIR / '..' / 'processed'

def _extract(lines: typing.List[str]) -> typing.List[str]:
    result = []
    capture = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('<h2>') or stripped.startswith('<h3>'):
            capture = True

        if capture and stripped.startswith(f'<hr size="1"'):
            break

        if capture:
            result.append(line)

    return result


def convert_chapter(chapter: int) -> None:
    p = RAW_DIR / f'chap{chapter:03d}.html'
    print(f'Processing {p}...')
    with open(p, 'r') as f:
        lines = f.readlines()

    extracted = _extract(lines)
    # pprint.pprint(extracted)

    pathlib.Path('processed').mkdir(exist_ok=True)

    p = PROCESSED_DIR / f'chap{chapter:03d}.xhtml'
    print(f'Writing to {p}')
    with open(p, 'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"\n')
        f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        f.write('<head>\n')
        f.write('<link href="../Styles/prosa.css" rel="stylesheet" type="text/css"/>\n')
        f.write('<title></title>\n')
        f.write('</head>\n')
        f.write('<body>\n')

        f.writelines('\n'.join(extracted))

        f.write('</body>\n')
        f.write('</html>\n')


def read_config(filename: str = 'config.yaml') -> typing.Mapping[str, any]:
    cfg_file_path = THIS_DIR / filename
    with open(cfg_file_path, 'r') as f:
        config = yaml.safe_load(f)
        pprint.pprint(config)
        return config


def fetch_files(cfg: typing.Mapping[str, any]):
    start = cfg['chapters']['start']
    end = cfg['chapters']['end']
    base_url =  cfg['base_url']

    RAW_DIR.mkdir(exist_ok=True)

    for chapter in range(start, end + 1):
        chapter_filename_html = f'chap{chapter:03d}.html'
        url = os.path.join(base_url, chapter_filename_html)
        pprint.pprint(f'Fetch {chapter}: {url}')

        output_file_path = RAW_DIR / chapter_filename_html
        response = requests.get(url)

        with open(output_file_path, 'wb') as file:
            file.write(response.content)


def convert_chapters(cfg: typing.Dict[str, any]):
    start = cfg['chapters']['start']
    end = cfg['chapters']['end']

    PROCESSED_DIR.mkdir(exist_ok=True)

    for i in range(start, end+1):
        convert_chapter(i)


def main():
    cfg = read_config(filename='config_template.yaml')
    fetch_files(cfg)
    convert_chapters(cfg)

if __name__ == '__main__':
    main()