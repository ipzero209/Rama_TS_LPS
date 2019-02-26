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


def nonZero(num_list):
    """Returns the number of samples that are 0."""
    zc = 0
    nz_samples = []
    for num in num_list:
        if num == 0:
            zc += 1
        else:
            nz_samples.append(num)
    nz_avg = getAverage(nz_samples)
    return zc,nz_avg


def capCheck(model, mode, in_rate, stdev):
    """Checks the calculated ingtestion rate (avg + SD) against model
    capacity."""
    capacities = {'Panorama':{'management-only':0,'panorama':10000,'logger':15000},
                  'M-100':{'management-only':0,'Panorama':10000,'logger':15000},
                  'M-200':{'management-only':0,'panorama':10000,'logger':28000},
                  'M-500':{'management-only':0,'panorama':15000,'logger':30000},
                  'M-600':{'management-only':0,'panorama':25000,'logger':55000}}
    capacity = capacities[model][mode]
    if (in_rate + stdev) > capacity:
        return 1
    else:
        return 0


def getCap(model, mode):
    """Returns the ingestion rate for the model/mode provided."""
    capacities = {'Panorama': {'management-only': 0, 'panorama': 10000, 'logger': 15000},
                  'M-100': {'management-only': 0, 'Panorama': 10000, 'logger': 15000},
                  'M-200': {'management-only': 0, 'panorama': 10000, 'logger': 28000},
                  'M-500': {'management-only': 0, 'panorama': 15000, 'logger': 30000},
                  'M-600': {'management-only': 0, 'panorama': 25000, 'logger': 55000}}
    capacity = capacities[model][mode]
    return capacity

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
                    line = line.split(': ')
                    if ('Panorama' or 'M-100' or 'M-200' or 'M-500' or 'M-600') in line[1]:
                        model = line[1].strip('\n')
                        print "This TS came from a Panorama. Checking operational" \
                              " mode."
                        for m_line in ts_text:
                            if "system-mode" in m_line:
                                m_line = m_line.split(": ")
                                mode = m_line[1].strip('\n')
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



    print "\n========================================"

    print "Total number of samples: {}".format(str(len(samples)))

    high = getHigh(samples)
    print "High: {0:.2f}".format(high)

    low = getLow(samples)
    print "Low: {0:.2f}".format(low)

    average = getAverage(samples)
    print "Average incoming log rate is {0:.2f}.".format(average)

    stdev = getSD(samples)
    print "Standard deviation is {0:.2f}\n\n".format(stdev)

    num_zeros , nz_avg = nonZero(samples)
    zero_pct = num_zeros / len(samples)
    print "The average above includes {} samples with a value of 0.".format(num_zeros)

    print "This number represents {0:.2f}%" \
          " of the total number of samples. If this number is greater than" \
          " 5, please investigate.".format(zero_pct)

    # print "The average of all non-zero samples is {0:.2f}".format(nz_avg)

    print "========================================\n"

    print "\n========================================"
    capacity = getCap(model, mode)
    usage = average + stdev
    usage_pct = ((average + stdev) / capacity) * 100
    print "Platform usage as of this TS file is:\n{0:.2f}".format(usage)
    print "---------"
    print "{}\n".format(capacity)
    print "or {0:.2f}% capacity.\n\n".format(usage_pct)
    print "The top number represents the simple average ingestion rate + 1 standard deviation."

    print "========================================\n"


    cap = capCheck(model, mode, average, stdev)
    if cap == 1:
        print "===================================="
        print "The average + 1 stddev is greater than the capacity of this " \
              "model/mode of Panorama."
        print "===================================="





if __name__ == "__main__":
    main()