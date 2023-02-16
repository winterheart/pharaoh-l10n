#!/usr/bin/env python
# This file is part of I2Loc translation project
# SPDX-License-Identifier: GPL-3.0-or-later
# (c) 2020, 2023 Azamat H. Hackimov <azamat.hackimov@gmail.com>

"""
RCG2 Translate - translation tool for River City Girls 2 text resources

Usage:
    i2loc_translate extract --input=<input_csv> --podir=<podir> [--lang=<language>...] [-V]
    i2loc_translate pack --input=<input_cvs> --podir=<podir> --output=<output_cvs> [--lang=<language>...] [-V]
    i2loc_translate --help
    i2loc_translate --version

Commands:
    extract     Extract text resources from source csv into Gettext PO files
    pack        Create updated csv-file based on source.csv and Gettext PO files

Options:
    -i IN_CSV --input=IN_CSV        Source CSV file
    -p PO_DIR --podir=PO_DIR        Directory where Gettext PO files will be placed or fetched
    -l LANG --lang=LANG             Process only specified language. This parameter can be defined multiple times
                                    By default will be processed all supported languages
    -o OUT_CSV --output=OUT_CSV     Path to translated CSV file
    -V --verbose                    Enable verbose output
    -h --help                       Print this help
    -v --version                    Print version and exit

Description:
I2Loc Translate tool

Copyright:
    (c) 2020, 2023 Azamat H. Hackimov <azamat.hackimov@gmail.com>
    License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it. There is NO WARRANTY,
    to the extent permitted by law.

"""

import logging
from docopt import docopt
from lib.i2loc_l10n import I2LocCsvKeys, I2LocLanguages, I2LocTranslation
from os.path import exists

version = "I2Loc Translate 0.9.0"

if __name__ == "__main__":
    args = docopt(__doc__, version=version)

    logger = logging.getLogger("I2Loc")
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(name)s: %(message)s')
    if args["--verbose"]:
        logger.setLevel(logging.INFO)

    if not exists(args["--input"]):
        logger.error("'{}' does not exist! Please specify correct path.".format(args["--input"]))
        exit(-2)

    languages = []
    # Validate languages
    if len(args["--lang"]):
        for lang in args["--lang"]:
            try:
                language = next(name.value["iso_code"] for name in I2LocLanguages if name.value["iso_code"] == lang)
                languages.append(language)
            except StopIteration:
                logger.warning("{} is not supported, skipping it.".format(lang))

    if len(languages) == 0:
        for lang in I2LocLanguages:
            languages.append(lang.value["iso_code"])
    logger.info("Processing languages: {}".format(languages))

    if args["extract"]:
        logger.info("Extracting text data into {}".format(args["--podir"]))
        rcg_translation = I2LocTranslation(args["--input"])
        rcg_translation.save_po(args["--podir"], languages)
        logger.info("Done!")

    if args["pack"]:
        logger.info("Packing text data into {}".format(args["--output"]))
        rcg_translation = I2LocTranslation(args["--input"])

        for lang in languages:
            for item in I2LocCsvKeys:
                rcg_translation.load_po(args["--podir"], item, lang)

        rcg_translation.save_csv(args["--output"], languages)
        logger.info("Done!")
