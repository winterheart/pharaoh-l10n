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
msginit_exec = "msginit"
msgmerge_exec = "msgmerge"


DOIT_CONFIG = {"default_tasks": ["pack"]}
SOURCES = {
    "po": list(po_file_dir.glob("**/*.po")),
    "pot": list(po_file_dir.glob("**/*.pot")),
    "source_csv": ["data/source/pharaoh.csv"],
    "target_csv": ["unity/pharaoh-l10n-assets/Assets/Resources/translation.csv"],
    "assetbundle": ["pharaoh-l10n.assetbundle"]
}


def task_extract():
    return {
        "actions": [
            f"{i2loc_exec} extract -i {SOURCES['source_csv'][0]} -p {po_file_dir}",

        ],
        "file_dep": SOURCES["source_csv"],
        "targets": SOURCES["pot"]
    }


def task_update_po():
    for i in SOURCES["pot"]:
        for lang in langs:
            po_file = Path.joinpath(po_file_dir, lang, Path(i.name).stem + ".po")
            if po_file.exists():
                action = f"{msgmerge_exec} -q --backup=off -U {po_file} {i}"
            else:
                action = f"{msginit_exec} -i {i} -o {po_file} -l {lang} --no-translator"

            yield {
                "name": i,
                "actions": [action],
                "task_dep": ["extract"],
                "file_dep": [i],
                "targets": [po_file]
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
        "targets": SOURCES["target_csv"],
        "task_dep": ["update_po"]
    }


def task_pack_assetbundle():
    return {
        "actions": [
            f"{unity_exec} {unity_args}"
        ],
        "file_dep": SOURCES["target_csv"],
        "targets": SOURCES["assetbundle"],
    }


def task_stats():
    return {
        "actions": [
            f"{i2loc_exec} stats -i {SOURCES['source_csv'][0]} -p {po_file_dir} -l {','.join(langs)} -V"
        ]
    }
