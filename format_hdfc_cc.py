#!/usr/bin/python3
import os
import time
import argparse
import csv
import re

def ParseAmount(amount):
    x = re.sub(",", "", amount).split()
    if x[1] == "Cr.":
        print("Got credit entry [%s] [%s]" % (x[0], x[1]))
        return -1*float(x[0])
    else:
        return x[0]

def GetFields(csvreader):
    values = next(csvreader)
    fields = {}
    for index, value in enumerate(values):
        fields[value] = index
    return fields

def processInputFile(filename):
    transactions = []
    skip = True
    with open(filename, "r") as f:
        for line in f:
            if not skip:
                if line.strip() == "":
                    break
                transactions.append(line)
            if line.startswith("Transaction type"):
                skip = False
                transactions.append(line)
    return transactions


def ProcessRow(values):
    if values[5].startswith("Cr"):
        x = re.sub(",", "", values[4])
        values[4] = str(-1*(float(x)))

def WriteOutput(transactions, filename):
    results = []
    for index, row in enumerate(transactions):
        values = row.split("~")
        if index == 0:
            results.append(row)
        else:
            ProcessRow(values)
            results.append("~".join(values))
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
    transactions = processInputFile(args.input)
    WriteOutput(transactions, args.output)

main()
    
    
        

    
