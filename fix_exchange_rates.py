#!/usr/bin/python3
import os
import datetime
import argparse
import csv
import re
import sys

DATE_FORMAT_MDY = '%m/%d/%Y'
DATE_FORMAT_DMY = '%d/%m/%Y'
ONE_DAY = datetime.timedelta(days=-1)

class Record:
    def __init__(self, price, **args):
        self.price = price
        date = args['date'] if 'date' in args else None
        mdy = args['mdy'] if 'mdy' in args else None
        dmy = args['dmy'] if 'dmy' in args else None
        if date is None and mdy is None and dmy is None:
            print("Invalid object - Date, mdy, dmy are all None")
            sys.exit()
        if mdy is not None:
            self.date = self.toDate(mdy, DATE_FORMAT_MDY)
            if dmy:
                d = self.toDate(dmy, DATE_FORMAT_DMY)
            if self.date != d:
                print("Dates not equal %s %s" % (mdy, dmy))
                sys.exit()
        elif dmy is not None:
            self.date = self.toDate(dmy, DATE_FORMAT_DMY)
        else:
            self.date = date

    def toDate(self, mdy, date_format):
        return datetime.datetime.strptime(mdy, date_format)

    def __str__(self):
        return "p:%s, d:%s" % (self.price, self.date.strftime(DATE_FORMAT_MDY))

class Processor:
    def __init__(self, inputfile, outputfile, verbosity):
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.verbosity = verbosity

    def generateMissingRecords(self, start, end):
        if self.verbosity: print("Generating missing between %s, %s" % (start,end))
        missing = []
        if (start.date <= end.date):
            print("Dates not sorted or duplicate dats: %s %s", (
                start.date.strftime(DATE_FORMAT_MDY), end.date.strftime(DATE_FORMAT_MDY)))
            sys.exit()
        ONE_DAY
        curr = start
        while curr.date + ONE_DAY > end.date:
            next_val = Record(start.price, date=(curr.date + ONE_DAY))
            if self.verbosity: print("Created record %s" % next_val)
            missing.append(next_val)
            curr = next_val
        return missing
    
    def addMissingRecords(self, records):
        updated = []
        prev = None
    
        for index, record in enumerate(records):
            if not updated:
                updated.append(record)
                prev = record
                continue
            if record.date == (prev.date + ONE_DAY):
                updated.append(record)
            elif prev.date != record.date:
                missing = self.generateMissingRecords(prev, record)
                if self.verbosity: print("Generated %d records" % len(missing))
                updated.extend(missing)
                updated.append(record)
            prev = record
        return updated
    
    def printRecords(self, records):
        for rec in records:
            print("Got record [%s, %s]" % (rec.date, rec.price))

    def writeOutputFile(self, records):
        lines = []
        for rec in records:
            lines.append([rec.date.strftime(DATE_FORMAT_MDY), rec.date.strftime(DATE_FORMAT_DMY), rec.price])
        with open(self.outputfile, "w") as f:
            writer=csv.writer(f)
            writer.writerows(lines)

    def processInputFile(self):
        lines = []
        print("Reading file %s" % self.inputfile)
        skip = True
        records = []
        with open(self.inputfile, "r", newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if skip:
                    skip = False
                    continue
                rec = Record(row[1], dmy=row[0])
                records.append(rec)
        if self.verbosity: self.printRecords(records)
        records = self.addMissingRecords(records)
        if self.verbosity: self.printRecords(records)
        self.writeOutputFile(records)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input", help="File to parse")
    parser.add_argument("-o", "--output", help="File to write")
    parser.add_argument("-v", "--verbose", help="Verbose logging")
    args = parser.parse_args()
    print("Input file: %s" % args.input)
    processor = Processor(args.input, args.output, args.verbose)
    processor.processInputFile()

main()
    
    
        

    
