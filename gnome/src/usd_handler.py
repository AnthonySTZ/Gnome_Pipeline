import os
from pxr import Usd, UsdGeom


def create_new_stage(path: str, name: str) -> Usd.Stage:
    """Create a new USD stage with the given path and name"""

    os.makedirs(path, exist_ok=True)
    if not (name.endswith(".usd") or name.endswith(".usda") or name.endswith(".usdc")):
        name += ".usda"
    stage: Usd.Stage = Usd.Stage.CreateNew(os.path.join(path, name))
    return stage
