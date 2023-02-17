# This file is part of Pharaoh L10n project
# SPDX-License-Identifier: GPL-3.0-or-later
# (c) 2023 Azamat H. Hackimov <azamat.hackimov@gmail.com>

from pathlib import Path

langs = ["ru"]
po_file_dir = Path("data/po")
unity_exec = "/home/winterheart/Unity/Hub/Editor/2019.4.38f1/Editor/Unity"
unity_args = "-projectPath unity/pharaoh-l10n-assets" \
             " -executeMethod CreateAssetBundles.BuildAllAssetBundles -batchmode -quit"

i2loc_exec = "scripts/i2loc_translate.py"


DOIT_CONFIG = {"default_tasks": ["pack"]}
SOURCES = {
    "po": list(po_file_dir.glob("**/*.po")),
    "source_csv": ["data/source/pharaoh.csv"],
    "target_csv": ["unity/pharaoh-l10n-assets/Assets/Resources/translation.csv"],
    "assetbundle": ["pharaoh-l10n.assetbundle"]
}


def task_pack():
    return {
        "actions": None,
        "task_dep": ["pack_assetbundle"]
    }


def task_pack_target_csv():
    return {
        "actions": [
            f"{i2loc_exec} pack -i {SOURCES['source_csv'][0]} -p {po_file_dir} -o {SOURCES['target_csv'][0]} -l {','.join(langs)}"
        ],
        "file_dep": SOURCES["po"],
        "targets": SOURCES["target_csv"]
    }


def task_pack_assetbundle():
    return {
        "actions": [
            f"{unity_exec} {unity_args}"
        ],
        "file_dep": SOURCES["target_csv"],
        "targets": SOURCES["assetbundle"],
    }
