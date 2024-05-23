import os
import argparse
import re
import translators as ts


def get_srt_files(root_dir):
    """receive all files with .srt extension"""
    srt_paths = []

    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".srt"):
                relative_path = os.path.join(foldername, filename)
                srt_paths.append(relative_path)

    return srt_paths


def transl(s: str, from_lang: str, to_lang: str) -> str:
    """receiving translate of str"""
    return ts.translate_text(
        s,
        translator="yandex",
        from_language=from_lang,
        to_language=to_lang,
    )


def is_timecode(s: str) -> bool:
    """checking that is a timecode str"""
    return bool(re.match(r"\d\d:\d\d:\d\d", s))


def is_num(s: int) -> bool:
    """checking is num (pattrn: "<num>\\n")"""
    for i in s:
        if not i.isdigit() and i != "\n":
            return False
    return True


def setup_parser() -> argparse.ArgumentParser:
    """setup and return CL args parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root_dir",
        "-rd",
        type=str,
        default="./",
        help="Root directory to search for .srt files",
    )
    parser.add_argument(
        "--from_lang",
        "-fl",
        type=str,
        default="en",
        help="Language from translate",
    )
    parser.add_argument(
        "--to_lang",
        "-tl",
        type=str,
        default="ru",
        help="Language to translate",
    )
    return parser


def temp_file_name(file_name: str) -> str:
    """gen names for temp files"""
    return f"{file_name[:-4]}_1.srt"


def main():
    # setup CL argumens parser
    parser = setup_parser()
    # receive CL args
    args = parser.parse_args()

    from_names = get_srt_files(args.root_dir)

    for file_index in range(len(from_names)):
        # open temp file for write
        with open(temp_file_name(from_names[file_index]), "w") as temp_file:
            # open original file for read
            with open(from_names[file_index], "r") as original_file:
                for line in original_file:
                    # on its cases is no point in translating
                    if is_num(line) or line == "\n" or is_timecode(line):
                        temp_file.write(line)
                        continue

                    temp_file.write(transl(line, args.from_lang, args.to_lang) + "\n")

        # replace from temp file to original
        os.remove(from_names[file_index])
        os.rename(temp_file_name(from_names[file_index]), from_names[file_index])


if __name__ == "__main__":
    main()
