import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from datetime import datetime
import subprocess, json, shutil, threading, re, os

APP_NAME="Sentinelles Content Factory MVP 0.2"
NAVY="#081B4B"; RED="#E41F2B"

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title(APP_NAME); self.geometry("980x680"); self.configure(bg="#F3F5F9")
        self.files=[]; self.output=Path.cwd()/"exports"; self.output.mkdir(exist_ok=True)
        self.event=tk.StringVar(value="Nouvel événement"); self.sponsor=tk.StringVar(value=""); self.status=tk.StringVar(value="Prêt")
        self._ui()

    def _ui(self):
        top=tk.Frame(self,bg=NAVY,height=76); top.pack(fill="x")
        tk.Label(top,text="LES SENTINELLES",bg=NAVY,fg="white",font=("Arial",20,"bold")).pack(side="left",padx=24,pady=20)
        tk.Label(top,text="CONTENT FACTORY - MVP LOCAL",bg=NAVY,fg="#D9E2FF",font=("Arial",11,"bold")).pack(side="left",pady=25)
        body=tk.Frame(self,bg="#F3F5F9"); body.pack(fill="both",expand=True,padx=24,pady=18)
        form=tk.LabelFrame(body,text=" 1. ÉVÉNEMENT ",bg="white",fg=NAVY,font=("Arial",11,"bold")); form.pack(fill="x",pady=6)
        tk.Label(form,text="Nom",bg="white").grid(row=0,column=0,sticky="w",padx=12,pady=10); tk.Entry(form,textvariable=self.event,width=42).grid(row=0,column=1,padx=8)
        tk.Label(form,text="Partenaire(s)",bg="white").grid(row=0,column=2,sticky="w",padx=12); tk.Entry(form,textvariable=self.sponsor,width=32).grid(row=0,column=3,padx=8)
        imp=tk.LabelFrame(body,text=" 2. RUSHS ",bg="white",fg=NAVY,font=("Arial",11,"bold")); imp.pack(fill="both",expand=True,pady=6)
        bar=tk.Frame(imp,bg="white"); bar.pack(fill="x",padx=10,pady=8)
        tk.Button(bar,text="IMPORTER DES VIDÉOS",command=self.pick,bg=RED,fg="white",relief="flat",padx=14,pady=7).pack(side="left")
        tk.Button(bar,text="CHOISIR EXPORT",command=self.pick_output,padx=12,pady=7).pack(side="left",padx=8)
        self.list=tk.Listbox(imp,height=10); self.list.pack(fill="both",expand=True,padx=10,pady=(0,10))
        actions=tk.LabelFrame(body,text=" 3. AUTOMATISATION ",bg="white",fg=NAVY,font=("Arial",11,"bold")); actions.pack(fill="x",pady=6)
        tk.Button(actions,text="ANALYSER & CRÉER 3 SHORTS",command=self.run_thread,bg=NAVY,fg="white",font=("Arial",11,"bold"),relief="flat",padx=16,pady=10).pack(side="left",padx=12,pady=12)
        tk.Button(actions,text="OUVRIR EXPORTS",command=self.open_exports,padx=12,pady=9).pack(side="left")
        tk.Label(actions,textvariable=self.status,bg="white",fg="#475467").pack(side="right",padx=15)
        self.progress=ttk.Progressbar(body,mode="indeterminate"); self.progress.pack(fill="x",pady=6)
        tk.Label(body,text="Validation humaine requise avant publication. FFmpeg obligatoire.",bg="#F3F5F9",fg="#667085").pack(anchor="w")

    def pick(self):
        fs=filedialog.askopenfilenames(filetypes=[("Vidéos","*.mp4 *.mov *.mkv *.avi *.m4v")])
        for f in fs:
            if f not in self.files: self.files.append(f); self.list.insert("end",f)

    def pick_output(self):
        d=filedialog.askdirectory()
        if d: self.output=Path(d); self.status.set(f"Export: {self.output}")

    def run_thread(self):
        if not self.files: messagebox.showwarning("Rushs","Importe au moins une vidéo."); return
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            messagebox.showerror("FFmpeg manquant","Installe FFmpeg et ajoute-le au PATH."); return
        threading.Thread(target=self.process,daemon=True).start()

    def duration(self,f):
        cmd=["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",f]
        return float(subprocess.check_output(cmd,text=True).strip())

    @staticmethod
    def event_slug(name):
        return re.sub(r'[^A-Za-z0-9_-]+','_',name).strip('_') or "evenement"

    @staticmethod
    def build_candidates(sources):
        # Round-robin by temporal tier: this guarantees that, when >=3 rushs exist,
        # the three first candidates come from distinct rushs.
        tiers=(.25,.50,.75)
        candidates=[]
        for frac in tiers:
            for src in sources:
                d=src["duration"]
                start=max(0,d*frac-9)
                dur=min(18,max(0,d-start))
                if dur >= 1:
                    candidates.append({"file":src["file"],"start":start,"duration":dur,"fraction":frac})
        return candidates

    @staticmethod
    def select_candidates(candidates, limit=3, min_gap=12):
        selected=[]
        for c in candidates:
            duplicate=any(
                c["file"]==s["file"] and abs(c["start"]-s["start"]) < min_gap
                for s in selected
            )
            if not duplicate:
                selected.append(c)
            if len(selected) >= limit:
                break
        return selected

    def new_run_dir(self):
        event_dir=self.output/self.event_slug(self.event.get())
        event_dir.mkdir(parents=True,exist_ok=True)
        stamp=datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        run_dir=event_dir/f"run_{stamp}"
        run_dir.mkdir(parents=True,exist_ok=False)
        return run_dir

    def process(self):
        self.progress.start(10); self.status.set("Analyse en cours...")
        run_dir=self.new_run_dir()
        report={"schema_version":"0.2","event":self.event.get(),"sponsors":self.sponsor.get(),
                "run_dir":str(run_dir),"sources":[],"candidates":[],"exports":[]}
        try:
            for f in self.files:
                d=self.duration(f)
                report["sources"].append({"file":f,"duration":d})

            candidates=self.build_candidates(report["sources"])
            selected=self.select_candidates(candidates,3)
            report["candidates"]=selected

            for i,c in enumerate(selected,1):
                out=run_dir/f"short_{i:02d}_9x16.mp4"
                vf="scale=-2:1920,crop=1080:1920:(iw-1080)/2:0,drawbox=x=0:y=0:w=iw:h=150:color=0x081B4B@0.82:t=fill,drawtext=text='LES SENTINELLES':x=(w-text_w)/2:y=45:fontsize=54:fontcolor=white"
                cmd=["ffmpeg","-y","-ss",str(c["start"]),"-i",c["file"],"-t",str(c["duration"]),"-vf",vf,
                     "-c:v","libx264","-preset","veryfast","-crf","22","-c:a","aac","-b:a","160k",str(out)]
                subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                report["exports"].append({"file":str(out),"source":c["file"],"start":c["start"],"duration":c["duration"]})

            copy=f"{self.event.get()} | Les Sentinelles | Hockey des Forces de l'Ordre | {self.sponsor.get()}".strip()
            (run_dir/"publication_proposee.txt").write_text(
                "Titre proposé : "+self.event.get()+" | Les Sentinelles\n\nDescription : "+copy+
                "\n\n#LesSentinelles #Hockey #ForcesDeLOrdre\n",encoding="utf-8")
            (run_dir/"rapport.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
            self.status.set(f"Terminé : {len(report['exports'])} Shorts prêts à valider")
            messagebox.showinfo("Terminé",f"{len(report['exports'])} Shorts générés dans\n{run_dir}\n\nVérifie-les avant publication.")
        except Exception as e:
            self.status.set("Erreur"); messagebox.showerror("Erreur",str(e))
        finally:
            self.progress.stop()

    def open_exports(self):
        p=str(self.output.resolve())
        if os.name=='nt': os.startfile(p)
        elif shutil.which('xdg-open'): subprocess.Popen(['xdg-open',p])
        else: messagebox.showinfo("Exports",p)

if __name__=='__main__': App().mainloop()
