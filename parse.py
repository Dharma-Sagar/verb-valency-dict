import json
from pathlib import Path
from collections import defaultdict
import csv

in_path = Path('input/LIM_TibetanVerbValencyDictionary_data.json')
dump = in_path.read_text(encoding='utf-8')

loaded = json.loads(dump)

arg_list = []
parsed = defaultdict(list)
for head, a in loaded.items():
    exs = a['Examples']
    for struct, b in exs.items():
        pattern = struct.replace('+', ' ').split(' ')
        pattern = [p for p in pattern if p != 'solo']
        occs = []
        for occ in b:
            sent = occ['Citation']
            args = {p: occ[p] for p in pattern}
            arg_list.extend(args)
            occs.append([sent, args])
        parsed[head].append(occs)

arg_list = sorted(list(set(arg_list)))

# format for spreadsheet
out = [['verb'] + arg_list + ['example']]
for verb, exs in parsed.items():
    for ex in exs:
        for e in ex:
            args = []
            for a in arg_list:
                if a in e[1]:
                    args.append(e[1][a])
                else:
                    args.append('')
            out.append([[verb] + args + [e[0]]])

# export to csv
with open('verb-valency-raw.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)
    for line in out:
        writer.writerow(line)

print()
