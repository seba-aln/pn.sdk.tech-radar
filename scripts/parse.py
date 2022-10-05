import json
import os
import re

from argparse import ArgumentParser
from csv import reader

parser = ArgumentParser(
    description="CSV to JSON parser",
    usage="\n\tpython parse.py -d ./input_dir -o ./output_dir \n" \
        "\tpython parse.py -d ./input_dir -o ./output_dir"
)
parser.add_argument('-d', '--input-dir', type=str, help='source directory')
parser.add_argument('-f', '--input-file', type=str, help='source file')
parser.add_argument('-o', '--output-dir', type=str, default="./output/")
parser.add_argument('-r', '--replace', type=bool, default=False, help="Automatically replace existing output files")
parser.add_argument('-s', '--skip-header', type=bool, default=True, help="Should skip header line")
parser.add_argument('-t', '--input-type', type=str, default='md', help="Type of input file [md, csv]")

args = parser.parse_args()

extension = f".{args.input_type}"
if not args.input_dir and not args.input_file:
    raise Exception('Input file OR input dir are required')

files = []
if args.input_file:
    if not os.path.isfile(args.input_file) or not args.input_file.lower().endswith(extension):
        raise Exception(f"Input file does not exist or is not a {extension.upper()} file")

    files = [args.input_file]

if args.input_dir:
    if not os.path.isdir(args.input_dir):
        raise Exception('Input dir does not exist')

    files = [os.path.join(args.input_dir, file) for file in os.listdir(args.input_dir)
             if os.path.isfile(os.path.join(args.input_dir, file)) and file.lower().endswith(extension)]

    if not files:
        raise Exception(f'Input directory does not contain any {extension} files')


for cnt, file in enumerate(files):
    print(f'Parsing {cnt+1} of {len(files)}')
    header_row_skipped = False
    out = os.path.join(args.output_dir, os.path.basename(file.lower()).replace(extension, '.json'))

    if os.path.exists(out) and not args.replace:
        raise Exception(f'Cannot parse {file}. Output already exists. Use --replace to override')

    with open(file, 'r') as input_file, open(out, 'w') as output_file:
        lines = []
        if args.input_type == 'csv':
            csv_reader = reader(input_file)
            for row in csv_reader:
                if args.skip_header and not header_row_skipped:
                    header_row_skipped = True
                    continue
                lines.append({
                    'name': row[0],
                    'ring': row[1],
                    'quadrant': row[2],
                    'isNew': row[3],
                    'description': row[4]
                })
        if args.input_type == 'md':
            line = input_file.readline()
            while line:
                if args.skip_header and not header_row_skipped:
                    header_row_skipped = True
                    line = input_file.readline()
                    continue
                # skip markdown header separator
                is_head_separator = re.search('^([\| -])*$', line)
                if is_head_separator:
                    line = input_file.readline()
                    continue
                row = line.split('|')
                lines.append({
                    'name': row[1],
                    'ring': row[2],
                    'quadrant': row[3],
                    'isNew': row[4],
                    'description': row[5]
                })
                line = input_file.readline()


        output_file.write(json.dumps(lines))

