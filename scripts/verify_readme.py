"""Check that the GitHub README references real local artifacts and valid SVG."""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def verify():
    text=Path('README.md').read_text(encoding='utf-8')
    references=re.findall(r'\[[^\]]+\]\(([^)]+)\)',text)+re.findall(r'src="([^"]+)"',text)
    missing=[]
    for reference in references:
        if reference.startswith(('https://','http://','#')):continue
        target=Path(reference.split('#')[0])
        if not target.is_file():missing.append(reference)
    if missing:raise ValueError('Missing README artifacts: '+repr(missing))
    if any(ord(c)<32 and c not in '\n\r\t' for c in text):raise ValueError('Unexpected control character in README')
    for p in Path('design/readme').glob('*.svg'):ET.parse(p)
    if 'https://github.com/KaidAkram/ZeroGrad' not in text:raise ValueError('Incorrect repository metadata')
    print(f'README verified: {len(references)} references, 0 missing artifacts, valid SVG, no unexpected control characters.')

if __name__=='__main__':verify()
