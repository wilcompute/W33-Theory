from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'analysis' / 'BT667_codec_g2_paper_insert.tex'
DST = ROOT / 'paper' / 'sections' / 'sec_bt667_codec_g2_chart.tex'
PREPRINT = ROOT / 'paper' / 'w33_preprint.tex'
INPUT = '\\input{sections/sec_bt667_codec_g2_chart}'
MARKER = '\\input{sections/sec_bt662_secondary_codec_g2_channel}'

def main():
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(SRC.read_text(encoding='utf-8'), encoding='utf-8')
    text = PREPRINT.read_text(encoding='utf-8')
    if INPUT not in text:
        if MARKER in text:
            text = text.replace(MARKER, MARKER + '\n' + INPUT, 1)
        else:
            text = text + '\n' + INPUT + '\n'
        PREPRINT.write_text(text, encoding='utf-8')
    print('integrated BT667')

if __name__ == '__main__':
    main()
