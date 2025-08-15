#!/usr/bin/python3
import os
import time
import argparse
import csv
import re

def GetFields(csvreader):
    values = next(csvreader)
    fields = {}
    for index, value in enumerate(values):
        fields[value] = index
    return fields

def processInputFile(filename):
    lines = []
    skip = True
    with open(filename, "r") as f:
        for line in f:
            # skip empty lines
            if not line.strip():
                continue
            if line.startswith("REWARD POINTS SUMMARY"):
                break
            if not skip:
                lines.append(line.strip())
            if line.startswith("DATE,MODE,PARTICULARS,DEPOSITS,WITHDRAWALS,BALANCE"):
                lines.append(line.strip())
                skip = False
    for line in lines:
        print("Got line: %s" % line)
    csvreader = csv.reader(lines)
    fields = GetFields(csvreader)
    for key in fields:
        print("Got field: %s, value %s" % (key, fields[key]))
    processed_lines = []
    processed_lines.append(("Transaction Date",
                            "Details",
                            "Deposits",
                            "Withdrawals",
                            "Balance"))
                            
    for row in csvreader:
        date = row[fields["DATE"]]
        details = row[fields["PARTICULARS"]]
        if row[fields["MODE"]]:
            details = details + " (%s)" % row[fields["MODE"]]
        deposit = row[fields["DEPOSITS"]]
        withdrawal = row[fields["WITHDRAWALS"]]
        balance = row[fields["BALANCE"]]
        details = details + "[%s]" % balance
        parsed_row = (date, details, deposit, withdrawal, balance)
        print("%s, %s, %s, %s, %s" % parsed_row)
        processed_lines.append(parsed_row)
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
    
    
        

    
