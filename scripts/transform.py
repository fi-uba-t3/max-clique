#!/usr/bin/env python3

import glob

OUTPUT_FILE = "{}.txt"

def main():

    for file_path in glob.glob("graphs/*.clq"):
        
        with open(file_path) as f:
            lines = f.readlines()

        lines = filter(lambda x: not x.startswith("c"), lines)
        lines = filter(lambda x: not x.startswith("p"), lines)

        lines = map(lambda x: x.strip("e "), lines)

        with open(OUTPUT_FILE.format(file_path.strip(".clq")), "w") as f:
            for l in lines:
                f.write(l)

if __name__ == "__main__":
    main()

