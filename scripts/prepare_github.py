"""Apply publication metadata and keep generated documentation reproducible."""
import json
from pathlib import Path

def main():
    # The dedicated front-door generator owns README; paper regeneration must retain it.
    p=Path('scripts/report.py');text=p.read_text(encoding='utf-8')
    start=text.find("    write('README.md',f'''")
    if start!=-1:
        end=text.index("    write('career/CV_BULLETS.md'",start)
        text=text[:start]+text[end:]
    marker="    from scripts.readme import generate as generate_readme\n    generate_readme()\n"
    if marker not in text:text=text.replace("\nif __name__=='__main__':generate()",'\n'+marker+"\nif __name__=='__main__':generate()")
    text=text.replace('Author: project owner (affiliation unspecified).','Author: Akram Kaid. Affiliation not specified.')
    text=text.replace('[Repository URL to be supplied before posting]','https://github.com/KaidAkram/ZeroGrad')
    text=text.replace('[Repository link]','https://github.com/KaidAkram/ZeroGrad')
    p.write_text(text,encoding='utf-8')
    p=Path('scripts/finalize_docs.py');text=p.read_text(encoding='utf-8')
    text=text.replace('author metadata should be configured before publication.','source and evidence are available in the linked repository.')
    text=text.replace('  - name: "ZeroGrad-Sec contributors"','  - family-names: "Kaid"\n    given-names: "Akram"\nrepository-code: "https://github.com/KaidAkram/ZeroGrad"\nurl: "https://github.com/KaidAkram/ZeroGrad"')
    text=text.replace('studio/public/media/\n','studio/public/media/\n.publish/\n')
    p.write_text(text,encoding='utf-8')
    p=Path('scripts/release_check.py');text=p.read_text(encoding='utf-8')
    text=text.replace("'Author metadata and a real repository URL must be configured before publication; workspace began without Git history.',",
                      "'Repository and author metadata are configured; consult docs/PUBLISHING.md for the observed publication state.',")
    text=text.replace("'.pytest_cache','.git'}","'.pytest_cache','.git','.publish'}")
    # Publication status is reported by the publishing record rather than guessed here.
    text=text.replace('No deployment, external post, email or DM has occurred.',
                      'Website deployment and social posting are separate actions; repository publication is recorded in docs/PUBLISHING.md.')
    p.write_text(text,encoding='utf-8')

if __name__=='__main__':main()
