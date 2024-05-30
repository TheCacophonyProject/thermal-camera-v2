from kikit import panelize
from kikit import panelize_ui_impl as ki
from kikit.units import mm, deg
from kikit.panelize import Panel, BasicGridPosition, Origin
from pcbnewTransition.pcbnew import LoadBoard, VECTOR2I
from pcbnewTransition import pcbnew
from itertools import chain
from kikit.units import mm

from shapely.geometry import Polygon

# Custom config
board1_path = "tc2-main-pcb/tc2-main-pcb.kicad_pcb"
board2_path = "tc2-plugs-buck-boost-pcb/tc2-plugs-buck-boost-pcb.kicad_pcb"
output_path = "tc2-panelized/tc2-panelized.kicad_pcb"

board_spacing = 3*mm

## Check kikit cli for defaults https://yaqwsx.github.io/KiKit/latest/panelization/cli/
framing={
    "type": "frame",
    "vspace" : "3mm",
    "hspace" : "3mm",
    "width": "6mm",
}
cuts =  {
    "type": "mousebites",
    "drill": "0.5mm",
    "spacing": "0.75mm",
    "offset": "-0.1mm",
    "layer": "F.Cu"
}
tabs = {
    "type":"annotation",
    "fillet": "1.5mm",
}
tooling = {
    "type": "3hole",
    "hoffset": "3mm",
    "voffset": "3mm",
    "size": "3mm",
}
fiducials = {
    "type": "3fid",
    "hoffset": "3mm",
    "voffset": "6mm",
}
post = {
     "millradius": "1.5mm" # Will add fillets when needed for manufacturing.
}

preset = ki.obtainPreset([], tabs=tabs, cuts=cuts, framing=framing, tooling=tooling, post=post, fiducials=fiducials)

board1 = LoadBoard(board1_path)
board2 = LoadBoard(board2_path)
panel = Panel(output_path)

# Add substrate on left edge for attaching tabs to. Otherwise the tabs are too far from the edge and won't be created.
x1 = -40*mm
y1 = -55.75*mm
x2 = -33*mm
y2 = 5*mm
substrate = Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
panel.appendSubstrate(substrate)

# Inherit settings from board1
panel.inheritDesignSettings(board2)
panel.inheritProperties(board2)
panel.inheritTitleBlock(board2)

### Build layout of boards for panel.
# Get source areas for the boards.
sourceArea1 = ki.readSourceArea(preset["source"], board1)
sourceArea2 = ki.readSourceArea(preset["source"], board2)

# Prepare renaming nets and references.
netRenamer = lambda x, y: "Board_{n}-{orig}".format(n=x, orig=y)
refRenamer = lambda x, y: "Board_{n}-{orig}".format(n=x, orig=y)

# Place the boards in the panel. The origin is the center of each board.
# If needing to rotate a board you can add `rotationAngle=deg*90` as a parameter.
panel.appendBoard(
    board1_path, 
    pcbnew.wxPointMM(0, 0), 
    sourceArea=sourceArea1, 
    netRenamer=netRenamer, 
    refRenamer=refRenamer, 
    bufferOutline=100000
)
panel.appendBoard(
    board2_path, 
    pcbnew.wxPointMM(4, -51.5), 
    sourceArea=sourceArea2, 
    netRenamer=netRenamer, 
    refRenamer=refRenamer,  
    inheritDrc=False
)
# Add mill fillets
panel.addMillFillets(panelize.fromMm(0.75))


# Build frame
ki.buildFraming(preset, panel)
framingSubstrates = ki.dummyFramingSubstrate(panel.substrates, preset)
panel.buildPartitionLineFromBB(framingSubstrates, safeMargin=True) # safeMargin set to true helps to force building tabs
backboneCuts = ki.buildBackBone(preset["layout"], panel, panel.substrates, preset)

# Debug to help visualize the layout and as to why some tabs might not be created
#panel.debugRenderPartitionLines()
#panel.debugRenderBoundingBoxes()

# Panelize things..
#ki.buildTooling(preset, panel)
#ki.buildFiducials(preset, panel)

tabCuts = ki.buildTabs(preset, panel, panel.substrates, framingSubstrates)
ki.makeTabCuts(preset, panel, tabCuts)
frameCuts = ki.buildFraming(preset, panel)
ki.makeOtherCuts(preset, panel, chain(backboneCuts, frameCuts))
ki.buildPostprocessing(preset["post"], panel)
ki.buildCopperfill(preset["copperfill"], panel)

panel.save(reconstructArcs=preset["post"]["reconstructarcs"],
    refillAllZones=preset["post"]["refillzones"])
