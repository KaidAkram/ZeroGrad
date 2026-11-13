// Restore registry integrity metadata after a read-only offline cache recovery.
const fs=require('node:fs');
const cacache=require('C:/Users/Akram KAID/AppData/Roaming/npm/node_modules/npm/node_modules/cacache');
(async()=>{
 const entries=await cacache.ls('D:/npm_cache/_cacache');
 const lock=JSON.parse(fs.readFileSync('package-lock.json','utf8'));
 for(const [key,p]of Object.entries(lock.packages)){
  if(!key)continue;
  const name=key.replace(/^node_modules\//,''),url=`https://registry.npmjs.org/${name}/-/${name.split('/').pop()}-${p.version}.tgz`;
  const entry=entries['make-fetch-happen:request-cache:'+url];
  if(entry){p.resolved=url;p.integrity=entry.integrity}
 }
 fs.writeFileSync('package-lock.json',JSON.stringify(lock,null,2)+'\n');
})();
