import requests
import csv
import os
from lxml import etree
from bs4 import BeautifulSoup

semester_translation = {0: "winter",
                        1: "summer",
                        2: "fall"}

def create_url_tuple_list(start_year, start_semester, end_year, end_semester):
    start_year = max(start_year, 2013)
    result = []
    
    if start_year < end_year:
        for semester in range(start_semester, 3):
            result.append(create_url_tuple(start_year, semester))
        
        for year in range(start_year + 1, end_year):
            for semester_id in range(0, 3):
                result.append(create_url_tuple(year, semester_id))

        for semester in range(0, end_semester + 1):
            result.append(create_url_tuple(end_year, semester))
            
        return result
    
    elif start_year == end_year:
        for semester in range(start_semester, end_semester + 1):
            result.append(create_url_tuple(end_year, semester))

        return result


    return result
        

#tuple format: (year, semester, url)
def create_url_tuple(year, semester_id):
    semester = semester_translation[semester_id]
    return (year, semester, "https://service.scs.carleton.ca/cu-course-outline?field_course_term_value=" + semester.capitalize() + "&field_course_year_value=" + str(year))


def crawl(url_tuple):
    result = []

    try:
        page = requests.get(url_tuple[2])
        soup = BeautifulSoup(page.content, "html.parser")
        content_area = soup.find(id = "content-area")
        course_elements = content_area.find_all("div", class_ = "views-row")
        
        for course_element in course_elements:
            course_code = course_element.select('[style*="width: 160px"]')[0].get_text(strip=True, separator='-')
            if "-" in course_code:
                carleton_code, uottawa_code = course_code.split('-', 1)
            else:
                carleton_code, uottawa_code = course_code, None
            try:
                course_name = course_element.select('[style*="width: 465px"]')[0].get_text()
            except:
                #some pages have course title elements with width 365px
                course_name = course_element.select('[style*="width: 365px"]')[0].get_text()
            professor = course_element.select('[style*="width: 175px"]')[0].get_text()
            try:
                outline_link = course_element.select('[style*="width: 100px"]')[0].find_all('a', class_ = "cu_outline")[0]['href']
            except:
                outline_link = None
                
            result.append((carleton_code, uottawa_code, course_name, professor, outline_link))
    except:
        pass

    return result


def crawl_all(url_tuple_list):
    header = ["year", "semester", "carleton_code", "uottawa_code", "course_name", "professor", "outline_link"]
    try:
        os.mkdir("csv")
    except:
        pass

    address = "csv/all.csv"
    with open(address, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for url_tuple in url_tuple_list:
            result = crawl(url_tuple)
            print("Currently crawling " + str(url_tuple[0]) , url_tuple[1] + " page.")
            #address = "csv/" + str(url_tuple[0]) + url_tuple[1] + ".csv"
            for line in result:
                try:
                    writer.writerow((url_tuple[0], url_tuple[1], line[0], line[1], line[2], line[3], line[4]))       
                except:
                    print(url_tuple, line)

    file.close()

crawl_all(create_url_tuple_list(2013, 0, 2023, 1))
