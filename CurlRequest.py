import pycurl
from io import BytesIO


def curlRequest(s):
    buffer = BytesIO()
    print(type(s))
    print(s)
    s = s.replace(" ", "%20")
    s = s.replace("'", "%E2%80%99")
    s = s.replace("\t", "")
    request = "http://localhost:2222/rest/annotate?text=" + s.encode("ascii", errors="ignore").decode()
    # request = "https://api.dbpedia-spotlight.org/en/annotate?text=" + b;
    print(request)
    crl = pycurl.Curl()
    crl.setopt(crl.URL, request)
    crl.setopt(pycurl.HTTPHEADER, ['accept: application/json'])
    crl.setopt(pycurl.CUSTOMREQUEST, "GET")
    crl.setopt(crl.WRITEDATA, buffer)
    crl.perform()
    crl.close()
    result = buffer.getvalue().decode('utf-8')
    print(result)
    print(type(result))
    dict = {}
    try:
        result = result[result.index("[")+1:result.index("]"):1].split("},")
        key = ""
        value = ""
        for single_result in result:
            items = single_result.split("\",")
            for item in items:
                if (item.startswith("\"@surfaceForm")):
                    key = item[item.index(":") + 2:]
                    print(key)
                if (item.startswith("{\"@URI")):
                    value = item[item.index(":") + 2:]
                    print(value)
            dict[key] = value
    except ValueError:
        pass

    for x, y in dict.items():
        print(x, y)

    return dict

# curlRequest("Concordia advanced six spots to 10th place among Canada's engineering schools in the Maclean's 2018 Program Rankings, while computer science advanced three spots into 11th position this year")
# curlRequest("TOPICS IN SOFTWARE ENGINEERING 1 - 	SOFTWARE RE-ENGINEERING")

def id_keywords_uri_pair(id_description_dict):
    id_keywords = {}
    for id in id_description_dict:
        id_keywords[id] = curlRequest(id_description_dict[id])
        print(id_keywords[id])

    fo = open("id_keywords_uri.txt", "w")
    for x, y in id_keywords.items():
        for y1, y2 in y.items():
            fo.write(x + " " + y1 + " " + y2 + "\n")
    fo.close()

    return id_keywords


