import csv
from datetime import datetime, timedelta
import bs4
import requests
from PIL import Image, ImageDraw, ImageFont

# TODO special event dates? Might have to hardcode
def parkrun_club_report(club_id,club_name,event_date):
    report_url = f'https://www.parkrun.com/results/consolidatedclub/?clubNum={club_id}&eventdate={event_date}'
    res = requests.get(report_url,headers = {'user-agent':'Chrome/43.0.2357'})
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    intro = soup.select('.floatleft p')             # first intro para within main body
    locations = soup.select('.floatleft h2')        # get parkrun locations from h2 headers
    index_table = soup.select('.floatleft table')    # get each table
    table_rows = soup.select('.floatleft table tr')  # get rows within tables

    if intro == []:
        print('Could not find page.')
    else:
        # get date, number of runners data from into para
        intro_text=intro[0].getText()
        date_report = intro_text.split(".")[0][-10::]
        # numberMembers = introText.split(".")[1].split(",")[1].replace("took part on this date","").strip()

        # loop parkrun, get table data for each runner
        data = []
        start_row,last_row=1,1                          # 1 to avoid header row
        for index,parkrun in enumerate(locations):
            start_row=last_row
            last_row+=len(index_table[index].findAll(lambda tag: tag.name == 'tr'))   # increment lastRow by number of rows found in next table
            for row in table_rows[start_row:last_row]:
                cols = row.findAll("td")
                if cols !=[] and cols[3].get_text().strip()==club_name.strip():
                    line={
                        'Parkrun':parkrun.getText(),
                        'Date':date_report,
                        'Position':cols[0].get_text(),
                        'GenderPosition':cols[1].get_text(),
                        'Name':cols[2].get_text(),
                        'Time':cols[4].get_text()}
                    data.append(line)
        return data

def output_to_csv(data,club_id):
    with open(f'parkrunData_{club_id}.csv','a',newline='') as output_file:
        fieldnames = ['Parkrun','Date','Position','GenderPosition','Name','Time']
        output_dictwriter  = csv.DictWriter(output_file,fieldnames=fieldnames)
        if output_file.tell() == 0:
            output_dictwriter.writeheader()
        output_dictwriter.writerows(data)

    return output_file

def club_report_to_image(csv_file,club_id):
    # TODO sizing/spacing of text could be made dynamic with number of rows
    img = Image.open('logo.jpg')
    drawing = ImageDraw.Draw(img)
    with open(csv_file,'r') as input_file:
        example_reader = csv.reader(input_file)
        x_coord,y_coord = 0,0
        font = ImageFont.truetype("arial.ttf", 16, encoding="unic")
        for row in example_reader:
            drawing.text((x_coord, y_coord), row[0], fill=(0, 0, 0),font=font)
            drawing.text((x_coord+450, y_coord), row[1], fill=(0, 0, 0),font=font)
            drawing.text((x_coord+600, y_coord), row[2], fill=(0, 0, 0),font=font)
            drawing.text((x_coord+700, y_coord), row[3], fill=(0, 0, 0),font=font)
            drawing.text((x_coord+1020, y_coord), row[4], fill=(0, 0, 0),font=font)
            drawing.text((x_coord+1330, y_coord), row[5], fill=(0, 0, 0),font=font)
            y_coord+=17
        img.save(f"parkrunReportImage_{club_id}.jpg")
    return

def main():
    #TODO: input validation
    club_id=input("Input your parkrun club ID:")
    club_name=input("Input your club name:")
    final_event_date=input("Input your final parkrun event date (yyyy-MM-dd):")
    loops = input("Input how many events to go back (1 or more):")
    image_choice = input("Do you want an image to be generated? (Y/N):")
    input_date= datetime.strptime(final_event_date, '%Y-%m-%d').strftime('%Y-%m-%d')

    for _ in range(int(loops)):
        output_data = parkrun_club_report(club_id,club_name,input_date)
        output_file = output_to_csv(output_data,club_id)
        input_date = (datetime.strptime(input_date,'%Y-%m-%d')-timedelta(days=7)).strftime('%Y-%m-%d')

    if image_choice=="Y":
        club_report_to_image(output_file.name,club_id)

if __name__ == '__main__':
    main()
    