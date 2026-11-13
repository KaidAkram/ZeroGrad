"""Build a local visual preview; GitHub owns its Mermaid/math rendering."""
from pathlib import Path
import markdown

root=Path(__file__).resolve().parents[1]
out=root/'.publish';out.mkdir(exist_ok=True)
body=markdown.markdown((root/'README.md').read_text(encoding='utf-8'),extensions=['tables','fenced_code'])
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><base href="../"><title>ZeroGrad README preview</title><style>
body{margin:0;background:#f6f8fa;color:#1f2328;font:16px/1.65 Arial,sans-serif}article{max-width:1000px;margin:30px auto;padding:40px;background:white;border:1px solid #d1d9e0;border-radius:8px}img{max-width:100%;height:auto}a{color:#0969da;text-decoration:none}h1,h2{border-bottom:1px solid #d1d9e0;padding-bottom:8px;line-height:1.3}h1{font-size:32px}h2{font-size:24px;margin-top:40px}h3{font-size:20px}table{border-collapse:collapse;display:block;overflow:auto;font-size:14px}td,th{padding:10px 13px;border:1px solid #d1d9e0}tr:nth-child(even){background:#f6f8fa}pre{padding:18px;background:#f6f8fa;overflow:auto;border-radius:6px;line-height:1.5}code{font-family:Consolas,monospace;font-size:14px}blockquote{border-left:4px solid #0969da;padding:6px 18px;background:#f0f7ff;margin:24px 0;color:#374151}summary{cursor:pointer}li{margin:7px 0}
</style></head><body><article>'''+body+'</article></body></html>'
(out/'README-preview.html').write_text(html,encoding='utf-8')
node=r'''const {chromium}=require('../studio/node_modules/playwright');
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});try{const page=await browser.newPage({viewport:{width:1280,height:1000}});await page.goto(require('node:url').pathToFileURL(require('node:path').resolve('.publish/README-preview.html')).href);await page.screenshot({path:'.publish/README-preview.png',fullPage:false});await page.screenshot({path:'.publish/README-preview-full.png',fullPage:true});console.log('README layout screenshot captured. Local preview excludes GitHub Mermaid/math processing.')}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});'''
(out/'preview.cjs').write_text(node,encoding='utf-8')
print('Local README visual preview written to .publish/README-preview.html')
