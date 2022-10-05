import json
import os

from argparse import ArgumentParser
from csv import reader

parser = ArgumentParser(
    description="CSV to JSON parser",
    usage="\n\tpython parse.py -d ./input_dir -o ./output_dir \n" \
        "\tpython parse.py -d ./input_dir -o ./output_dir"
)
parser.add_argument('-d', '--input-dir', type=str, help='source directory')
parser.add_argument('-f', '--input-file', type=str, help='source file')
parser.add_argument('-o', '--output-dir', type=str, default="./radars/")
parser.add_argument('-r', '--replace', type=bool, default=False, help="Automatically replace existing output files")
parser.add_argument('-s', '--skip-header', type=bool, default=True, help="Should skip header line")

args = parser.parse_args()


if not args.input_dir and not args.input_file:
    raise Exception('Input file OR input dir are required')

files = []
if args.input_file:
    if not os.path.isfile(args.input_file) or not args.input_file.lower().endswith('.csv'):
        raise Exception('Input file does not exist or is not a CSV file')

    files = [args.input_file]

if args.input_dir:
    if not os.path.isdir(args.input_dir):
        raise Exception('Input dir does not exist')

    files = [os.path.join(args.input_dir, file) for file in os.listdir(args.input_dir)
             if os.path.isfile(os.path.join(args.input_dir, file)) and file.lower().endswith('.csv')]

    if not files:
        raise Exception('Input directory does not contain any CSV file')


for cnt, file in enumerate(files):
    print(f'Parsing {cnt+1} of {len(files)}')
    header_row_skipped = False
    out = os.path.join(args.output_dir, os.path.basename(file.lower()).replace('.csv', '.json'))

    if os.path.exists(out) and not args.replace:
        raise Exception(f'Cannot parse {file}. Output already exists. Use --replace to override')

    with open(file, 'r') as input_file, open(out, 'w') as output_file:
        csv_reader = reader(input_file)
        lines = []
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
        output_file.write(json.dumps(lines))

