# ParkrunClubReportScraper

Inputs:
- Club ID (can be found in consolidated report URL e.g. https://www.parkrun.com/results/consolidatedclub/?clubNum=21485)
- Club name for validating only members of that club are extracted
- Date of final event you want data for (in format yyyy-MM-dd)
- How many events to go back from the above date (e.g. 1 would only give one event, 2 would give the above and the previous week)
- Y/N flag of whether you want a branded image to be generated 

Outputs:
- csv file named parkrunData_ClubID.csv with fields Parkrun,Date,Position,GenderPosition,Name,Time
- jpg image of results data written onto logo image (if requested)
