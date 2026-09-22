import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser(description="Generate the tc2-usb-pi3 panel.")
_ = parser.add_argument(
    "--production",
    action="store_true",
    help="Render V-cuts on Edge.Cuts for the production Gerbers. " +
         "By default they stay on KiKit's default layer (Cmts.User) so DRC passes.",
)
args = parser.parse_args()

dir_path = "./.generated-pcbs/tc2-sim-usb-pi3-panel"

shutil.rmtree(dir_path, ignore_errors=True)
os.makedirs(dir_path, exist_ok=True)

cuts = "mousebites;" # layer: Edge.Cuts" if args.production else "vcuts"

command = [
    "kikit", "panelize",
    "--layout", "grid; rows: 4; cols: 4; alternation: cols; hspace: 3mm; vspace: 3mm; renameref: {orig}-{n}; rotation: 180deg; vbackbone: 5mm; vboneskip: 1",
    "--tabs", "annotation",
    "--cuts", cuts,
    "--post", "millradius: 1mm",
    "--framing", "frame; cuts: both",
    "--fiducials", "type: 4fid; hoffset: 3.85mm; voffset:6mm",
    "--tooling", "type: 4hole; hoffset: 3mm; voffset: 3mm; size: 2mm",
    "tc2-sim-usb-pi3-pcb/tc2-sim-usb-pi3-pcb.kicad_pcb",
    f"{dir_path}/tc2-sim-usb-pi3-panel.kicad_pcb"
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