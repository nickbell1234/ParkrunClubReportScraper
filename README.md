# ParkrunClubReportScraper
## main.py

Inputs:
- Club ID (can be found in consolidated report URL e.g. https://www.parkrun.com/results/consolidatedclub/?clubNum=21485) e.g. "21485"
- Club name for validating only members of that club are extracted e.g. "Manchester Road Runners"
- Date of final event you want data for (in format yyyy-MM-dd) e.g. "2022-12-31"
- How many events to go back from the above date (e.g. 1 would only give one event, 2 would give the above and the previous week) e.g. "1"
- Y/N flag of whether you want a branded image to be generated e.g. "Y"

Actions:
- A request is made to the report URL, and the HTML is parsed
- The relevant information (date, parkrun locations and results tables) is extracted
- A csv with headers is generated from this data
- If requested, a branded image is generated with results data written on. This uses logo.jpg as the base image.

Outputs:
- csv file named parkrunData_ClubID.csv with fields Parkrun,Date,Position,GenderPosition,Name,Time
- jpg image of results data written onto logo image (if requested)

## analysis.py
Inputs:
- csv file output from main.py 

Actions:
- Uses pandas library to analyse the dataset:
1. Top 10 quickest times
2. Top 10 unique quickest performers
3. Any first positions
4. Any first gender positions
5. Top 10 runners by lowest average position
6. Top 10 runners by lowest average time
7. Top 10 runners by most number of parkrun events
8. Top 10 runners by most number of parkrun locations
9. Top 10 runners by appearances at a single parkrun location
10. Top 10 runners by appearances at Peel parkrun
11. Total unique number of parkrun locations for the entire club
12. List of unique parkrun locations (where there was only 1 visitor)
13. Top 5 days by number of runners
