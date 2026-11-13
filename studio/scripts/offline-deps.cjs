// Read the existing npm content-addressed cache without writing outside this project.
const path=require('node:path'),fs=require('node:fs/promises');
const base='C:/Users/Akram KAID/AppData/Roaming/npm/node_modules/npm/node_modules/';
const cache=require(base+'cacache'),tar=require(base+'tar'),semver=require(base+'semver');
(async()=>{
 const source='D:/npm_cache/_cacache', entries=await cache.ls(source), installed=new Set();
 async function install(name,range){
  if(installed.has(name))return;
  const prefix='make-fetch-happen:request-cache:https://registry.npmjs.org/'+name+'/-/';
  let candidates=Object.keys(entries).filter(k=>k.startsWith(prefix)).map(k=>({k,v:k.slice(prefix.length).replace(/^.*?-(\d)/,'$1').replace(/\.tgz$/,'')})).filter(x=>semver.valid(x.v)&&semver.satisfies(x.v,range));
  candidates.sort((a,b)=>semver.rcompare(a.v,b.v));
  if(!candidates.length)throw Error('Missing cache '+name+' '+range);
  const selected=candidates[0],data=await cache.get(source,selected.k);installed.add(name);
  const dest=path.join('node_modules',name);await fs.mkdir(dest,{recursive:true});
  await new Promise((resolve,reject)=>{const out=tar.x({cwd:dest,strip:1});out.on('error',reject).on('close',resolve);out.end(data.data)});
  const pkg=JSON.parse(await fs.readFile(path.join(dest,'package.json'),'utf8'));console.log(name,pkg.version);
  for(const [n,r]of Object.entries(pkg.dependencies||{}))await install(n,r);
  for(const [n,r]of Object.entries(pkg.optionalDependencies||{})){if(n.includes('win32-x64')||n==='@esbuild/win32-x64')await install(n,r)}
 }
 for(const [n,v]of Object.entries({react:'19.2.0','react-dom':'19.2.0',vite:'5.4.21',typescript:'5.9.3','@types/react':'19.2.2','@types/react-dom':'19.2.2','@playwright/test':'1.58.2'}))await install(n,v);
})();
