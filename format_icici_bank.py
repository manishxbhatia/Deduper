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
        if value == "DATE" or "Value Date" in value:
            fields["DATE"] = index
        if value == "MODE" or "Cheque Number" in value:
            fields["MODE"] = index
        if value == "PARTICULARS" or "Transaction Remarks" in value:
            fields["PARTICULARS"] = index
        if value == "DEPOSITS" or "Deposit Amount" in value:
            fields["DEPOSITS"] = index
        if value == "WITHDRAWALS" or "Withdrawal Amount" in value:
            fields["WITHDRAWALS"] = index
        if value == "BALANCE" or "Balance" in value:
            fields["BALANCE"] = index
    return fields

def processInputFile(filename):
    lines = []
    skip = True
    with open(filename, "r") as f:
        for line in f:
            print("Processing line: %s" % line)
            # skip empty lines
            if not line.strip():
                continue
            if "Legends Used in Account Statement" in line:
                print("Stopping")
                break
            if line.startswith("REWARD POINTS SUMMARY"):
                break
            if "DATE,MODE,PARTICULARS,DEPOSITS,WITHDRAWALS,BALANCE" in line:
                skip = False
            if "S No.,Value Date,Transaction Date,Cheque Number,Transaction Remarks,Withdrawal Amount(INR),Deposit Amount(INR),Balance(INR)" in line:
                skip = False
            if not skip:
                lines.append(line.strip())
    print("Got total lines: %d" % len(lines))
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
        mode = row[fields["MODE"]]
        if mode and mode != "-":
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

