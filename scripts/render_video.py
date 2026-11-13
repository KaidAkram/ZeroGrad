"""Original deterministic Pillow/FFmpeg fallback; motion consumes recorded writes."""
import json
import math
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

BG='#07090e';FG='#f0f3f5';MUTED='#94a3b8';GREEN='#10b981';AMBER='#f59e0b'
FONT=Path('C:/Windows/Fonts/arial.ttf')
BOLD=Path('C:/Windows/Fonts/arialbd.ttf')
def font(size,bold=False):
    candidates=[BOLD if bold else FONT,Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    for p in candidates:
        if p.exists(): return ImageFont.truetype(str(p),size)
    return ImageFont.load_default(size=size)

def frame(t,w,h,data,stream,card=None):
    im=Image.new('RGB',(w,h),BG);d=ImageDraw.Draw(im);s=w/1080;wide=w>h
    left=int(w*.08);top=int(h*.08);fs=lambda n:font(max(12,int(n*s)),True)
    def text(x,y,msg,size=24,fill=FG): d.text((int(x),int(y)),msg,font=fs(size),fill=fill)
    chapter=card if card is not None else (0 if t<7 else 2 if t<23 else 3 if t<34 else 4)
    titles=[['NEURAL WEIGHTS.','WRITTEN AS CODE?'],['A BOUNDED','REGISTER MACHINE.'],['SYMBOLIC RULE.','REAL TENSOR.'],['ANALYTIC EDIT.','MEASURABLE DRIFT.'],['SOME RULES COMPILE.','LIMITS STILL MATTER.'],['THE NEXT EXPERIMENT','IS A HARDER TEST.']]
    subs=['Direct compilation / synthetic security grammar','64-dimensional embedding / finite entity vocabulary','Exact authored coordinates / deterministic replay','Synthetic associative memory / no backpropagation','Evidence from the bounded diagnostic suite','Semantic generalization remains untested']
    text(left,top,'ZEROGRAD—SEC     /     RESEARCH PROTOTYPE',18,GREEN)
    title_y=top+70*s
    for i,line in enumerate(titles[chapter]): text(left,title_y+i*64*s,line,49)
    text(left,title_y+150*s,subs[chapter],20,MUTED)
    area_y=title_y+235*s; area_h=h-area_y-180*s
    if wide:
        # Wide framing keeps typography left and instrument right.
        im=Image.new('RGB',(w,h),BG);d=ImageDraw.Draw(im)
        text(left,top,'ZEROGRAD—SEC / RESEARCH PROTOTYPE',13,GREEN)
        for i,line in enumerate(titles[chapter]):text(left,top+130+i*70,line,30)
        for i,line in enumerate(subs[chapter].split(' / ')):text(left,top+320+i*42,line,14,MUTED)
        left=w*.52;area_y=h*.17;area_h=h*.61;s=min(w/1920,h/1080)
    if chapter==1:
        cell=(w*.78 if not wide else w*.4)/16
        for i in range(64):
            x=left+(i%16)*cell;y=area_y+(i//16)*cell
            d.rounded_rectangle((x,y,x+cell-4,y+cell-4),radius=3,fill=GREEN if i<25 else '#14212a')
            text(x+8*s,y+12*s,f'{i:02}',14,BG if i<25 else MUTED)
        text(left,area_y+cell*4+70*s,'00: benign symbol',25)
        text(left,area_y+cell*4+120*s,'01–24: class × stage × entity symbols',25,GREEN)
        text(left,area_y+cell*4+170*s,'25–63: reserved / unused embedding coordinates',21,MUTED)
        text(left,area_y+cell*4+270*s,'Three signatures · two stages · four finite IDs',23)
        text(left,area_y+cell*4+320*s,'Supported length: 2–128 · no semantic tokenizer',21,MUTED)
    elif chapter in [0,2]:
        size=min(w*.78 if not wide else w*.4,area_h*.88);cell=size/16
        e=stream['events'][min(2,int(max(0,t-7)/5))] if chapter==2 else stream['events'][0]
        count=int(len(e['coords'])*min(1,max(.04,(t%7)/7))) if card is None else len(e['coords'])
        active={(i%16,j%16):v for i,j,v in e['coords'][:count]}
        for i in range(16):
            for j in range(16):
                x=left+j*cell;y=area_y+i*cell
                d.rounded_rectangle((x,y,x+cell-4,y+cell-4),radius=3,fill=GREEN if (i,j) in active else '#14212a')
        text(left,area_y+size+20*s,f"{e['tensor']} {e['shape']}   /   {e['id']}",21,GREEN)
        text(left,area_y+size+56*s,'Folded coordinate view; exact values in the studio',16,MUTED)
        if card==2:
            first=e['coords'][0]
            text(left,area_y+size+98*s,f"{e['formula']}   /   [{first[0]}, {first[1]}] = {first[2]:g}",19)
        # A moving scan is visual interpolation, not a computation checkpoint.
        yy=area_y+(t%7)/7*size;d.line((left,yy,left+size,yy),fill='#06b6d4',width=2)
    elif chapter==3:
        edit=data['edits'][2];sv=edit['singular_values'][:8];maxv=max(sv)
        bw=(w*.75 if not wide else w*.38)/8
        for i,v in enumerate(sv):
            bh=max(3,v/maxv*area_h*.58);x=left+i*bw
            d.rectangle((x,area_y+area_h*.6-bh,x+bw*.65,area_y+area_h*.6),fill=AMBER)
        text(left,area_y+area_h*.69,f"Rank {edit['rank']}  /  locality weight 1",26,AMBER)
        text(left,area_y+area_h*.80,f"Target MSE {edit['before_mse']:.3f} → {edit['target_mse']:.6f}",23)
        text(left,area_y+area_h*.91,f"Unrelated output drift (MSE): {edit['drift']:.5f}",20,MUTED)
    elif chapter==4:
        rows=[r for r in data['results'] if r['study']=='E2' and r['seed']==data['seed']]
        for i,r in enumerate(rows):
            y=area_y+i*75*s;span=w*.56 if not wide else w*.3
            text(left,y,f"L={r['length']}",23,MUTED)
            d.rectangle((left+100*s,y,left+100*s+span,y+30*s),fill='#14212a')
            d.rectangle((left+100*s,y,left+100*s+span*r['accuracy'],y+30*s),fill=GREEN)
            text(left+100*s,y+34*s,f"{r['correct']}/{r['n']} correct",15)
        text(left,area_y+len(rows)*75*s+35*s,'Length 512: explicit counterexample',23,AMBER)
        text(left,area_y+len(rows)*75*s+80*s,'No real-world detection claim.',22,MUTED)
    else:
        for i,line in enumerate(['01  Architecture-matched training','02  Unseen grammar compositions','03  Calibration distribution shift','04  Independent replication']):
            text(left,area_y+i*100*s,line,26,GREEN if i==0 else FG)
    text(w*.08,h*.90,'CODE  /  EVIDENCE  /  REPRODUCE',16,MUTED)
    text(w*.08,h*.94,'Toy symbols. Bounded assumptions. No production security claims.',14,MUTED)
    if card is None:
        d.rectangle((w*.08,h*.98,w*.08+w*.84*min(t/45,1),h*.982),fill=GREEN)
    return im

def render(quality='preview'):
    data=json.loads(Path('telemetry/benchmark_results.json').read_text());stream=json.loads(Path('telemetry/weight_write_stream.json').read_text())
    Path('outputs').mkdir(exist_ok=True)
    targets=[('zerograd_preview',720,900,5)] if quality=='preview' else [('zerograd_linkedin_reel',1080,1350,45),('zerograd_widescreen',1920,1080,45),('zerograd_teaser_12s',1080,1350,12)]
    for name,w,h,duration in targets:
        cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','60','-i','-','-an','-c:v','libx264','-threads','2','-preset','fast','-crf','20','-pix_fmt','yuv420p',f'outputs/{name}.mp4']
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for f in range(duration*60):
                proc.stdin.write(frame(f/60,w,h,data,stream).tobytes())
                if f%600==0: print(f'{name}: {f}/{duration*60}',flush=True)
        finally: proc.stdin.close()
        if proc.wait()!=0: raise RuntimeError('FFmpeg failed')
        probe=subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',f'outputs/{name}.mp4'])
        Path(f'outputs/{name}.ffprobe.json').write_bytes(probe)
    for t in [1,10,18,27,39,44]: frame(t,1080,1350,data,stream).save(f'outputs/frame_{t:02}.png')
    frame(1,1080,1350,data,stream,0).save('outputs/zerograd_reel_poster.png')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--quality',choices=['preview','final'],default='preview');render(p.parse_args().quality)
