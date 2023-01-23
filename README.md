# ParkrunClubReportScraper

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
