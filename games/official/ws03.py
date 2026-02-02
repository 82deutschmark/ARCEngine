# Author: Claude Opus 4.5
# Date: 2026-02-01
# PURPOSE: WS03 game - variant of LS20/WS02 with jarring color palette and permanent fog of war
# Features: Pink/Red/Yellow/Orange/Purple clashing colors, always-on fog of war, extra energy pickups
# SRP/DRY check: Pass - Reuses proven game mechanics from LS20/WS01/WS02

import logging
from typing import List
import numpy as np
from arcengine import ARCBaseGame, Camera, Level, Sprite

# WS03 uses jarring clashing colors: Pink (6), Red (8), Yellow (11), Orange (12), Purple (15), Green (14)
sprites = {
    "dcb": Sprite(pixels=[[-1, 6, -1], [6, 6, -1], [-1, 6, 6]], name="dcb", visible=True, collidable=True, layer=1),
    "fij": Sprite(pixels=[[6, 6, 6], [-1, -1, 6], [6, -1, 6]], name="fij", visible=True, collidable=False, layer=-2),
    "ggk": Sprite(pixels=[[5, 5, 5, 5, 5, 5, 5], [5, -1, -1, -1, -1, -1, 5], [5, -1, -1, -1, -1, -1, 5], [5, -1, -1, -1, -1, -1, 5], [5, -1, -1, -1, -1, -1, 5], [5, -1, -1, -1, -1, -1, 5], [5, 5, 5, 5, 5, 5, 5]], name="ggk", visible=True, collidable=True, tags=["yar", "vdr"], layer=-3),
    "hep": Sprite(pixels=[[5]*10]*10, name="hep", visible=True, collidable=True, tags=["nfq"], layer=1),
    "hul": Sprite(pixels=[[13, 13, -1, -1, -1, -1, -1, 13, 13], [13]*9, [13]*9, [13]*9, [13]*9, [13]*9, [13]*9, [13]*9, [13]*9], name="hul", visible=True, collidable=True, layer=-4),
    "kdj": Sprite(pixels=[[6, -1, 6], [-1, 6, -1], [6, -1, 6]], name="kdj", visible=True, collidable=True, tags=["wex"], layer=10),
    "kdy": Sprite(pixels=[[-2]*5, [-2, -2, 6, -2, -2], [-2, 1, 6, 6, -2], [-2, -2, 1, -2, -2], [-2]*5], name="kdy", visible=True, collidable=True, tags=["bgt"], layer=-1),
    "krg": Sprite(pixels=[[8]], name="krg", visible=True, collidable=True, layer=3),
    "lhs": Sprite(pixels=[[5]*5]*5, name="lhs", visible=True, collidable=False, tags=["mae"], layer=-3),
    "lyd": Sprite(pixels=[[-1, 6, -1], [-1, 6, -1], [6, 6, 6]], name="lyd", visible=True, collidable=True),
    "mgu": Sprite(pixels=[[5, 5, 5, 5] + [-1]*60]*24 + [[4]*12 + [-1]*52, [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4] + [-1]*52]*7 + [[4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4] + [5]*52]*3 + [[4]*12 + [5]*52], name="mgu", visible=True, collidable=True),
    "nio": Sprite(pixels=[[-1, 6, 6], [6, -1, 6], [-1, 6, -1]], name="nio", visible=True, collidable=True),
    "nlo": Sprite(pixels=[[4]*5]*5, name="nlo", visible=True, collidable=True, tags=["jdd"], layer=-5),
    "opw": Sprite(pixels=[[6, 6, -1], [-1, 6, 6], [6, -1, 6]], name="opw", visible=True, collidable=True),
    "pca": Sprite(pixels=[[12]*5, [12]*5, [15]*5, [15]*5, [15]*5], name="pca", visible=True, collidable=True, tags=["caf"]),
    "qqv": Sprite(pixels=[[-2]*5, [-2, 15, 8, 8, -2], [-2, 15, 6, 11, -2], [-2, 12, 12, 11, -2], [-2]*5], name="qqv", visible=True, collidable=False, tags=["gic"], layer=-1),
    "rzt": Sprite(pixels=[[6, -1, -1], [-1, 6, -1], [-1, -1, 6]], name="rzt", visible=True, collidable=True, tags=["axa"]),
    "snw": Sprite(pixels=[[5]*7, [5, -1, -1, -1, -1, -1, 5], [5, -1, -1, -1, -1, -1, 5], [5, -1, -1, -1, -1, -1, 5], [5, -1, -1, -1, -1, -1, 5], [5, -1, -1, -1, -1, -1, 5], [5]*7], name="snw", visible=True, collidable=True, tags=["yar"], layer=-3),
    "tmx": Sprite(pixels=[[6, -1, 6], [6, -1, 6], [6, 6, 6]], name="tmx", visible=True, collidable=True),
    "tuv": Sprite(pixels=[[6]*10] + [[6] + [-1]*8 + [6]]*8 + [[6]*10], name="tuv", visible=False, collidable=True, tags=["fng"], layer=5),
    "ulq": Sprite(pixels=[[6]*7] + [[6] + [-1]*5 + [6]]*5 + [[6]*7], name="ulq", visible=False, collidable=True, tags=["qex"], layer=-1),
    "vxy": Sprite(pixels=[[-2]*5, [-2, 6, -2, -2, -2], [-2, -2, 6, 6, -2], [-2, -2, 6, -2, -2], [-2]*5], name="vxy", visible=True, collidable=False, tags=["gsu"], layer=-1),
    "zba": Sprite(pixels=[[11, 11, 11], [11, -1, 11], [11, 11, 11]], name="zba", visible=True, collidable=False, tags=["iri"], layer=-1),
}

