# This file is part of River City Girls L10n project
# Licensed under GPL-3+ License
# (c) 2020, 2023 Azamat H. Hackimov <azamat.hackimov@gmail.com>

from datetime import datetime
from enum import Enum
import csv
import logging
from os import makedirs
from os.path import join, exists
from polib import POEntry, POFile, pofile


class I2LocCsvKeys(Enum):
    # Constants from CSV dictionary
    EMPTY_CATEGORY = "EmptyCat"
    BUILDING = "Building"
    BUILDINGS = "Buildings"
    ENCYCLO = "Encyclo"
    EVENTS = "Events"
    EVENTS_CHAINEDEVENTS = "Events/ChainedEvents"
    GUIDE = "Guide"
    GUIDE_LOADINGSTRING = "Guide/LoadingScreen"
    HOUSES = "Houses"
    KEYBOARD = "Keyboard"
    LEGACY = "Legacy"
    MAPEDITOR = "MapEditor"
    MENU = "Menu"
    MENU_AUTOBATTLE = "Menu/AutoBattle"
    MENU_BATTLE = "Menu/Battle"
    MENU_CREDITS = "Menu/Credits"
    MENU_EVENT = "Menu/Event"
    MENU_GAMEMODE = "Menu/GameMode"
    MENU_LANGUAGE = "Menu/Language"
    MENU_OBJECTIVES = "Menu/Objectives"
    MENU_OPTIONS = "Menu/Options"
    MENU_OPTIONS_HOTKEY = "Menu/Options/Hotkey"
    MENU_OPTIONS_KEYREBING = "Menu/Options/KeyRebind"
    MENU_OPTIONS_SCREENMODE = "Menu/Options/ScreenMode"
    MISSIONS = "Missions"
    MISSIONS_PERIODS = "Missions/Periods"
    MONUMENTS = "Monuments"
    NAMES = "Names"
    NAMES_ARMY = "Names/Army"
    NAMES_PHARAOH = "Names/Pharaoh"
    OVERLAYS = "Overlays"
    OVERSEERS = "Overseers"
    RELIGION = "Religion"
    TUTORIAL = "Tutorial"
    WALKERS = "Walkers"
    WALKERS_PREDATOR = "Walkers/Predator"
    WORLDMAP = "Worldmap"


class I2LocLanguages(Enum):
    LANG_CHINESESIMPLIFIED = {"key": "Chinese (Simplified)", "iso_code": "zh-cn", "loc_name": "Chinese (Simplified)"}
    LANG_CHINESETRADITIONAL = {"key": "Chinese (Traditional)", "iso_code": "zh-tw", "loc_name": "Chinese (Traditional)"}
    LANG_ENGLISH = {"key": "English", "iso_code": "en", "loc_name": "English"}
    LANG_FRENCH = {"key": "French", "iso_code": "fr", "loc_name": "Français"}
    LANG_GERMAN = {"key": "German", "iso_code": "de", "loc_name": "Deutsch"}
    LANG_ITALIAN = {"key": "Italian", "iso_code": "it", "loc_name": "Italiano"}
    LANG_JAPANESE = {"key": "Japanese", "iso_code": "ja", "loc_name": "Japanese"}
    LANG_KOREAN = {"key": "Korean", "iso_code": "ko", "loc_name": "Korean"}
    LANG_RUSSIAN = {"key": "Russian", "iso_code": "ru", "loc_name": "Русский"}
    LANG_SPANISH = {"key": "Spanish", "iso_code": "es", "loc_name": "Español"}


LANG_KEY = "Key"

METADATA_ENTRY = {
    'Project-Id-Version': '1.0',
    'Report-Msgid-Bugs-To': 'you@example.com',
    'POT-Creation-Date': datetime.now().strftime("%Y-%m-%d %H:%M%z"),
    'PO-Revision-Date': datetime.now().strftime("%Y-%m-%d %H:%M%z"),
    'Last-Translator': 'you <you@example.com>',
    'Language-Team': '',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding': '8bit',
}


