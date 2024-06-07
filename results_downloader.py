import os
import requests
import csv
from enum import Enum
# import urllib.request

#Ballot types
class Ballot(Enum):
    NATIONAL = "NATIONAL"
    PROVINCIAL = "PROVINCIAL"
    REGIONAL = "REGIONAL"

    @property
    def urlPrefix(self):
        # Base URL for downloading the result files.
        base_url = "http://results.elections.org.za/home/NPEPublicReports/"
        # URL parts for national, regional and provincial results.

        if self == Ballot.NATIONAL:
            url_national = "1334/National%20Ballot/Results%20Report/"
            return f'{base_url}{url_national}'
        elif self == Ballot.PROVINCIAL:
            url_provincial = "1335/Results%20Report/"
            return f'{base_url}{url_provincial}'
        elif self == Ballot.REGIONAL:
            url_regional = "1334/Regional%20Ballot/Results%20Report/"
            return f'{base_url}{url_regional}'
        else:
            raise Exception("Invalid type")
        

class DetailLevel(Enum):
    PROVENCE = "BY_PROVINCE"
    MUNICIPALITY = "BY_MUNICIPALITY"
    VOTING_DISTRICT = "BY_VOTING_DISTRICT"
     

download_folder = "download"

class ResultsDownloader:
    
    def __init__(self, ballot: Ballot):
        self.ballot = ballot


# Input data
data_folder = "data"
municipalities_file = "municipalities.csv"
municipalities = { "WP" : [] ,
              "EC" : [],
              "FS" : [],
              "GP" : [],
              "KN" : [],
              "NP" : [],
              "MP" : [],
              "NW" : [],
              "NC" : []
            }

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "http://results.elections.org.za/dashboards/npe/",
}

def load_data():
    datafile = os.path.join(data_folder, municipalities_file)
    col_municipality = 0
    col_province = 2
    with open(datafile, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in filereader:
            # print(row)
            province = row[col_province]
            mun = row[col_municipality]
            municipalities[province].append(mun)


# def download_results():
#     # For each province, download the results.
#     for province in municipalities.keys():
#         download_by_provence(province, type=Ballot.PROVINCIAL)
#         # Only downloads at a municipality level for now
#         for municipality in municipalities[province]:
#             download(f'{url}{url_provincial}{province}/{municipality}/{municipality}.xls', province, municipality, folder=provincial_folder)
#             download(f'{url}{url_regional}{province}/{municipality}/{municipality}.xls', province, municipality, folder=regional_folder)
#             download(f'{url}{url_national}{province}/{municipality}/{municipality}.xls', province, municipality, folder=national_folder)


def download_by_provence(province: str, type: Ballot):
    base_url = type.urlPrefix
    dest_folder = os.path.join(download_folder, type.name.lower())
    download(f'{base_url}{province}/{province}.xls', filename=f'{province}.xls', dest_folder=os.path.join(dest_folder, DetailLevel.PROVENCE.value.lower()))
    

def download_by_municipality(province: str, municipality: str, type: Ballot):
    base_url = type.urlPrefix
    dest_folder = os.path.join(download_folder, type.name.lower(), DetailLevel.MUNICIPALITY.value.lower(), province)
    filename = f'{municipality}.xls'
    download(f'{base_url}{province}\{filename}', folder=dest_folder)


def download_by_vd(province: str, municipality: str, voting_district:str, type: Ballot):
    raise NotImplementedError("Not implemented yet")
    # base_url = type.urlPrefix
    # dest_folder = os.path.join(download_folder, type.name.tolower(), DetailLevel.MUNICIPALITY.value.tolower(), province)
    # filename = f'{municipality}.xls'
    # download(f'{base_url}{province}\{filename}', folder=dest_folder)


def download(url: str, dest_folder: str, filename: str):
    file_path = os.path.join(dest_folder, filename)
    if not os.path.exists(file_path):
        r = requests.get(url, stream=True)
        if r.ok:
            print("saving to", os.path.abspath(file_path))
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(r.status_code, r.text))
            print("Download failed: {} ({}\{})".format(url, dest_folder, filename))
    else:
        print("File exists - Skipping", file_path)


# def download(url: str, province: str, municipality: str, folder: str):
#     dest_folder = os.path.join(download_folder, folder)
#     province_folder = os.path.join(dest_folder, province)
#     filename = f'{municipality}.xls'
#     file_path = os.path.join(province_folder, filename)
#     if not os.path.exists(file_path):
#         r = requests.get(url, stream=True)
#         if r.ok:
#             print("saving to", os.path.abspath(file_path))
#             with open(file_path, 'wb') as f:
#                 for chunk in r.iter_content(chunk_size=1024 * 8):
#                     if chunk:
#                         f.write(chunk)
#                         f.flush()
#                         os.fsync(f.fileno())
#         else:  # HTTP status code 4XX/5XX
#             # print("Download failed: status code {}\n{}".format(r.status_code, r.text))
#             print("{}: {}".format(province, municipality))
#     else:
#         print("File exists - Skipping", file_path)
        

# Creates the download folders if they do not exist
def create_folders():
    for folder in [Ballot.PROVINCIAL.value.lower(), Ballot.REGIONAL.value.lower(), Ballot.NATIONAL.value.lower()]:
        by_province_folder = os.path.join(download_folder, folder, DetailLevel.PROVENCE.value.lower())
        if not os.path.exists(by_province_folder):
            os.makedirs(by_province_folder)  # create province folder if it does not exist
        for detail_folder in [DetailLevel.MUNICIPALITY.value.lower(), DetailLevel.VOTING_DISTRICT.value.lower()]:
            for province in municipalities.keys():
                province_folder = os.path.join(download_folder, folder.lower(), detail_folder.lower(), province)
                if not os.path.exists(province_folder):
                    os.makedirs(province_folder)  # create province folder if it does not exist


def main():
    load_data()  # Load the municipalities data
    create_folders()  # Create the download folders if they do not exist

    # Gets a session object to persist cookies across requests. Probably not needed.
    s = requests.Session()
    s.headers.update(headers)
    r = s.get("http://results.elections.org.za/home/Downloads/NPE-Results/")
    # print(r.status_code, r.headers)

    # Download the results for each province.
    for province in municipalities.keys():
        # First at a provence level
        download_by_provence(province, type=Ballot.PROVINCIAL)
        download_by_provence(province, type=Ballot.REGIONAL)
        download_by_provence(province, type=Ballot.NATIONAL)
        # Then download at a municipality level
        # for municipality in municipalities[province]:
        #     download(f'{url}{url_provincial}{province}/{municipality}/{municipality}.xls', province, municipality, folder=provincial_folder)
        #     download(f'{url}{url_regional}{province}/{municipality}/{municipality}.xls', province, municipality, folder=regional_folder)
        #     download(f'{url}{url_national}{province}/{municipality}/{municipality}.xls', province, municipality, folder=national_folder)

if __name__ == "__main__":
    main()
