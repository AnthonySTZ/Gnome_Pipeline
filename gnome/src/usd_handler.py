import os
from pxr import Usd, UsdGeom, Sdf


def create_new_stage(path: str, name: str) -> tuple[Usd.Stage, str]:
    """Create a new USD stage with the given path and name"""

    os.makedirs(path, exist_ok=True)
    if not (
        name.endswith(".usd") or name.endswith(".usda") or name.endswith(".usdc")
    ):  # Check if the name already ends with ".usd" like format
        name += ".usda"
    path = os.path.join(path, name)
    stage: Usd.Stage = Usd.Stage.CreateNew(path)
    return stage, path


def save_stage(stage: Usd.Stage) -> None:
    """Save the USD stage"""
    stage.GetRootLayer().Save()


def add_layer(root_layer: Sdf.Layer, sub_layer_path: str) -> Sdf.Layer:
    """Add a new root layer to the USD stage"""
    sub_layer: Sdf.Layer = Sdf.Layer.FindOrOpen(sub_layer_path)
    if not sub_layer:  # If the layer doesn't exist, then create it
        sub_layer: Sdf.Layer = Sdf.Layer.CreateNew(sub_layer_path)
    root_layer.subLayerPaths.append(
        sub_layer.identifier
    )  # Append the sublayer to the root_layer
    return sub_layer
