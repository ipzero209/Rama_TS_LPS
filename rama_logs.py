#!/usr/bin/python


import sys
import tarfile









def main():
    if len(sys.argv) < 2:
        print "Usage: ./rama_logs <TS File> where <TS File> is the path to the" \
              "Panorama tech support tarball."
        exit(1)
    infile = sys.argv[1]
    ts_file = tarfile.open(infile, 'r:gz')
    file_list = ts_file.getmembers()
    for file in file_list:
        if ('techsupport' in file.name) and ('saved-curr' not in file.name):
            print "Found Tech Support text file - {}. Checking device type.".format(file.name)
            ts_text = ts_file.extractfile(file)
            for line in ts_text:
                if 'model' in line:
                    line = line.split(':')
                    if ('Panorama' or 'M-100' or 'M-200' or 'M-500' or 'M-600') in line[1]:
                        print "This TS came from a Panorama. We can proceed."
                    else:
                        print "This TS file is not from a Panorama. Exiting."
                        exit(1)
    samples = []
    for file in file_list:
        if 'mp-monitor.log' in file.name:
            log_text = ts_file.extractfile(file)
            for line in log_text:
                if 'Incoming log rate' in line:
                    line = line.split(' = ')
                    sample = float(line[1].strip('\n'))
                    samples.append(sample)


    average = sum(samples) / len(samples)
    print "Average incoming log rate is {0:.2f}".format(average)

if __name__ == "__main__":
    main()