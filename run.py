import argparse
import PDBUtils

# Parse the arguments to get the output directory where the dictionary must be created
parser = argparse.ArgumentParser(description="This Python script is a crawler/parser that " \
                        "extracts phonetic transcriptions of french words from fr.wiktionary.org.")
group = parser.add_argument_group('mandatory arguments')
group.add_argument('-o', '--output_dir', help="output directory where the dictionary will be created", required=True)
args = parser.parse_args()

# Run the Phonetic Dictionary Builder
PDBUtils.getLatestWiktionaryDump(PDBUtils.WikiLang.fr, args.output_dir)

