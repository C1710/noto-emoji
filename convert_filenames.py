import argparse
from os import PathLike
from typing import IO, AnyStr, Dict, List, Tuple
import re
import logging
import os, os.path
import pathlib

# Regexes from emoji_builder
# These first regexes are not used at the moment
hex_sequence = r"[a-fA-F0-9]{1,8}"
range_regex = r"(?P<range>(?P<range_start>{hex})\.\.(?P<range_end>{hex}))".format(hex = hex_sequence)
sequence_regex = r"(?P<sequence>({hex})(\s+({hex}))*)".format(hex = hex_sequence)
emoji_regex = r"(?P<codepoints>{}|{})".format(range_regex, sequence_regex)
emoji_kind_regex = r"(?P<kind>[A-Za-z_\-]+)"
data_regex = r"^{}\s*;\s*{}\s*(;(?P<name>.*)\s*)?(#.*)?$".format(emoji_regex, emoji_kind_regex)

emoji_sequence_space_regex = r"(([A-F0-9a-f]{1,8})(\s+([A-F0-9a-f]{1,8}))*)"
emoji_status_regex = r"(component|fully-qualified|minimally-qualified|unqualified)"
emoji_name_regex = r"(.*)?\s*E(\d+.\d+) (.+)"
emoji_test_regex = re.compile(r"^{}\s*;\s*{}\s*#\s*{}$".format(emoji_sequence_space_regex, emoji_status_regex, emoji_name_regex))

normalize_delimiter_regex = re.compile(r"[-_. ]")
normalize_remove_regex = re.compile(r"""[,*\\/:'"()]""")

def normalize_name(name: str) -> str:
    """Normalizes names to be space-separated and lowercase with less special characters"""
    name_components = normalize_delimiter_regex.split(name)
    simplified_name_components = (normalize_remove_regex.sub("", name_component) for name_component in name_components)
    simplified_name = " ".join(simplified_name_components)
    return simplified_name.lower()


def load_test_table(table: IO[AnyStr]) -> Dict[str, Tuple[int]]:
    """
    Loads the content of emoji-test.txt.
    The general format is "codepoint    ; fully-qualified # <Emoji> E<version> name"
    """
    mapping = dict()
    for line in table:
        line = line.strip()
        if line.startswith("#") or not line:
            # Comment
            continue
        entry = emoji_test_regex.match(line)
        if entry:
            sequence: str = entry.group(1)
            sequence_int = (int(codepoint, 16) for codepoint in sequence.split() if codepoint)
            sequence_int_no_fe0f = tuple((codepoint for codepoint in sequence_int if codepoint != 0xfe0f))
            _status = entry.group(5)
            name = normalize_name(entry.group(8))
            mapping[name] = sequence_int_no_fe0f
        else:
            logging.warn("Unrecognized table line:\n    {}".format(line))
    return mapping

def make_mapping(int_mappings: List[Dict[str, Tuple[int]]]) -> Dict[str, str]:
    """
    Merges normalized-name to int tuple-mappings to normalized-name to emoji_u<codepoint>-mapping
    """
    mapping = dict()
    for int_mapping in int_mappings:
        for (name, sequence) in int_mapping.items():
            sequence_str = "emoji_u{}".format("_".join((hex(codepoint)[2:] for codepoint in sequence)))
            mapping[name] = sequence_str
    return mapping

def replace_file_names(directory: PathLike, mapping: Dict[str, str], dry_run: bool = False):
    """Actually looks up the file names and replaces them"""
    for file in os.scandir(directory):
        if not file.is_file() or os.fsdecode(file.name).startswith("emoji_u"):
            continue
        else:
            file_path = pathlib.Path(file.path)
            basename = file_path.stem
            normalized_basename = normalize_name(basename)
            if normalized_basename not in mapping:
                logging.warning("Unrecognized name: {}".format(basename))
            else:
                # Rename/Move
                new_path = file_path.with_stem(mapping[normalized_basename])
                if not dry_run:
                    logging.info("{}  -->  {}".format(file_path, new_path))
                    os.rename(file_path, new_path)
                else:
                    print("{}  -->  {}".format(file_path, new_path))

def main(directory: PathLike, emoji_test_txt: PathLike, dry_run: bool = False):
    with open(emoji_test_txt, encoding="utf-8") as emoji_test_file:
        test_mapping = load_test_table(emoji_test_file)
        mapping = make_mapping([test_mapping])
        replace_file_names(directory=directory, mapping=mapping, dry_run=dry_run)

parser = argparse.ArgumentParser(
    description="Replaces emoji files with rich names by their emoji_u<codepoint> format"
)
parser.add_argument("--directory", type=pathlib.PurePath, help="The directory in which to replace the file names", default="./svg")
parser.add_argument("--emoji_test", type=pathlib.PurePath, help="The emoji-test.txt file to use for the translation", default="./emoji_test.txt")
parser.add_argument("--dry-run", action="store_true", help="does not perform any actual renaming")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.directory, args.emoji_test, args.dry_run)