class I2LocTranslation:
    def __init__(self, csv_path):
        """
        Init class for handling *.csv
        :param csv_path: Path to CSV file (UTF-8, ";" as delimiter)
        """
        self.inject_langs = list([I2LocLanguages.LANG_RUSSIAN])
        self.logger = logging.getLogger("I2Loc")
        with open(csv_path, "r", newline="", encoding="utf-8") as read_file:
            csv_content = csv.DictReader(read_file, delimiter=";")
            self.content = list(csv_content)

    def save_csv(self, csv_path, languages):
        """
        Save class as complete CSV file
        :param csv_path: path to CSV file
        :param languages: list of languages being processed into result CSV
        :return:
        """
        with open(csv_path, "w", encoding="utf-8", newline="") as write_file:
            fieldnames = ["Key", "Type", "Desc"]
            for i in languages:
                language = next(name.value["key"] for name in I2LocLanguages if name.value["iso_code"] == i)
                fieldnames.append(language)
            writer = csv.DictWriter(
                write_file,
                fieldnames=["Key", "Type", "Desc",
                            I2LocLanguages.LANG_ENGLISH.value["key"],
                            I2LocLanguages.LANG_FRENCH.value["key"],
                            I2LocLanguages.LANG_SPANISH.value["key"],
                            I2LocLanguages.LANG_GERMAN.value["key"],
                            I2LocLanguages.LANG_ITALIAN.value["key"],
                            I2LocLanguages.LANG_RUSSIAN.value["key"],
                            ],
                delimiter=";", lineterminator="\n")
            writer.writeheader()
            for row in self.content:
                writer.writerow(row)
        return

    def load_po(self, path, csv_root_key, lang):
        """
        Load content of Gettext PO file (from "path/lang/json_root_key.po") into already loaded JSON content
        :param path: Root directory
        :param csv_root_key: JSON key from RcgJsonKeys class
        :param lang: Language. Should be in RcgLanguages class
        :return:
        """

        language = next(name.value["key"] for name in I2LocLanguages if name.value["iso_code"] == lang)

        po_file = join(path, lang, csv_root_key.value.replace("/", "_") + ".po")

        if exists(po_file):
            po = pofile(po_file)

            for entry in po:
                if not entry.obsolete:
                    temp_list = list()
                    if csv_root_key != I2LocCsvKeys.EMPTY_CATEGORY:
                        temp_list.append(csv_root_key.value)
                    temp_list.append(entry.msgctxt)
                    try:
                        csv_entry = next(item for item in self.content if item[LANG_KEY] == "/".join(temp_list))
                        if entry.translated() and "fuzzy" not in entry.flags:
                            csv_entry[language] = entry.msgstr
                        else:
                            csv_entry[language] = entry.msgid
                    except StopIteration:
                        self.logger.warning(f"Entry '{'/'.join(temp_list)}' does not exist in source CSV")
                        for lang in self.inject_langs:
                            if f"#{lang.value['key']}" == entry.msgctxt:
                                self.content.append(
                                    {
                                        "Key": "/".join(temp_list),
                                        "Type": "Text",
                                        "Desc": "",
                                        I2LocLanguages.LANG_ENGLISH.value["key"]: entry.msgstr,
                                        I2LocLanguages.LANG_FRENCH.value["key"]: entry.msgstr,
                                        I2LocLanguages.LANG_SPANISH.value["key"]: entry.msgstr,
                                        I2LocLanguages.LANG_GERMAN.value["key"]: entry.msgstr,
                                        I2LocLanguages.LANG_ITALIAN.value["key"]: entry.msgstr,
                                        I2LocLanguages.LANG_RUSSIAN.value["key"]: entry.msgstr,
                                    }
                                )

        else:
            self.logger.warning(f"ERROR: '{po_file}' is not exists! Skipping.")

        return

    def save_po(self, path, languages):
        """
        Save Gettext PO file into directory structure as "path/lang/csv_root_key.po"
        If "path/lang/json_root_key.po" already exists, it will be updated accordingly to CSV dict
        :param path: Root directory where place to files
        :param lang: Language to translate. Should be in Rcg2Languages class
        :return:
        """

        class PotFileEntry:
            def __init__(self, path, pot_file, create=False):
                self.path = path
                self.po_file = pot_file
                self.create = create

        # Create POT files
        pot_files = dict()
        pot_path = join(path, "pot")
        if not exists(pot_path):
            makedirs(pot_path)

        for i in I2LocCsvKeys:
            pot_files[i.value] = PotFileEntry(join(pot_path, i.value.replace("/", "_") + ".pot"),
                                              POFile(check_for_duplicates=True),
                                              not exists(join(pot_path, i.value.replace("/", "_") + ".pot")))
            pot_files[i.value].po_file.metadata = METADATA_ENTRY
            pot_files[i.value].po_file.metadata_is_fuzzy = 1

        for row in self.content:
            temp_list = row[LANG_KEY].split("/")
            if len(temp_list) == 1:
                category = I2LocCsvKeys.EMPTY_CATEGORY.value
                key = temp_list[0]
            else:
                key = temp_list.pop()
                category = "/".join(temp_list)
                # (category, key) = row[LANG_KEY].split("/")
            if category in pot_files.keys():
                if row[I2LocLanguages.LANG_ENGLISH.value["key"]] != "":
                    po_entry = POEntry(
                        msgctxt=key,
                        msgid=row[I2LocLanguages.LANG_ENGLISH.value["key"]],
                    )

                    try:
                        pot_files[category].po_file.append(po_entry)
                    except ValueError:
                        self.logger.debug(f"Entry {row[LANG_KEY]} already exists, skipping...")
            else:
                self.logger.warning(f"Category '{category}' not found")
        # We ready to dump POT files into FS
        for i in I2LocCsvKeys:
            self.logger.info(f"Saving POT-file {pot_files[i.value].path}")
            if i == I2LocCsvKeys.MENU_LANGUAGE:
                # Injecting here own languages
                for lang in self.inject_langs:
                    po_entry = POEntry(
                        msgctxt=f"#{lang.value['key']}",
                        msgid=lang.value["loc_name"],
                    )
                    try:
                        pot_files[i.value].po_file.append(po_entry)
                    except ValueError:
                        self.logger.debug(f"Entry {po_entry.msgid} already exists, skipping...")

            pot_files[i.value].po_file.save(pot_files[i.value].path)

        for lang_code in languages:
            language = next(name.value["key"] for name in I2LocLanguages if name.value["iso_code"] == lang_code)
            save_path = join(path, lang_code)
            if not exists(save_path):
                makedirs(save_path)

            for i in I2LocCsvKeys:
                po_path = join(save_path, i.value.replace("/", "_") + ".po")
                po_file = pot_files[i.value].po_file
                for entry in po_file:
                    tmp_list = list()
                    if i.value != "EmptyCat":
                        tmp_list.append(i.value)
                    tmp_list.append(entry.msgctxt)

                    target_str = self.find_csv_entry(language, "/".join(tmp_list))
                    if target_str != "":
                        entry.msgstr = target_str
                        if "fuzzy" not in entry.flags:
                            entry.flags.append("fuzzy")
                if exists(po_path):
                    self.logger.info(f"Merging PO-file {po_path}")
                    po = pofile(po_path)
                    po.merge(po_file)
                    po.save(po_path)
                else:
                    self.logger.info(f"Saving PO-file {po_path}")
                    po_file.save(po_path)
        return

    def show_stats(self, path, csv_root_key, lang):
        po_file = join(path, lang, csv_root_key.value.replace("/", "_") + ".po")

        stats = {
            "translated": 0,
            "untranslated": 0,
            "fuzzy": 0
        }
        if exists(po_file):
            po = pofile(po_file)
            stats["fuzzy"] += len(po.fuzzy_entries())
            stats["translated"] += len(po.translated_entries())
            stats["untranslated"] += len(po.untranslated_entries())
            self.logger.debug(
                f"{po_file}: "
                f"{stats['translated']}/"
                f"{stats['fuzzy']}/"
                f"{stats['untranslated']} "
                f"({100 * stats['translated'] / (stats['translated'] + stats['untranslated'] + stats['fuzzy']):.2f}%)"
            )
        return stats

    def find_csv_entry(self, column, input):
        """
        Lookup entry in loaded CSV file
        :param column: Where to search
        :param input: Reference input in English
        :return: Translated string or empty string if no such entry
        """
        for row in self.content:
            if row[LANG_KEY] == input and column in row.keys():
                return row[column]
        return ""
