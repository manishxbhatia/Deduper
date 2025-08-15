#!/usr/bin/python3
import os
import time
import argparse
import csv
import re

START_LINE = '"Transaction Details:"'

def ParseAmount(amount):
    x = re.sub(",", "", amount).split()
    if x[1] == "CR":
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
    lines = []
    skip = True
    print("Reading file %s" % filename)
    with open(filename, "r") as f:
        for line in f:
            if not skip:
                lines.append(line.strip())
            if line.startswith(START_LINE):
                skip = False
    for line in lines:
        print("Got line: %s" % line)
    csvreader = csv.reader(lines)
    fields = GetFields(csvreader)
    processed_lines = []
    processed_lines.append(("Date",
                            "Details",
                            "Amount (INR)",
                            "Ref"))
                            
    for row in csvreader:
        date = row[fields["Date"]]
        details = row[fields["Transaction Details"]]
        amount = row[fields["Amount(in Rs)"]]
        sign = row[fields["BillingAmountSign"]]
        if sign:
            amount = -1*float(amount)
        ref_no = row[fields["Sr.No."]]
        print("%s, %s, %s, %s" % (date, details, amount, ref_no))
        processed_lines.append((date, details, amount, ref_no))
    return processed_lines

def WriteOutput(lines, filename):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input", help="File to parse")
    parser.add_argument("-o", "--output", help="Location of output file")
    args = parser.parse_args()
    print("Input file: %s" % args.input)
    print("output file: %s" % args.output)
    processed_lines = processInputFile(args.input)
    WriteOutput(processed_lines, args.output)

main()
    
    
        

    
