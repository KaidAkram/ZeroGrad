"""Small deterministic content migration for the independently verified extension."""
from pathlib import Path
p=Path('studio/src/main.tsx')
s=p.read_text(encoding='utf-8')
s=s.replace('The original four-block transformer is not presented as verified.',
            'A separate four-block transformer implements the same narrow grammar; its evidence is linked below.')
s=s.replace('${pct(r.ci[0])}?${pct(r.ci[1])}', '${pct(r.ci[0])} to ${pct(r.ci[1])}')
extension_link='<a href="./data/transformer_validation.json">Four-block extension evidence ↗</a>'
s=s.replace(extension_link,'')
s=s.replace('<a href="./data/limitations.md">Known limitations ↗</a>',
            '<a href="./data/limitations.md">Known limitations ↗</a><a href="./data/transformer_validation.json">Four-block extension evidence ↗</a>')
p.write_text(s,encoding='utf-8')
