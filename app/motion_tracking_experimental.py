"""Experimental offline motion-guided 9:16 crop. No puck/player recognition."""
import json
import subprocess
import numpy as np
import cv2


def tracking_keyframes(path, start, duration, samples_per_second=3):
    """Return FFmpeg crop x coordinates at evenly spaced source timestamps."""
    probe = subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","json",str(path)],text=True)
    v=json.loads(probe)["streams"][0]
    width,height=int(v["width"]),int(v["height"])
    crop_width=min(width,round(height*9/16))
    if crop_width>=width:
        return {"width":width,"height":height,"crop_width":crop_width,"positions":[(0,0)]}
    small_w=320
    small_h=max(2,round(height*small_w/width))
    fps=max(1,min(5,int(samples_per_second)))
    cmd=["ffmpeg","-v","error","-ss",str(start),"-i",str(path),"-t",str(duration),
         "-vf",f"fps={fps},scale={small_w}:{small_h},format=gray",
         "-f","rawvideo","-pix_fmt","gray","-"]
    raw=subprocess.check_output(cmd)
    frame_bytes=small_w*small_h
    count=len(raw)//frame_bytes
    if count<2:
        return {"width":width,"height":height,"crop_width":crop_width,"positions":[(0,(width-crop_width)//2)]}
    frames=np.frombuffer(raw[:count*frame_bytes],dtype=np.uint8).reshape(count,small_h,small_w)
    centers=[]
    prev=None
    for frame in frames:
        blurred=cv2.GaussianBlur(frame,(5,5),0)
        if prev is None:
            centers.append(width/2)
        else:
            diff=cv2.absdiff(blurred,prev)
            # Ignore scoreboards/stands and low-amplitude compression noise.
            mask=np.zeros_like(diff)
            top=int(small_h*.30)
            bottom=int(small_h*.94)
            mask[top:bottom]=diff[top:bottom]
            _,mask=cv2.threshold(mask,22,255,cv2.THRESH_BINARY)
            mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
            weights=mask.sum(axis=0,dtype=np.float64)
            if weights.sum()>255*12:
                x=float(np.dot(np.arange(small_w),weights)/weights.sum())*width/small_w
                centers.append(x)
            else:
                centers.append(centers[-1])
        prev=blurred
    # Strong temporal smoothing, plus bounded camera speed.
    x=(width-crop_width)/2
    max_step=width*.035/fps
    positions=[]
    for i,center in enumerate(centers):
        desired=max(0,min(width-crop_width,center-crop_width/2))
        delta=max(-max_step,min(max_step,(desired-x)*.22))
        x=max(0,min(width-crop_width,x+delta))
        positions.append((i/fps,round(x)))
    return {"width":width,"height":height,"crop_width":crop_width,"positions":positions}


def crop_filter(path,start,duration):
    """Return filter chain. FFmpeg evaluates a smooth time-dependent x expression."""
    info=tracking_keyframes(path,start,duration)
    positions=info["positions"]
    if len(positions)==1:
        expr=str(positions[0][1])
    else:
        # Piecewise linear x(t) interpolation, with safe fixed endpoint.
        expr=str(positions[-1][1])
        for (t0,x0),(t1,x1) in reversed(list(zip(positions[:-1],positions[1:]))):
            dt=max(.001,t1-t0)
            segment=f"({x0}+({x1-x0})*(t-{t0:.4f})/{dt:.4f})"
            expr=f"if(lt(t,{t1:.4f}),{segment},{expr})"
    # Crop filter uses 't' only in some FFmpeg builds; use frame index n instead
    # for portability at fixed source output fps after fps filter.
    fps=3
    expr=expr.replace("t-",f"n/{fps}-").replace("lt(t,",f"lt(n/{fps},")
    return f"fps={fps},crop={info['crop_width']}:{info['height']}:x='{expr}':y=0,scale=1080:1920"
