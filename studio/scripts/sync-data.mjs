import {mkdir,copyFile,access,writeFile} from 'node:fs/promises';
await mkdir('public/data',{recursive:true});
for(const file of ['benchmark_results.json','weight_write_stream.json']) {
 try {await copyFile('../telemetry/'+file,'public/data/'+file)} catch {await writeFile('public/data/'+file,JSON.stringify(file.startsWith('benchmark')?{results:[],edits:[]}:{events:[]}));}
}
for(const [source,target] of [['../paper/zerograd_sec_paper.md','research.md'],['../docs/CLAIM_REGISTER.md','claims.md'],['../docs/KNOWN_LIMITATIONS.md','limitations.md'],['../outputs/metrics.csv','metrics.csv']]){try {await access(source);await copyFile(source,'public/data/'+target)}catch{}}
for(const file of ['transformer_validation.json','transformer_weight_stream.json']){try{await copyFile('../telemetry/'+file,'public/data/'+file)}catch{}}
await mkdir('public/media',{recursive:true});
for(const file of ['zerograd_linkedin_reel.mp4','zerograd_widescreen.mp4','zerograd_reel_poster.png','zerograd_subtitles.vtt']){try{await copyFile('../outputs/'+file,'public/media/'+file)}catch{}}