levels = [
    # Level 1: krg - Tutorial level, 0 base energy + 2 fog compensation
    Level(
        sprites=[
            sprites["hep"].clone().set_position(1, 53), sprites["hul"].clone().set_position(32, 8).set_rotation(180),
            sprites["kdj"].clone().set_position(3, 55).set_scale(2), sprites["kdy"].clone().set_position(19, 30),
            sprites["lhs"].clone().set_position(34, 10), sprites["mgu"].clone(),
        ] + [sprites["nlo"].clone().set_position(x, y) for x, y in [(4,0),(9,0),(4,5),(14,0),(19,0),(24,0),(29,0),(39,0),(44,0),(49,0),(54,0),(59,0),(4,10),(4,15),(4,20),(4,25),(59,15),(59,20),(59,25),(59,30),(59,35),(59,40),(59,45),(59,50),(59,55),(54,55),(49,55),(44,55),(39,55),(34,55),(29,55),(24,55),(19,55),(4,40),(4,45),(4,50),(9,50),(4,55),(9,55),(14,55),(54,25),(54,20),(34,0),(59,10),(59,5),(54,15),(54,10),(44,5),(39,5),(34,5),(29,5),(54,50),(54,45),(24,5),(19,5),(9,35),(9,45),(19,50),(9,40),(49,5),(54,5),(49,50),(14,50),(14,5),(9,5),(9,30),(9,25),(9,20),(9,15),(9,10),(49,10),(44,20),(39,10),(44,10),(49,15),(29,10),(29,15),(39,15),(44,15),(49,20),(14,15),(19,15),(24,15),(24,10),(19,10),(14,10),(29,20),(39,20),(24,20),(29,40),(19,20),(14,20),(54,30),(24,40),(14,45),(29,35),(4,30),(4,35),(54,35),(54,40),(14,40),(24,50),(29,50),(39,50),(44,50),(34,50),(29,30)]] + [
            sprites["pca"].clone().set_position(39, 45), sprites["rzt"].clone().set_position(35, 11),
            sprites["snw"].clone().set_position(33, 9), sprites["tuv"].clone().set_position(1, 53),
            sprites["ulq"].clone().set_position(33, 9),
            # Fog compensation: 2 pickups near start and mid-path
            sprites["zba"].clone().set_position(15, 16),
            sprites["zba"].clone().set_position(30, 26),
        ],
        grid_size=(64, 64),
        data={"vxy": 42, "tuv": 5, "nlo": 9, "opw": 0, "qqv": 5, "ggk": 9, "fij": 270, "kdy": True},
        name="krg",
    ),
    # Level 2: mgu - 2 base energy + 2 fog compensation = 4 total
    Level(
        sprites=[
            sprites["hep"].clone().set_position(1, 53), sprites["hul"].clone().set_position(12, 38),
            sprites["kdj"].clone().set_position(3, 55).set_scale(2), sprites["kdy"].clone().set_position(49, 45),
            sprites["lhs"].clone().set_position(14, 40), sprites["mgu"].clone(),
        ] + [sprites["nlo"].clone().set_position(x, y) for x, y in [(4,0),(9,0),(4,5),(14,0),(19,0),(24,0),(29,0),(39,0),(44,0),(49,0),(54,0),(59,0),(4,10),(4,15),(4,20),(4,25),(4,30),(4,35),(59,15),(59,20),(59,25),(59,30),(59,35),(59,40),(59,45),(59,50),(59,55),(54,55),(49,55),(44,55),(39,55),(34,55),(29,55),(24,55),(19,55),(4,40),(4,45),(4,50),(9,50),(4,55),(9,55),(14,55),(54,30),(34,0),(59,10),(59,5),(54,15),(54,10),(9,35),(9,45),(19,50),(9,40),(54,5),(14,45),(14,50),(9,5),(9,30),(9,25),(19,30),(24,30),(19,40),(19,45),(19,35),(39,15),(39,35),(44,30),(34,45),(14,5),(39,20),(44,20),(24,20),(44,25),(39,40),(39,45),(24,35),(24,25),(24,50),(19,25),(24,40),(24,45),(29,45),(29,30),(29,25),(24,15),(44,35),(54,34)]] + [
            sprites["pca"].clone().set_position(29, 40), sprites["rzt"].clone().set_position(15, 41),
            sprites["snw"].clone().set_position(13, 39), sprites["tuv"].clone().set_position(1, 53),
            sprites["ulq"].clone().set_position(13, 39),
            # LS20 base energy
            sprites["zba"].clone().set_position(15, 16),
            sprites["zba"].clone().set_position(30, 51),
            # Fog compensation: 2 pickups near decision points
            sprites["zba"].clone().set_position(45, 26),
            sprites["zba"].clone().set_position(20, 36),
        ],
        grid_size=(64, 64),
        data={"vxy": 42, "tuv": 5, "nlo": 9, "opw": 270, "qqv": 5, "ggk": 9, "fij": 0, "kdy": True},
        name="mgu",
    ),
    # Level 3: puq - 3 base energy + 2 fog compensation = 5 total
    Level(
        sprites=[
            sprites["hep"].clone().set_position(1, 53), sprites["hul"].clone().set_position(52, 48),
            sprites["kdj"].clone().set_position(3, 55).set_scale(2), sprites["kdy"].clone().set_position(49, 10),
            sprites["lhs"].clone().set_position(54, 50), sprites["mgu"].clone(),
        ] + [sprites["nlo"].clone().set_position(x, y) for x, y in [(4,0),(9,0),(4,5),(14,0),(19,0),(24,0),(29,0),(39,0),(44,0),(49,0),(54,0),(59,0),(4,10),(4,15),(4,20),(4,25),(4,30),(4,35),(59,15),(59,20),(59,25),(59,30),(59,35),(59,40),(59,45),(59,50),(59,55),(54,55),(49,55),(44,55),(39,55),(34,55),(29,55),(24,55),(19,55),(4,40),(4,45),(4,50),(9,50),(4,55),(9,55),(14,55),(34,0),(59,10),(59,5),(39,10),(14,25),(19,40),(19,45),(19,35),(49,50),(39,35),(39,40),(39,45),(14,30),(49,45),(49,40),(14,20),(14,50),(39,5),(39,50),(44,45),(19,50),(44,40),(44,50),(44,20),(49,20),(39,20),(19,10),(14,35),(39,15),(34,35),(14,10),(14,15),(44,35),(24,35),(34,10),(24,10)]] + [
            sprites["pca"].clone().set_position(9, 45), sprites["qqv"].clone().set_position(29, 45),
            sprites["rzt"].clone().set_position(55, 51), sprites["snw"].clone().set_position(53, 49),
            sprites["tuv"].clone().set_position(1, 53), sprites["ulq"].clone().set_position(53, 49),
            # LS20 base energy
            sprites["zba"].clone().set_position(20, 31),
            sprites["zba"].clone().set_position(35, 6),
            sprites["zba"].clone().set_position(50, 36),
            # Fog compensation: 2 pickups near corridors
            sprites["zba"].clone().set_position(15, 16),
            sprites["zba"].clone().set_position(45, 21),
        ],
        grid_size=(64, 64),
        data={"vxy": 42, "tuv": 5, "nlo": 9, "opw": 270, "qqv": 5, "ggk": 12, "fij": 0, "kdy": True},
        name="puq",
    ),
    # Level 4: tmx - 4 base energy + 2 fog compensation = 6 total
    Level(
        sprites=[
            sprites["hep"].clone().set_position(1, 53), sprites["hul"].clone().set_position(7, 3).set_rotation(90),
            sprites["kdj"].clone().set_position(3, 55).set_scale(2),
            sprites["lhs"].clone().set_position(9, 5), sprites["mgu"].clone(),
        ] + [sprites["nlo"].clone().set_position(x, y) for x, y in [(4,0),(9,0),(4,5),(14,0),(19,0),(24,0),(29,0),(39,0),(44,0),(49,0),(54,0),(59,0),(4,10),(4,15),(4,20),(4,25),(4,30),(4,35),(59,15),(59,20),(59,25),(59,30),(59,35),(59,40),(59,45),(59,50),(59,55),(54,55),(49,55),(44,55),(39,55),(34,55),(29,55),(24,55),(19,55),(4,40),(4,45),(4,50),(9,50),(4,55),(9,55),(14,55),(34,0),(59,10),(59,5),(19,30),(14,10),(9,10),(24,25),(29,30),(19,10),(29,5),(9,20),(14,15),(29,25),(29,35),(34,35),(19,50),(39,50),(39,30),(49,35),(9,15),(49,10),(49,15),(44,10),(29,40),(29,20),(39,45),(44,50),(19,25),(39,35),(14,50),(9,45)]] + [
            sprites["pca"].clone().set_position(54, 5), sprites["qqv"].clone().set_position(34, 30),
            sprites["rzt"].clone().set_position(10, 6), sprites["snw"].clone().set_position(8, 4),
            sprites["tuv"].clone().set_position(1, 53), sprites["ulq"].clone().set_position(8, 4),
            sprites["vxy"].clone().set_position(24, 30),
            # LS20 base energy
            sprites["zba"].clone().set_position(35, 41),
            sprites["zba"].clone().set_position(15, 46),
            sprites["zba"].clone().set_position(25, 21),
            sprites["zba"].clone().set_position(55, 51),
            # Fog compensation: 2 pickups near start and mid-map
            sprites["zba"].clone().set_position(20, 16),
            sprites["zba"].clone().set_position(45, 26),
        ],
        grid_size=(64, 64),
        data={"vxy": 42, "tuv": 5, "nlo": 9, "opw": 0, "qqv": 4, "ggk": 14, "fij": 0, "kdy": True},
        name="tmx",
    ),
    # Level 5: zba - 3 base energy + 2 fog compensation = 5 total
    Level(
        sprites=[
            sprites["hep"].clone().set_position(1, 53), sprites["hul"].clone().set_position(52, 3).set_rotation(180),
            sprites["kdj"].clone().set_position(3, 55).set_scale(2), sprites["kdy"].clone().set_position(19, 40),
            sprites["lhs"].clone().set_position(54, 5), sprites["mgu"].clone(),
        ] + [sprites["nlo"].clone().set_position(x, y) for x, y in [(4,0),(9,0),(4,5),(14,0),(19,0),(24,0),(29,0),(39,0),(44,0),(49,0),(54,0),(59,0),(4,10),(4,15),(4,20),(4,25),(4,30),(4,35),(59,15),(59,20),(59,25),(59,30),(59,35),(59,40),(59,45),(59,50),(59,55),(54,55),(49,55),(44,55),(39,55),(34,55),(29,55),(24,55),(19,55),(4,40),(4,45),(4,50),(9,50),(4,55),(9,55),(14,55),(34,0),(59,10),(59,5),(29,30),(29,35),(49,10),(49,5),(29,15),(29,20),(24,25),(19,25),(49,15),(24,30),(24,20),(34,20),(34,30),(49,35),(49,40),(49,45),(49,50),(44,50),(44,5),(14,25),(49,20),(49,30),(14,50),(9,45)]] + [
            sprites["pca"].clone().set_position(54, 50), sprites["qqv"].clone().set_position(29, 25),
            sprites["rzt"].clone().set_position(55, 6), sprites["snw"].clone().set_position(53, 4),
            sprites["tuv"].clone().set_position(1, 53), sprites["ulq"].clone().set_position(53, 4),
            sprites["vxy"].clone().set_position(19, 10),
            # LS20 base energy
            sprites["zba"].clone().set_position(40, 6),
            sprites["zba"].clone().set_position(10, 6),
            sprites["zba"].clone().set_position(40, 51),
            # Fog compensation: 2 pickups along traversal path
            sprites["zba"].clone().set_position(20, 26),
            sprites["zba"].clone().set_position(35, 36),
        ],
        grid_size=(64, 64),
        data={"vxy": 42, "tuv": 5, "nlo": 9, "opw": 90, "qqv": 4, "ggk": 12, "fij": 0, "kdy": True},
        name="zba",
    ),
    # Level 6: lyd - 5 base energy + 2 fog compensation = 7 total (dual targets)
    Level(
        sprites=[
            sprites["ggk"].clone().set_position(53, 34),
            sprites["hep"].clone().set_position(1, 53), sprites["hul"].clone().set_position(52, 48),
            sprites["hul"].clone().set_position(52, 33),
            sprites["kdj"].clone().set_position(3, 55).set_scale(2), sprites["kdy"].clone().set_position(19, 25),
            sprites["lhs"].clone().set_position(54, 50), sprites["lhs"].clone().set_position(54, 35),
            sprites["mgu"].clone(),
        ] + [sprites["nlo"].clone().set_position(x, y) for x, y in [(4,0),(9,0),(4,5),(14,0),(19,0),(24,0),(29,0),(39,0),(44,0),(49,0),(54,0),(59,0),(4,10),(4,15),(4,20),(4,25),(4,30),(4,35),(59,15),(59,20),(59,25),(59,30),(59,35),(59,40),(59,45),(59,50),(59,55),(54,55),(49,55),(44,55),(39,55),(34,55),(29,55),(24,55),(19,55),(4,40),(4,45),(4,50),(9,50),(4,55),(9,55),(14,55),(34,0),(59,10),(59,5),(29,30),(54,10),(24,30),(34,30),(49,35),(49,40),(49,45),(49,50),(44,50),(49,30),(54,5),(44,45),(39,50),(44,40),(34,50),(39,45),(49,25),(19,10),(14,30),(44,30),(49,5),(24,10),(34,25),(19,30),(34,15),(29,10),(9,45),(14,50),(14,25),(44,35),(14,15),(34,10),(14,10)]] + [
            sprites["pca"].clone().set_position(24, 50), sprites["qqv"].clone().set_position(24, 25),
            sprites["rzt"].clone().set_position(55, 51), sprites["rzt"].clone().set_position(55, 36),
            sprites["snw"].clone().set_position(53, 49), sprites["tuv"].clone().set_position(1, 53),
            sprites["ulq"].clone().set_position(53, 34), sprites["ulq"].clone().set_position(53, 49),
            sprites["vxy"].clone().set_position(29, 25),
            # LS20 base energy
            sprites["zba"].clone().set_position(45, 26),
            sprites["zba"].clone().set_position(10, 41),
            sprites["zba"].clone().set_position(55, 16),
            sprites["zba"].clone().set_position(45, 6),
            sprites["zba"].clone().set_position(20, 16),
            # Fog compensation: 2 pickups near dual targets
            sprites["zba"].clone().set_position(35, 46),
            sprites["zba"].clone().set_position(15, 31),
        ],
        grid_size=(64, 64),
        data={"vxy": 42, "tuv": [5, 0], "nlo": [9, 8], "opw": [90, 90], "qqv": 0, "ggk": 14, "fij": 0, "kdy": True},
        name="lyd",
    ),
    # Level 7: fij - 6 base energy, no fog compensation (originally had fog)
    Level(
        sprites=[
            sprites["hep"].clone().set_position(1, 53), sprites["hul"].clone().set_position(27, 48),
            sprites["kdj"].clone().set_position(3, 55).set_scale(2), sprites["kdy"].clone().set_position(54, 20),
            sprites["lhs"].clone().set_position(29, 50), sprites["mgu"].clone(),
        ] + [sprites["nlo"].clone().set_position(x, y) for x, y in [(4,0),(9,0),(4,5),(14,0),(19,0),(24,0),(29,0),(39,0),(44,0),(49,0),(54,0),(59,0),(4,10),(4,15),(4,20),(4,25),(4,30),(4,35),(59,15),(59,20),(59,25),(59,30),(59,35),(59,40),(59,45),(59,50),(59,55),(54,55),(49,55),(44,55),(39,55),(34,55),(29,55),(24,55),(19,55),(4,40),(4,45),(4,50),(9,50),(4,55),(9,55),(14,55),(34,0),(59,10),(59,5),(24,40),(49,10),(49,5),(39,20),(29,20),(24,25),(49,15),(24,20),(34,20),(39,45),(34,40),(24,45),(34,45),(24,50),(34,50),(49,20),(39,40),(54,40),(19,50),(24,35),(39,50),(44,20),(9,45),(14,50),(19,45)]] + [
            sprites["pca"].clone().set_position(14, 10), sprites["qqv"].clone().set_position(9, 40),
            sprites["rzt"].clone().set_position(30, 51), sprites["snw"].clone().set_position(28, 49),
            sprites["tuv"].clone().set_position(1, 53), sprites["ulq"].clone().set_position(28, 49),
            sprites["vxy"].clone().set_position(19, 40),
            # LS20 base energy (fij already had fog, no compensation needed)
            sprites["zba"].clone().set_position(55, 6),
            sprites["zba"].clone().set_position(30, 26),
            sprites["zba"].clone().set_position(55, 51),
            sprites["zba"].clone().set_position(15, 46),
            sprites["zba"].clone().set_position(15, 21),
            sprites["zba"].clone().set_position(45, 6),
        ],
        grid_size=(64, 64),
        data={"vxy": 42, "tuv": 0, "nlo": 8, "opw": 180, "qqv": 1, "ggk": 12, "fij": 0, "kdy": True},
        name="fij",
    ),
]


