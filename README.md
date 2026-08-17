# thermal-camera-v2

## Running tc2-panel.py (KiKit)

`tc2-panel.py` uses [KiKit](https://yaqwsx.github.io/KiKit/) to build the manufacturing panel from the individual board files.

```sh
# Create a venv that inherits the system site-packages (needed for pcbnew)
python3 -m venv --system-site-packages ~/.venvs/kikit
source ~/.venvs/kikit/bin/activate

# Install kikit and the other packages tc2-panel.py needs.
# pcbnewTransition is pinned >=0.5 because older versions assume a pre-KiCad-6
# pcbnew API (e.g. DRAWSEGMENT) and crash against current KiCad.
pip install kikit shapely "pcbnewTransition>=0.5"
```

Once the venv exists, running the panel script again only needs:

```sh
source ~/.venvs/kikit/bin/activate
cd /path/to/thermal-camera-v2
python3 tc2-panel.py
```
