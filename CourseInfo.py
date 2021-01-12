import pandas as pd
import re
import urllib.request
from bs4 import BeautifulSoup
from CurlRequest import id_keywords_uri_pair


def generateCourseInfo(src="input/CU_SR_OPEN_DATA_CATALOG.csv", dest="output/course_info.csv",
                       UGRD_desc="output/UGRD_descriptions.txt", GRAD_desc="output/GRAD_descriptions.txt",
                       BACKUP_desc="input/BACKUP_descriptions.txt", dictionary_path="output/id_descriptions.txt"):

    # Extract useful columns from input CSV file
    fields = ["Course ID", "Subject", "Catalog", "Long Title", "Career"]
    df = pd.read_csv(src, names=fields, index_col="Course ID", usecols=[0, 1, 2, 3, 8], encoding="latin1")
    df = df[1:]

    # Drop rows with duplicate course numbers
    df = df[~df.index.duplicated()]

    # Add a ew col and renames cols
    df["Course Description"] = ""
    df.rename(columns={"Subject":"Course Subject", "Catalog":"Course Number",
                       "Long Title":"Course Name", "Career":"Career"}, inplace=True)
    # print(df)

    # create a dictionary with id as key, description as value
    id_description = {}

    # Open course description file and read all the content
    # try:
    f1 = open(UGRD_desc, "r", encoding="utf-8")
    f2 = open(GRAD_desc, "r", encoding="utf-8")
    f3 = open(BACKUP_desc, "r", encoding="utf-8")
    content1 = f1.readlines()
    content2 = f2.readlines()
    backup = f3.read()

    counter = 0

    for id in df.index:
        description = ""
        # print("\n" + id)
        course_title = df.loc[id, "Course Subject"] + " " + df.loc[id, "Course Number"]
        print(course_title)
        course_name = df.loc[id, "Course Name"]  # added by Lexie
        print(type(df.loc[id, 'Course Name']))  # added by Lexie
        if "also listed as" in df.loc[id, 'Course Name']:  # added by Lexie
            course_name = course_name[course_name.index(")") + 2:]
        course_name = course_name.strip()
        print(course_name)
        if df.loc[id, "Career"] == "UGRD":
            description = get_description(id, course_title, content1, backup)
        else:
            description = get_description(id, course_title, content2, backup)
        print(description)
        # if description == "" or description[:10] == "Please see":
        #     counter += 1
        id_description[id] = course_name + ": " + description        # added by Lexie
        print(id_description[id])
        df.loc[id, 'Course Description'] = description

    f1.close()
    f2.close()
    f3.close()

    # except:
    #     pass

    # Saving and writing to a new CSV file
    # If file exists, need to close the file to save
    # print(df)
    df.to_csv(dest, encoding="utf-8-sig")

    fo = open(dictionary_path, "w", encoding="utf-8")
    for x, y in id_description.items():
        fo.write(x + "  " + y + "\n")
    fo.close()

    return id_description


# Get course description for ONE specific course
def get_description(id, course_title, content, backup):

    description = ""

    for i in range(len(content)-1):
        line = content[i]
        if course_title in line:
            if "dits" in line[-7:]:
                for j in range(i + 1, min(i+4, len(content))):
                    if len(content[j]) > 10:
                        next_line_title = re.search("[A-Z]{3,4}\s[0-9]{3,4}", content[j][0:10])
                        if next_line_title is None:
                            if content[j][0:4] != "NOTE" and content[j][0:4] != "Note":
                                description += content[j].strip()
                        else:
                            break
                break

    # Go search in back up file
    if description == "":
        if id in backup:
            rest = backup.split(id)[1]
            start = re.search("[A-Z|À-Ÿ][a-z]", rest).end() - 2
            end = rest.find("\"}")
            description = rest[start:end]

    return description.strip()


# Collect ALL course descriptions for both UGRD and GRAD from the web
def collect_course_descriptions(desc_file_path, url):

    GRAD = False
    if len(url) > 1:
        GRAD = True

    f = open(desc_file_path, "a", encoding="utf-8")
    url_list = []

    for u in url:
        # init BeautifulSoup object to read html page
        html = urllib.request.urlopen(u).read()
        soup = BeautifulSoup(html, features="html.parser")

        # collect a list of urls of course description pages
        for a in soup.find_all('a', href=True):
            if not GRAD:
                found = a['href'].find("current/sec")
                if found != -1 and a['href'].endswith("html"):
                    if int(a['href'][found+11: found+13]) >= 24 and int(a['href'][found+11: found+13]) != 25:
                        url_list.append("http://www.concordia.ca" + a['href'])
            else:
                found = a['href'].find(u[23:-5] + "/")
                if found != -1:
                    url_list.append("http://www.concordia.ca" + a['href'])

    # parse each course description page
    for u in url_list:
        print(u)
        start = end = 0

        # init BeautifulSoup object to read each html page
        html = urllib.request.urlopen(u).read()
        soup = BeautifulSoup(html, features="html.parser")

        # get rid of all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        for line in text.splitlines():

            if start == 0:
                found_title = line.find("dits)")
                if found_title != -1:
                    matched = re.search("[A-Z]{3}", line[0:3])
                    if matched:
                        start = text.index(line)
                        # print("START:")
                        # print(line)
            if start != 0:
                if not GRAD:
                    if line == "2019‑20 Concordia University Undergraduate Calendar":
                        end = text.index(line)
                        # print("END:")
                        # print(line)
                        break
                else:
                    if line == "Back to top":
                        end = text.index(line)
                        # print("END:")
                        # print(line)
                        break
        f.write(text[start:end])

    f.close()

if __name__ == "__main__":

    # Undergrad Course Descriptions:
    ugrd_url = ["http://www.concordia.ca/academics/undergraduate/calendar/current/courses-quick-links.html"]
    UGRD_description_file = "output/UGRD_descriptions.txt"
    collect_course_descriptions(UGRD_description_file, ugrd_url)

    # Graduate Course Descriptions:
    fasc_url = "http://www.concordia.ca/academics/graduate/calendar/current/fasc.html"
    encs_url = "http://www.concordia.ca/academics/graduate/calendar/current/encs.html"
    fofa_url = "http://www.concordia.ca/academics/graduate/calendar/current/fofa.html"
    jmsb_url = "http://www.concordia.ca/academics/graduate/calendar/current/jmsb.html"
    sgs_url = "http://www.concordia.ca/academics/graduate/calendar/current/sgs.html"
    grad_url = [fasc_url, encs_url, fofa_url, jmsb_url, sgs_url]
    GRAD_description_file = "output/GRAD_descriptions.txt"
    collect_course_descriptions(GRAD_description_file, grad_url)

    dict = generateCourseInfo(src="input/CU_SR_OPEN_DATA_CATALOG.csv", dest="output/course_info.csv",
                       UGRD_desc="output/UGRD_descriptions.txt", GRAD_desc="output/GRAD_descriptions.txt",
                       BACKUP_desc="input/BACKUP_descriptions.txt", dictionary_path="output/id_description.txt")

    id_keywords_uri_pair(dict)