class Ws03(ARCBaseGame):
    def __init__(self, seed: int = 0) -> None:
        # Initialize attributes BEFORE super().__init__ since on_set_level is called during init
        # Must match ls20's order: opw(0), lyd(1), tmx(2), nio(3), dcb(4), fij(5)
        self.hep = [sprites["opw"], sprites["lyd"], sprites["tmx"], sprites["nio"], sprites["dcb"], sprites["fij"]]
        # Jarring color palette: Pink, Red, Yellow, Orange, Purple, Green, Dark Red, Blue, Light Pink, Light Gray
        self.hul = [6, 8, 11, 12, 15, 14, 13, 9, 7, 1]
        self.kdj = [0, 90, 180, 270]
        camera = Camera(width=64, height=64, background=5, letter_box=5, interfaces=[])
        super().__init__(game_id="ws03", levels=levels, camera=camera, seed=seed)

    def _get_rotation_index(self, value) -> int:
        try:
            return self.kdj.index(value)
        except (ValueError, TypeError):
            logging.warning(f"Invalid rotation value {value}, defaulting to 0")
            return 0

    def _get_color_index(self, value) -> int:
        try:
            return self.hul.index(value)
        except (ValueError, TypeError):
            logging.warning(f"Invalid color value {value}, defaulting to 0")
            return 0

    def on_set_level(self, level: Level) -> None:
        # Use tags like ls20 does: caf=player piece, wex=key indicator, nfq=level boundary
        self.mgu = level.get_sprites_by_tag("caf")[0]
        self.nio = level.get_sprites_by_tag("wex")[0]
        self.nlo = level.get_sprites_by_tag("nfq")[0]
        self.opw = sprites["opw"].clone()
        self.current_level.add_sprite(self.opw)
        self.opw.set_visible(False)
        self.qqv = level.get_sprites_by_tag("gic")
        self.pca = level.get_sprites_by_tag("caf")
        self.gfy = [level.get_data("qqv")] * len(self.qqv)
        # Must convert color VALUE to INDEX (ls20 uses hul.index())
        self.vxy = [self._get_color_index(level.get_data("ggk"))] * len(self.qqv)
        self.cjl = [self._get_rotation_index(level.get_data("fij"))] * len(self.qqv)
        self.rzt = [False] * len(self.qqv)
        # Fog of war always enabled in WS03
        self.qee = True

        class Ggk:
            def __init__(self, pca_list):
                self.pca_list, self.tmx = pca_list, 0
            def rzt(self, tmx):
                self.tmx = tmx
            def pca(self):
                return all(sprite.visible for sprite in self.pca_list)

        self.ggk = Ggk(self.pca)
        for dqk in range(len(self.qqv)):
            self.qqv[dqk].pixels = self.hep[self.gfy[dqk]].pixels.copy()
            self.qqv[dqk].color_remap(0, self.hul[self.vxy[dqk]])
            self.qqv[dqk].set_rotation(self.kdj[self.cjl[dqk]])
            self.pca[dqk].pixels = self.hep[self.gfy[dqk]].pixels.copy()
            self.pca[dqk].color_remap(0, self.hul[self.vxy[dqk]])
            self.pca[dqk].set_rotation(self.kdj[self.cjl[dqk]])
        self.pxr()
        self.egb = sprites["krg"].clone()
        self.current_level.add_sprite(self.egb)
        self.egb.set_visible(False)
        self.lbq = 3
        self.vcn, self.bzf, self.osd = [], [], []
        self.xhp, self.kbj = False, False
        self.rjw, self.qbn = self.mgu.x, self.mgu.y

    def rbt(self, edo: int, cdg: int, hds: int, xwr: int) -> List[Sprite]:
        return [bes for bes in self.current_level._sprites if bes.x >= edo and bes.x < edo + hds and bes.y >= cdg and bes.y < cdg + xwr]

    def step(self) -> None:
        if self.xhp:
            self.egb.set_visible(False)
            self.nio.set_visible(True)
            self.xhp = False
            self.complete_action()
            return
        if self.kbj:
            self.nlo.color_remap(None, 5)
            self.kbj = False
            self.complete_action()
            return
        lgr, kyr, axv = 0, 0, False
        if self.action.id.value == 1:
            kyr, axv = -1, True
        elif self.action.id.value == 2:
            kyr, axv = 1, True
        elif self.action.id.value == 3:
            lgr, axv = -1, True
        elif self.action.id.value == 4:
            lgr, axv = 1, True
        if not axv:
            self.complete_action()
            return
        xpb = False
        qul, cfy = self.mgu.x + lgr * 5, self.mgu.y + kyr * 5
        yet = self.rbt(qul, cfy, 5, 5)
        mnc = False
        for oib in yet:
            if oib.tags is None:
                break
            elif "jdd" in oib.tags:
                mnc = True
                break
            elif "mae" in oib.tags:
                qzq = self.qqv.index(oib)
                if not self.qhg(qzq):
                    self.nlo.color_remap(None, 0)
                    self.kbj = True
                    return
            elif "iri" in oib.tags:
                xpb = True
                self.ggk.rzt(self.ggk.tmx)
                self.vcn.append(oib)
                self.current_level.remove_sprite(oib)
            elif "gsu" in oib.tags:
                self.snw = (self.snw + 1) % len(self.hep)
                self.nio.pixels = self.hep[self.snw].pixels.copy()
                self.nio.color_remap(0, self.hul[self.tmx])
                self.ihm()
            elif "gic" in oib.tags:
                apq = (self.tmx + 1) % len(self.hul)
                self.nio.color_remap(self.hul[self.tmx], self.hul[apq])
                self.tmx = apq
                self.ihm()
            elif "bgt" in oib.tags:
                self.tuv = (self.tuv + 1) % 4
                self.nio.set_rotation(self.kdj[self.tuv])
                self.ihm()
        if not mnc:
            self.mgu.set_position(qul, cfy)
        if self.nje():
            self.next_level()
            self.complete_action()
            return
        if not xpb and not self.ggk.pca():
            self.lbq -= 1
            if self.lbq == 0:
                self.lose()
                self.complete_action()
                return
            self.egb.set_visible(True)
            self.egb.set_scale(64)
            self.egb.set_position(0, 0)
            self.nio.set_visible(False)
            self.xhp = True
            self.rzt = [False] * len(self.qqv)
            self.mgu.set_position(self.rjw, self.qbn)
            self.pxr()
            for bqs in self.vcn:
                self.current_level.add_sprite(bqs)
            for grk in self.bzf:
                self.current_level.add_sprite(grk)
            for qmb in self.osd:
                self.current_level.add_sprite(qmb)
            self.vcn, self.bzf, self.osd = [], [], []
            self.ggk.rzt(self.ggk.tmx)
            self.opw.set_visible(False)
            for sfs in self.current_level.get_sprites_by_tag("qex"):
                sfs.set_visible(False)
            for pqv in self.current_level.get_sprites_by_tag("yar"):
                pqv.set_visible(True)
            return
        self.complete_action()

    def pxr(self) -> None:
        self.tuv = self._get_rotation_index(self.current_level.get_data("fij"))
        self.tmx = self._get_color_index(self.current_level.get_data("ggk"))
        self.snw = self.current_level.get_data("qqv")
        self.nio.pixels = self.hep[self.snw].pixels.copy()
        self.nio.color_remap(0, self.hul[self.tmx])
        self.nio.set_rotation(self.kdj[self.tuv])

    def ihm(self) -> None:
        kic = False
        for fxn, qis in enumerate(self.qqv):
            dbb = self.current_level.get_sprite_at(qis.x - 1, qis.y - 1, "qex")
            if self.qhg(fxn) and not self.rzt[fxn]:
                kic = True
                if dbb:
                    dbb.set_visible(True)
            else:
                if dbb:
                    dbb.set_visible(False)
        self.opw.set_visible(kic)

    def qhg(self, azz: int) -> bool:
        return self.snw == self.gfy[azz] and self.tmx == self.vxy[azz] and self.tuv == self.cjl[azz]

    def nje(self) -> bool:
        for uop, ywm in enumerate(self.qqv):
            if not self.rzt[uop] and self.mgu.x == ywm.x and self.mgu.y == ywm.y and self.qhg(uop):
                self.rzt[uop] = True
                self.bzf.append(self.qqv[uop])
                self.osd.append(self.pca[uop])
                self.current_level.remove_sprite(self.qqv[uop])
                self.current_level.remove_sprite(self.pca[uop])
                xkp = self.current_level.get_sprite_at(ywm.x - 1, ywm.y - 1, "yar")
                if xkp and "vdr" in xkp.tags:
                    xkp.set_visible(False)
                    aoj = self.current_level.get_sprite_at(ywm.x - 1, ywm.y - 1, "qex")
                    if aoj:
                        aoj.set_visible(False)
                    self.opw.set_visible(False)
        return all(self.rzt)
