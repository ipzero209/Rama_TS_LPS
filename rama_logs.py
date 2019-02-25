#!/usr/bin/python


import sys
import tarfile
import math





def getHigh(num_list):
    """Returns the highest value in the sample list."""
    h_val = 0
    for num in num_list:
        if num > h_val:
            h_val = num
    return h_val


def getLow(num_list):
    """Returns the lowest value in the sample list."""
    l_val = 80000
    for num in num_list:
        if num < l_val:
            l_val = num
    return l_val


def getAverage(num_list):
    """Returns the average value of the sample list."""
    avg = sum(num_list) / len(num_list)
    return avg


def getSD(num_list):
    """Returns the standard deviation of the sample list."""
    avg = getAverage(num_list)
    mean_diff = []
    for num in num_list:
        mds = (num - avg)**2
        mean_diff.append(mds)
    mds_avg = getAverage(mean_diff)
    sd = math.sqrt(mds_avg)
    return sd



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

    high = getHigh(samples)
    print "High: {0:.2f}".format(high)

    low = getLow(samples)
    print "Low: {0:.2f}".format(low)

    average = getAverage(samples)
    print "Average incoming log rate is {0:.2f}".format(average)

    stdev = getSD(samples)
    print "Standard deviation is {0:.2f}".format(stdev)


if __name__ == "__main__":
    main()