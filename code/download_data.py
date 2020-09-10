import urllib.request
#csv_url = 'https://www2.census.gov/programs-surveys/popest/tables/2010-2019/state/asrh/sc-est2019-agesex-civ.csv'
#urllib.request.urlretrieve(csv_url, '../data/population-data.csv')

gzip_file = 'https://github.com/obastani/covid19demographics/raw/master/data/data.json.gz'
urllib.request.urlretrieve(gzip_file, '../data/data.json.gz')