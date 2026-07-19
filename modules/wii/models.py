from dataclasses import dataclass


@dataclass
class WiiInfo:

    syscheck: bool = False
    nand: bool = False
    keys: bool = False

    bootmii: bool = False
    apps: bool = False
    private: bool = False
    wad: bool = False