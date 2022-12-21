import bs4, requests, csv
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# TODO special event dates? Might have to hardcode 
def parkrunClubReport(clubID,clubName,eventDate):    
    reportURL = f'https://www.parkrun.com/results/consolidatedclub/?clubNum={clubID}&eventdate={eventDate}'
    res = requests.get(reportURL,headers = {'user-agent':'Chrome/43.0.2357'})
    res.raise_for_status()
  
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    intro = soup.select('.floatleft p')             # first intro para within main body
    locations = soup.select('.floatleft h2')        # get parkrun locations from h2 headers
    indexTable = soup.select('.floatleft table')    # get each table
    tableRows = soup.select('.floatleft table tr')  # get rows within tables

    if intro == []:
        print('Could not find page.')
    else:
        # get date, number of runners data from into para
        introText=intro[0].getText()
        dateReport = introText.split(".")[0][-10::]
        # numberMembers = introText.split(".")[1].split(",")[1].replace("took part on this date","").strip()

        # loop name of parkrun, get table data for each MRR runner (position, gender position, name, run time)
        data = []
        startRow,lastRow=1,1                                                        # 1 to avoid header row
        for index,parkrun in enumerate(locations):
            startRow=lastRow
            lastRow+=len(indexTable[index].findAll(lambda tag: tag.name == 'tr'))   # increment lastRow by number of rows found in next table
            for row in tableRows[startRow:lastRow]:
                cols = row.findAll("td")
                if cols !=[] and cols[3].get_text().strip()==clubName.strip():
                    line={'Parkrun':parkrun.getText(),'Date':dateReport,'Position':cols[0].get_text(),'GenderPosition':cols[1].get_text(),'Name':cols[2].get_text(),'Time':cols[4].get_text()}
                    data.append(line)

    # output to csv file
    with open(f'parkrunData_{clubID}.csv','a',newline='') as outputFile:
        fieldnames = ['Parkrun','Date','Position','GenderPosition','Name','Time']
        outputDictWriter  = csv.DictWriter(outputFile,fieldnames=fieldnames)
        if outputFile.tell() == 0:
            outputDictWriter.writeheader()
        outputDictWriter.writerows(data)

    return outputFile

def clubReportToImage(csvFile,clubID):
    # TODO sizing/spacing of text could be made dynamic with number of rows  
    img = Image.open('MRRlogo.jpg')
    d1 = ImageDraw.Draw(img)
    with open(csvFile,'r') as inputFile:
        exampleReader = csv.reader(inputFile)
        x,y = 0,0
        font = ImageFont.truetype("arial.ttf", 16, encoding="unic")
        for row in exampleReader:
            d1.text((x, y), row[0], fill=(0, 0, 0),font=font)
            d1.text((x+450, y), row[1], fill=(0, 0, 0),font=font)
            d1.text((x+600, y), row[2], fill=(0, 0, 0),font=font)
            d1.text((x+700, y), row[3], fill=(0, 0, 0),font=font)
            d1.text((x+1020, y), row[4], fill=(0, 0, 0),font=font)
            d1.text((x+1330, y), row[5], fill=(0, 0, 0),font=font)
            y+=17
        img.save(f"parkrunReportImage_{clubID}.jpg")
    return

def main():
    #TODO: input validation
    clubID=input("Input your parkrun club ID:")
    clubName=input("Input your club name:")
    finalEventDate=input("Input your final parkrun event date (yyyy-MM-dd):")
    loops = input("Input how many events to go back (1 or more):")
    imageChoice = input("Do you want an image to be generated? (Y/N):")
    inputDate= datetime.strptime(finalEventDate, '%Y-%m-%d').strftime('%Y-%m-%d')

    for i in range(int(loops)):
        outputFile = parkrunClubReport(clubID,clubName,inputDate)
        inputDate = (datetime.strptime(inputDate, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')

    if imageChoice=="Y":
        clubReportToImage(outputFile.name,clubID)

if __name__ == '__main__':
    main()