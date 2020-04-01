import csv
import os
import shutil


RAW = './data/gov-pl/raw/'
COMBINED = './data/gov-pl/combined/'
CLEAN = './data/gov-pl/clean/'
PREFIX = 'codz'

def getFileFormat(year, month):
      return '{}_{}_{}.csv'.format(PREFIX, year, str(month).zfill(2))

def clearFolders():
      shutil.rmtree(COMBINED)
      shutil.rmtree(CLEAN)
      os.makedirs(COMBINED)
      os.makedirs(CLEAN)

def prepareFiles(year):
      for i in range(1, 13):
            file = getFileFormat(year, i)
            prepareCSV(RAW + file, CLEAN + file)

def prepareCSV(file, output):
      with open(file) as data_file:
            with open(output, "a") as clean_file:
                  for line in data_file:
                        clean_file.write(line.replace('\"', '').strip() + "\n")


def readDataFromFiles(year, station_ids):
      values = {}
      for id in station_ids:
            values[str(id)] = []
      for i in range(1, 13):
            file = getFileFormat(year, i)
            readData(file, station_ids, values)
      return values



def readData(file, station_ids, values):
      with open(CLEAN + file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                  id = row[0]
                  mm = row[6]
                  if int(id) in station_ids:
                        values[str(id)].append(float(mm))   


## Zwraca dane z roku w postaci słownika: { 'id': [dzien1, dzien2, dzien3, dzien4, ... dzien365] }
def Data(year, stations_ids):
      clearFolders()
      prepareFiles(year)
      values = readDataFromFiles(year, stations_ids)
      return values

