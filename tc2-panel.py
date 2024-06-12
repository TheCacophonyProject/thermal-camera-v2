# flatpak run --command=bash org.kicad.KiCad


from kikit import panelize
from kikit import panelize_ui_impl as ki
from kikit.units import mm, deg
from kikit.panelize import Panel, BasicGridPosition, Origin
from pcbnewTransition.pcbnew import LoadBoard, VECTOR2I
from pcbnewTransition import pcbnew
from itertools import chain
from kikit.units import mm
import os

from shapely.geometry import Polygon

# Custom config
main_board_path = "tc2-main-pcb/tc2-main-pcb.kicad_pcb"
plugs_board_path = "tc2-plugs-buck-boost-pcb/tc2-plugs-buck-boost-pcb.kicad_pcb"
output_path = "tc2-panel/tc2-panel.kicad_pcb"
os.makedirs("tc2-panel", exist_ok=True)

board_spacing = 3*mm

## Check kikit cli for defaults https://yaqwsx.github.io/KiKit/latest/panelization/cli/
framing={
    "type": "frame",        # One of none, railstb (top/bottom), railslr (left/right), frame, tightframe
    "vspace": "2.5mm",     # Min of 2mm for PCBA at JLCPCB
    "hspace": "2.5mm",     # Min of 2mm for PCBA at JLCPCB
    "width": "5mm",         # Min width of 5mm for PCBA at JLCPCB
}
cuts =  {
    "type": "mousebites",
    "drill": "0.6mm",       # Minimum mouse bite holes
    "spacing": "0.9mm",     # Minimum mouse bite spacing (0.3mm between holes)
    "offset": "-0.12mm",     # Offset of mouse bite holes into the mouse bite. -0.12mm gives enough clearance for traces/copper on the edge of the PCB for the DRM.
}
tabs = {
    "type":"annotation",    # Use annotations in the PCBs for the placement of the tabs.
    "fillet": "1mm",        # Required for manufacturability of the tabs.
    "tabfootprints": "kikit:Tab8"       # need to manually to the library as this config doesn't seam to work .var/app/org.kicad.KiCad/data/python/lib/python3.11/site-packages/kikit/annotations.py
}
tooling = {
    "type": "4hole",
    "hoffset": "3mm",
    "voffset": "3mm",
    "size": "2mm",          # JLCPCB requires  2mm tooling holes
}
fiducials = {
    "type": "4fid",
    "hoffset": "3.85mm",    # JLCPCB requires fids 3.85mm from edge
    "voffset": "6mm",
}
post = {
     "millradius": "1mm"    # Will add fillets when needed for manufacturability.
}
copperfill = {
    "type": "solid",        # Sometimes needed for manufacturability (lower than 30% copper fill can increase min trace width)
    "layers": "all",
}

preset = ki.obtainPreset([], 
    tabs=tabs, 
    cuts=cuts, 
    framing=framing, 
    tooling=tooling, 
    post=post, 
    fiducials=fiducials, 
    copperfill=copperfill,
    )

board1 = LoadBoard(main_board_path)
board2 = LoadBoard(plugs_board_path)
panel = Panel(output_path)

# Inherit settings from board1
panel.inheritDesignSettings(board2)
panel.inheritProperties(board2)
panel.inheritTitleBlock(board2)

### Build layout of boards for panel.
# Get source areas for the boards.
sourceArea1 = ki.readSourceArea(preset["source"], board1)
sourceArea2 = ki.readSourceArea(preset["source"], board2)

# Prepare renaming nets and references.
mainNetRefRenamer = lambda x, orig: "main-{orig}".format(n=x, orig=orig)
plugsNetRefRenamer = lambda x, orig: "plugs-{orig}".format(n=x, orig=orig)

# Place the boards in the panel. The origin is the center of each board.
# If needing to rotate a board you can add `rotationAngle=deg*90` as a parameter.
panel.appendBoard(
    main_board_path, 
    pcbnew.wxPointMM(0, 0), 
    sourceArea=sourceArea1, 
    netRenamer=mainNetRefRenamer, 
    refRenamer=mainNetRefRenamer, 
    bufferOutline=100000,
    inheritDrc=False,
)
panel.appendBoard(
    plugs_board_path, 
    pcbnew.wxPointMM(4, -50), 
    sourceArea=sourceArea2, 
    netRenamer=plugsNetRefRenamer, 
    refRenamer=plugsNetRefRenamer,  
    inheritDrc=True,
)
# Add mill fillets
panel.addMillFillets(panelize.fromMm(0.75))


# Build frame
ki.buildFraming(preset, panel)
framingSubstrates = ki.dummyFramingSubstrate(panel.substrates, preset)

# Add substrate on left edge for attaching tabs to. Otherwise the tabs are too far from the edge and won't be created.
x1 = -40*mm
y1 = -55.75*mm
x2 = -33*mm
y2 = 5*mm
substrate = Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
panel.appendSubstrate(substrate)

# safeMargin set to true helps to force building tabs when they won't reach the frame.
# If this is the case then you want to add substrates to the panel with Polygon as was done above.
panel.buildPartitionLineFromBB(framingSubstrates, safeMargin=True) 

backboneCuts = ki.buildBackBone(preset["layout"], panel, panel.substrates, preset)

# Debug to help visualize the layout and as to why some tabs might not be created
#panel.debugRenderPartitionLines()
#panel.debugRenderBoundingBoxes()

# Panelize things..
ki.buildTooling(preset, panel)
ki.buildFiducials(preset, panel)

tabCuts = ki.buildTabs(preset, panel, panel.substrates, framingSubstrates)
ki.makeTabCuts(preset, panel, tabCuts)
frameCuts = ki.buildFraming(preset, panel)
ki.makeOtherCuts(preset, panel, chain(backboneCuts, frameCuts))
ki.buildPostprocessing(preset["post"], panel)
ki.buildCopperfill(preset["copperfill"], panel)

panel.save()
