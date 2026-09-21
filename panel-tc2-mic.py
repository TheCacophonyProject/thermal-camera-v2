import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser(description="Generate the tc2-mic panel.")
_ = parser.add_argument(
    "--production",
    action="store_true",
    help="Render V-cuts on Edge.Cuts for the production Gerbers. " +
         "By default they stay on KiKit's default layer (Cmts.User) so DRC passes.",
)
args = parser.parse_args()

dir_path = "./.generated-pcbs/tc2-mic-panel"

shutil.rmtree(dir_path, ignore_errors=True)
os.makedirs(dir_path, exist_ok=True)

cuts = "vcuts; layer: Edge.Cuts" if args.production else "vcuts"

command = [
    "kikit", "panelize",
    "--layout", "grid; rows: 5; cols: 2; alternation: cols; hspace: 0mm; vspace: 0mm; renameref: {orig}-{n}",
    "--tabs", "annotation",
    "--cuts", cuts,
    "--post", "millradius: 1mm",
    "--framing", "frame; cuts: both",
    "--fiducials", "type: 4fid; hoffset: 3.85mm; voffset:6mm",
    "--tooling", "type: 4hole; hoffset: 3mm; voffset: 3mm; size: 2mm",
    "tc2-mic-pcb/tc2-mic-pcb.kicad_pcb",
    f"{dir_path}/tc2-mic-panel.kicad_pcb"
]

# Run the command
_ = subprocess.run(command, check=False)

# Set footprint library file
library_str = """(fp_lib_table
    (version 7)
    (lib (name "cacophony-library") (type "KiCad") (uri "${KIPRJMOD}/../../kicad-library/cacophony-library.pretty") (options "") (descr ""))
)
"""
with open(f"{dir_path}/fp-lib-table", "w") as f:
    _ = f.write(library_str)

print("Done")