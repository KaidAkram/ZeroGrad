"""Validate encoded dimensions, rates, durations and representative decoded frames."""
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

def verify():
    expected={'zerograd_preview':(720,900,5),'zerograd_linkedin_reel':(1080,1350,45),'zerograd_widescreen':(1920,1080,45),'zerograd_teaser_12s':(1080,1350,12)}
    results=[];tiles=[]
    Path('outputs/media_qa').mkdir(exist_ok=True)
    for name,(w,h,duration) in expected.items():
        path=Path('outputs')/(name+'.mp4')
        if not path.exists():
            results.append(dict(path=str(path),status='FAIL',reason='missing video'));continue
        obj=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(path)]))
        stream=next(s for s in obj['streams'] if s['codec_type']=='video')
        assert (stream['width'],stream['height'])==(w,h),name
        assert stream['r_frame_rate']=='60/1' and stream['codec_name']=='h264' and stream['pix_fmt']=='yuv420p',name
        assert abs(float(obj['format']['duration'])-duration)<.05,name
        assert int(stream['nb_frames'])==duration*60,name
        # Full decode catches broken frames/bitstream errors; -xerror makes failures fatal.
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'],check=True,timeout=180)
        times=[1,10,18,27,39,44] if duration==45 else [1,duration-1]
        stats=[]
        for t in times:
            out=Path('outputs/media_qa')/f'{name}_{t:02}.png'
            subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1',str(out)],check=True,timeout=30)
            im=Image.open(out).convert('RGB');a=np.array(im)
            # Obsidian backgrounds are intentional; reject nearly uniform/blank frames.
            assert float(a.std())>8,f'blank-looking frame {name}@{t}'
            stats.append(dict(time=t,pixel_std=float(a.std())))
            if duration==45:
                tile=Image.new('RGB',(384,300),'#07090e');thumbnail=im.copy();thumbnail.thumbnail((384,270));tile.paste(thumbnail,((384-thumbnail.width)//2,0));ImageDraw.Draw(tile).text((8,278),f'{name} / {t}s',fill='white');tiles.append(tile)
        results.append(dict(path=str(path),status='PASS',width=w,height=h,fps=60,frames=duration*60,duration=duration,codec='h264',pixel_format='yuv420p',full_decode=True,frame_probes=stats))
    if tiles:
        sheet=Image.new('RGB',(384*6,300*2),'#07090e')
        for i,tile in enumerate(tiles):sheet.paste(tile,((i%6)*384,(i//6)*300))
        sheet.save('outputs/media_qa/contact_sheet.png')
    Path('outputs/MEDIA_QA.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    return results

if __name__=='__main__':print(json.dumps(verify(),indent=2))
