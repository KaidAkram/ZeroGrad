const fs=require('node:fs');
const p=JSON.parse(fs.readFileSync('package.json','utf8').replace(/^\uFEFF/,''));
p.scripts.build='node node_modules/typescript/bin/tsc --noEmit && node scripts/build.mjs';
p.scripts.dev='node scripts/dev.mjs';
for(const group of [p.dependencies,p.devDependencies])for(const [k,v]of Object.entries(group)){const match=v.match(/-(\d[^/]+)\.tgz$/);if(match)group[k]=match[1]}
fs.writeFileSync('package.json',JSON.stringify(p,null,2));
fs.writeFileSync('src/style.css',fs.readFileSync('src/style.css','utf8').replace("@import url('');",''));
