# sa-elections-2024
2024 South African election results data scraped from the IEC dashboard and cleaned up to make it easier to work with.

## Input Data:

Municipalities were scraped from StatsSA (https://www.statssa.gov.za/?page_id=4542) and saved to data/municipalities.csv. Data were manually updated to match the expected values on the IEC results download page.

## Downloads:
The download paths were found by going to the NPE Results page and selecting:
    
* For Step 1: Election type: Provincial / Regional / National, Year: 2024, 
* For Step 2: Detailed Results
* For Step 3: Select a province and the 'All' option for municipalities
* and then finally inspecting the button to download the results in excel.

URL Structure was found to be

### National
* https://results.elections.org.za/home/NPEPublicReports/1334/National%20Ballot/Results%20Report/EC/EC.xls
* https://results.elections.org.za/home/NPEPublicReports/1334/National%20Ballot/Results%20Report/EC/BUF/BUF.xls
* https://results.elections.org.za/home/NPEPublicReports/1334/National%20Ballot/Results%20Report/EC/BUF/10590016.xls

### Regional:
* https://results.elections.org.za/home/NPEPublicReports/1334/Regional%20Ballot/Results%20Report/EC/EC.xls
* https://results.elections.org.za/home/NPEPublicReports/1334/Regional%20Ballot/Results%20Report/EC/BUF/BUF.xls
* https://results.elections.org.za/home/NPEPublicReports/1334/Regional%20Ballot/Results%20Report/EC/BUF/10590016.xls

### Provincial
* https://results.elections.org.za/home/NPEPublicReports/1335/Results%20Report/EC/EC.xls
* https://results.elections.org.za/home/NPEPublicReports/1335/Results%20Report/EC/BUF/BUF.xls
* https://results.elections.org.za/home/NPEPublicReports/1335/Results%20Report/EC/BUF/10590016.xls

## Simplified:
There's a different base url for national,  regional and provincial results.

For national it is:
`https://results.elections.org.za/home/NPEPublicReports/1334/National%20Ballot/Results%20Report/`

and for regional it is:
`https://results.elections.org.za/home/NPEPublicReports/1334/Regional%20Ballot/Results%20Report/`


and for provincial it is:
`https://results.elections.org.za/home/NPEPublicReports/1334/Regional%20Ballot/Results%20Report/`

### Getting results
To get results at a province level: 
`[Base]/[Province]/[Province].xls`

To get results at a municipality level: 
`[Base]/[Province]/[Municipality].xls`

To get results at a voting district level: 
`[Base]/[Province]/[Municipality]/[Voting District]`

