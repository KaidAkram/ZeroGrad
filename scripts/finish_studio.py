"""Connect the actual exported film to the static studio."""
from pathlib import Path
p=Path('studio/src/main.tsx');s=p.read_text(encoding='utf-8')
s=s.replace('<a href="#edit">Edit lab</a>','<a href="#edit">Edit lab</a><a href="#film">Film</a>')
film='''<section id="film" className="film-section"><div className="section-head"><div><p className="eyebrow">THE 45-SECOND FILM</p><h2>Recorded science.<br/><em>Original motion.</em></h2></div><a className="text-link" href="./media/zerograd_linkedin_reel.mp4" download>Download portrait film ↗</a></div><video controls preload="none" poster="./media/zerograd_reel_poster.png" aria-label="ZeroGrad-Sec: bounded compilation, analytic editing and measured limits"><source src="./media/zerograd_widescreen.mp4" type="video/mp4"/><track kind="captions" src="./media/zerograd_subtitles.vtt" srcLang="en" label="English" default/></video><p className="caption">Actual 45-second, 60fps render. Main film: prefix-circuit experiment and synthetic association edit. The separately validated transformer extension is linked in the evidence section. Silent by design; captions available.</p></section>'''
if 'className="film-section"' not in s:s=s.replace('<section id="compiler"',film+'\n <section id="compiler"')
p.write_text(s,encoding='utf-8')
p=Path('studio/src/style.css');s=p.read_text(encoding='utf-8')
if '.film-section{' not in s:s+='\n.film-section{padding:90px 5%;border-top:1px solid #1e293b}.film-section video{display:block;width:100%;max-height:680px;background:#07090e;border:1px solid #1e293b;border-radius:4px}.film-section .caption{margin-top:18px;max-width:900px}\n'
p.write_text(s,encoding='utf-8')
