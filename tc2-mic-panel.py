import subprocess
import os

dir_path = "./generated-pcbs/tc2-mic-panel"

os.makedirs(dir_path, exist_ok=True)

command = [
    "kikit", "panelize",
    "--layout", "grid; rows: 5; cols: 2; space: 3mm; renameref: {orig}-{n}",
    "--tabs", "annotation",
    "--cuts", "vcuts; offset: -0.1mm",
    "--post", "millradius: 1mm",
    "--framing", "frame",
    "--fiducials", "type: 4fid; hoffset: 3.85mm; voffset:6mm",
    "--tooling", "type: 4hole; hoffset: 3mm; voffset: 3mm; size: 2mm",
    "--copperfill", "type: solid; layers: all",
    "tc2-mic-pcb/tc2-mic-pcb.kicad_pcb",
    f"{dir_path}/tc2-mic-panel.kicad_pcb"
]

# Run the command
subprocess.run(command)
