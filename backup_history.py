#!/usr/bin/python3
import os
import shutil
import time
import itertools

HISTORY_BACKUP_FILE = "/home/bhatia/.history/backup.txt"
BASH_HISTORY_FILE = "/home/bhatia/.bash_history"

def ReadHistoryFileLines(filename):
    mylines = {}
    with open(filename, "r") as f:
        for line1, line2 in itertools.zip_longest(*[f]*2):
            if line2 is not None:
                mylines[line2] = line1
    return mylines


def CreateBackupFile(filename, mydict):
    with open(filename, "w") as myfile:
        for key, value in sorted(mydict.items(), key=lambda item: item[1]):
            myfile.write("%s" % value)
            myfile.write("%s" % key)

def MergeHistory(history, backup):
    for key, value in history.items():
        if key not in backup:
            backup[key] = value
    
def main():
    history_lines = ReadHistoryFileLines(BASH_HISTORY_FILE)
    backup_lines = ReadHistoryFileLines(HISTORY_BACKUP_FILE)
    MergeHistory(history_lines, backup_lines)
    ts = time.time()
    shutil.copyfile(BASH_HISTORY_FILE, "%s.%d.bak" % (HISTORY_BACKUP_FILE, ts))
    CreateBackupFile(HISTORY_BACKUP_FILE, backup_lines)

main()
    
    
        

    
