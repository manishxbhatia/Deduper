#!/usr/bin/python3
import os
import time
import argparse
import csv
import re

_DELIMITER_ = "~|~"
_OUT_DELIMITER_ = ","

def ParseAmount(amount):
    x = re.sub(",", "", amount).split()
    if x[1] == "Cr.":
        print("Got credit entry [%s] [%s]" % (x[0], x[1]))
        return -1*float(x[0])
    else:
        return x[0]


def readTransactionsFromInputFile(filename):
    transactions = []
    skip = True
    with open(filename, "r") as f:
        for line in f:
            print("Processing line: %s" % line)
            if not skip:
                if line.strip() == "":
                    break
                transactions.append(line)
            if line.startswith("Transaction type"):
                skip = False
                transactions.append(line)
    return transactions


def ProcessRow(values):
    x = re.sub(",", "", values[4])
    if values[5].startswith("Cr"):
        values[4] = str(-1*(float(x)))
    else:
        values[4] = str(float(x))


def ProcessTransactionsAndWriteOutput(transactions, filename):
    results = []
    for index, row in enumerate(transactions):
        print ("Processing Transaction %d: %s" % (index, row))
        values = row.split(_DELIMITER_)
        if index == 0:
            results.append(_OUT_DELIMITER_.join(values))
        else:
            ProcessRow(values)
            results.append(_OUT_DELIMITER_.join(values))
    with open(filename, "w") as f:
        for row in results:
            f.write(row)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input", help="File to parse")
    parser.add_argument("-o", "--output", help="Location of output file")
    args = parser.parse_args()
    print("Input file: %s" % args.input)
    print("output file: %s" % args.output)
    transactions = readTransactionsFromInputFile(args.input)
    ProcessTransactionsAndWriteOutput(transactions, args.output)

main()
    
    
        

    
