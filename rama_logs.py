#!/usr/bin/python


import sys
import tarfile









def main():
    infile = sys.argv[1]
    ts_file = tarfile.open(infile, 'r:gz')
    file_list = ts_file.getmembers()
    for file in file_list:
        if ('techsupport' in file.name) and ('saved-curr' not in file.name):
            print "Found Tech Support text file. Checking device type."
            ts_text = ts_file.extractfile(file)
            for line in ts_text:
                if 'model' in line:
                    line = line.split(':')
                    if ('Panorama' or 'M-100' or 'M-200' or 'M-500' or 'M-600') in line:
                        print "This TS came from a Panorama"


if __name__ == "__main__":
    main()