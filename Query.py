from rdflib import Namespace, URIRef, Graph


class Query:
    def __init__(self, theGraph):
        self.graph = theGraph
        self.newGraph = Graph()

    def queryOne(self):
        theTriples = self.graph.query(
            """SELECT (COUNT(*) as ?TriplesTotal)
               WHERE {
                  ?s ?p ?o.
               }""")

        allTriples = open("output/QueryResults/q1-out.txt", "w")

        for row in theTriples:
            print("The total number of triples are %s" % row)
            allTriples.write("Total number of triples: %s" % row)

        print("The output was also generated in output/QueryResults/q1-out.txt")
        allTriples.close()

    def queryTwo(self):
        allTriples = open("output/QueryResults/q2-out.txt", "w")

        # To get the number of students
        theTriples = self.graph.query(
            """SELECT (COUNT(*) as ?TriplesStudents)
               WHERE 
               {
                  ?s <http://xmlns.com/foaf/0.1/schoolHomepage> ?aUniversity.
               }""")

        for row in theTriples:
            print("Total number of students: %s" % row)
            allTriples.write("Total number of students: %s" % row)
            allTriples.write("\n")

        # To get the number of courses
        theTriples = self.graph.query(
            """SELECT (COUNT(*) as ?TriplesCourses)
               WHERE {
                  {?s <https://schema.org/courseCode> ?courseCode.}
               }""")

        for row in theTriples:
            print("Total number of courses: %s" % row)
            allTriples.write("Total number of courses: %s" % row)
            allTriples.write("\n")

        # To get the number of topics
        theTriples = self.graph.query(
            """SELECT (COUNT(*) as ?TriplesTopics)
               WHERE {
                  {?s  <http://focu.io/schema#topicLink> ?topicName.}
               }""")

        for row in theTriples:
            print("Total number of topics: %s" % row)
            allTriples.write("Total number of topics: %s" % row)
            allTriples.write("\n")

        theTriples = self.graph.query(
            """SELECT (COUNT(*) as ?TriplesTotal)
               WHERE
               {
               {?s1 <http://xmlns.com/foaf/0.1/schoolHomepage> ?o1.}
               UNION
               {?s2 <http://focu.io/schema#courseSubject> ?o2.}
               UNION
               {?s3 <http://focu.io/schema#topicLink> ?o3.}
               }
               """)

        for row in theTriples:
            print("The total number of triples for students, courses, and topics are %s" % row)
            allTriples.write("\n")

        print("The output was also generated in output/QueryResults/q2-out.txt")
        allTriples.close()

    def queryThree(self, name, code):
        courseSubject = str(name)
        courseCode = str(code)
        theTriples = self.graph.query(
            """SELECT ?topicName ?topicURL
               WHERE 
               {
               {?s  <https://schema.org/courseCode> \"%s\".}
               {?s  <http://focu.io/schema#courseSubject> \"%s\".}
               {?s <http://xmlns.com/foaf/0.1/topic> ?topicName.}
               {?topicName <http://focu.io/schema#topicLink> ?topicURL.}
               }
               """ % (courseCode, courseSubject))
        numberOfTriples = 0

        allTriples = open("output/QueryResults/q3-out.txt", "w")

        for row in theTriples.result:
            print("%s is the label for the URL %s" % row)
            numberOfTriples = numberOfTriples + 1
            allTriples.write(str(row))
            allTriples.write("\n")

        numberOfTopics = numberOfTriples
        print("Total number of topics: %s" % numberOfTopics)
        allTriples.write("Total number of topics: %s" % numberOfTopics)
        allTriples.write("\n")
        print("The output was also generated in output/QueryResults/q3-out.txt")
        allTriples.close()

    def queryFour(self, firstName, lastName):
        theFirstName = str(firstName)
        theLastName = str(lastName)
        theTriples = self.graph.query(
            """SELECT ?blankNode ?p ?o
               WHERE 
               {
               {?s  <http://xmlns.com/foaf/0.1/firstName> \"%s\"}
               {?s  <http://xmlns.com/foaf/0.1/lastName> \"%s\"}
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseID}
               {?blankNode  ?p ?courseID}
               {?courseID  <http://xmlns.com/foaf/0.1/name> ?o}
               FILTER (?p != <http://focu.io/schema#takesCourse>)
               }
               """ % (theFirstName, theLastName))

        results = {}
        theRow = {}

        allTriples = open("output/QueryResults/q4-out.txt", "w")

        for row in theTriples.result:
            allTriples.write(str(row))
            theValues = ["temp", "temp", "temp"]
            theRow[0] = str(row[0])
            if "got" in str(row[1]):
                theValues[0] = str(row[1])
                theValues[2] = str(row[2])
                if self.isKeyinDict(results, row[0]):
                    self.replaceKeyInDic(results, row[0], theValues[0], theValues[2])
                else:
                    results[row[0]] = tuple(theValues)
            elif "Semester" in str(row[1]):
                theValues[1] = str(row[1])
                theValues[2] = str(row[2])
                if self.isKeyinDict(results, row[0]):
                    self.replaceKeyInDic(results, row[0], theValues[1], theValues[2])
                else:
                    results[row[0]] = tuple(theValues)

        for key in results:
            print("This student took %s in %s and %s" % (results[key][2], results[key][1], results[key][0]))
            allTriples.write("This student took %s in %s and %s" % (results[key][2], results[key][1], results[key][0]))
            allTriples.write("\n")

        print("The output was also generated in output/QueryResults/q4-out.txt")

        allTriples.close()

    def queryFive(self, topic):
        theTopic = "<http://www.example.org#" + str(topic + ">")
        theTriples = self.graph.query(
            """SELECT ?studentID
               WHERE 
               {
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseID}
               {?blankNode <http://focu.io/schema#gotA>|<http://focu.io/schema#gotB>|<http://focu.io/schema#gotC>|<http://focu.io/schema#gotD> ?courseID}
               {?courseID <http://xmlns.com/foaf/0.1/topic> %s}
               {?s  <http://xmlns.com/foaf/0.1/account> ?studentID}
               }
               """ % theTopic)

        allTriples = open("output/QueryResults/q5-out.txt", "w")

        for row in theTriples.result:
            print("Student ID %s is familiar with the topic " % row, end='')
            allTriples.write("Student ID %s is familiar with the topic " % row)
            print(topic + ".")
            allTriples.write(topic + ".")
            allTriples.write("\n")

        print("The output was also generated in output/QueryResults/q5-out.txt")
        allTriples.close()

    def querySix(self, firstName, lastName):
        theFirstName = str(firstName)
        theLastName = str(lastName)
        theTriples = self.graph.query(
            """SELECT DISTINCT ?allTopics ?topicURL
               WHERE 
               {
               {?s  <http://xmlns.com/foaf/0.1/firstName> \"%s\"}
               {?s  <http://xmlns.com/foaf/0.1/lastName> \"%s\"}
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode}
               {?blankNode <http://focu.io/schema#gotA>|<http://focu.io/schema#gotB>|<http://focu.io/schema#gotC>|<http://focu.io/schema#gotD> ?courseID}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseID}
               {?courseID  <http://xmlns.com/foaf/0.1/topic> ?allTopics}
               {?allTopics <http://focu.io/schema#topicLink> ?topicURL}
               }
               """ % (theFirstName, theLastName))

        allTriples = open("output/QueryResults/q6-out.txt", "w")
        print("Displaying all topics that %s %s is familiar with based off his/her completed and passed courses:" % (
        theFirstName, theLastName))
        for row in theTriples.result:
            hashIndex1 = (str(row[0])).index("#") + 1
            topicName = str(row[0][hashIndex1:])
            topicURL = str(row[1])
            print("Topic is %s and URL is: %s" % (topicName, topicURL))
            allTriples.write("Topic is %s and URL is: %s" % (topicName, topicURL))
            allTriples.write("\n")

        print("The output was also generated in output/QueryResults/q6-out.txt")

        allTriples.close()

    def querySeven(self, query):
        theQuery = str(query)
        theTriples = self.graph.query("""%s""" % theQuery)

        for row in theTriples.result:
            print(row)

    def isKeyinDict(self, dictionary, key):
        if key in dictionary.keys():
            return True
        return False

    def replaceKeyInDic(self, dictionary, key, newValue1, newValue2):
        temp = []
        if (dictionary[key][0] == "temp"):
            firstString = newValue1
            hashIndex1 = firstString.index("#") + 1
            hashIndex2 = dictionary[key][1].index("#") + 1
            temp = [str(firstString[hashIndex1:]), str(dictionary[key][1][hashIndex2:]), str(newValue2)]
        elif (dictionary[key][1] == "temp"):
            theSemester = newValue1
            hashIndex1 = theSemester.index("#") + 1
            hashIndex2 = dictionary[key][0].index("#") + 1
            temp = [str(dictionary[key][0][hashIndex1:]), str(theSemester[hashIndex2:]), str(newValue2)]

        del dictionary[key]
        dictionary[key] = tuple(temp)
        return dictionary
