from rdflib import Namespace, URIRef, Graph


class Queryp2:
    def __init__(self, theGraph):
        self.graph = theGraph

    #This is the sparql query that gets run for query 1
    def queryOne(self, courseCode, courseNumber):
        theCourseCode = str(courseCode)
        theCourseNumber = str(courseNumber)
        theTriples = self.graph.query(
            """SELECT ?description
               WHERE 
               {
               {?s  <http://focu.io/schema#courseSubject> \"%s\".}
               {?s  <https://schema.org/courseCode> \"%s\".}
               {?s  <https://schema.org/about> ?description.}
               }
               """ % (theCourseCode, theCourseNumber))
        for row in theTriples:
            #This is to remove the pre-requisites from the description
            #The pre-requistics is kepts in the decription since it is included on the website but for this
            #query it is not needed.

            startingIndex = (row.description.find('.') + 2)
            endingIndex = (row.description.rfind('.') + 1)
            theDescription = row.description[startingIndex:endingIndex]

        if len(theTriples.result) == 0:
            print("%s %s does not exist at Concordia" %(courseCode, courseNumber))
            return

        print("%s %s is about:\n%s" % (theCourseCode, theCourseNumber, theDescription))

    #This is the sparql query that gets run if the student's first name and last name is entered
    def queryTwoWithName(self, firstName, lastName):
        theFirstName = str(firstName.title())
        theLastName = str(lastName.title())
        theTriples = self.graph.query(
            """SELECT ?blankNode ?p ?o ?courseSubject ?CourseID
               WHERE 
               {
               {?s  <http://xmlns.com/foaf/0.1/firstName> \"%s\"}
               {?s  <http://xmlns.com/foaf/0.1/lastName> \"%s\"}
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseCode}
               {?courseCode  <http://focu.io/schema#courseSubject> ?courseSubject.}
               {?courseCode  <https://schema.org/courseCode> ?CourseID.}
               {?blankNode  ?p ?courseCode}
               {?courseCode  <http://xmlns.com/foaf/0.1/name> ?o}
               FILTER (?p != <http://focu.io/schema#takesCourse>)
               }
               """ % (theFirstName, theLastName))

        results = {}
        theRow = {}

        for row in theTriples:
            theValues = ["temp", "temp", "temp", "temp", "temp"]
            theRow[0] = str(row[0])
            if "got" in str(row[1]):
                theValues[0] = str(row[1])
                theValues[2] = str(row[2])
                theValues[3] = str(row[3])
                theValues[4] = str(row[4])
                if self.isKeyinDict(results, row[0]):
                    self.replaceKeyInDic(results, row[0], theValues[0], theValues[2], theValues[3], theValues[4])
                else:
                    results[row[0]] = tuple(theValues)
            elif "Semester" in str(row[1]):
                theValues[1] = str(row[1])
                theValues[2] = str(row[2])
                theValues[3] = str(row[3])
                theValues[4] = str(row[4])
                if self.isKeyinDict(results, row[0]):
                    self.replaceKeyInDic(results, row[0], theValues[1], theValues[2], theValues[3], theValues[4])
                else:
                    results[row[0]] = tuple(theValues)

        if len(theTriples.result) == 0:
            print("%s %s did not take any courses at Concordia." %(firstName, lastName))
            return

        for key in results:
            print("%s %s took %s %s (%s) in %s and %s an %s" % (
            theFirstName, theLastName, results[key][3], results[key][4], results[key][2],
            results[key][1].replace("_", " ").lower(), results[key][0][:3], results[key][0][3:]))

    #This is the sparql query that gets run if the student's ID is entered
    def queryTwoWithID(self, studentID):
        theTriples = self.graph.query(
            """SELECT ?blankNode ?p ?o ?courseSubject ?CourseID
               WHERE 
               {
               {?s  <http://xmlns.com/foaf/0.1/account> %s}
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseCode}
               {?courseCode  <http://focu.io/schema#courseSubject> ?courseSubject.}
               {?courseCode  <https://schema.org/courseCode> ?CourseID.}
               {?blankNode  ?p ?courseCode}
               {?courseCode  <http://xmlns.com/foaf/0.1/name> ?o}
               FILTER (?p != <http://focu.io/schema#takesCourse>)
               }
               """ % (studentID))

        results = {}
        theRow = {}

        for row in theTriples:
            theValues = ["temp", "temp", "temp", "temp", "temp"]
            theRow[0] = str(row[0])
            if "got" in str(row[1]):
                theValues[0] = str(row[1])
                theValues[2] = str(row[2])
                theValues[3] = str(row[3])
                theValues[4] = str(row[4])
                if self.isKeyinDict(results, row[0]):
                    self.replaceKeyInDic(results, row[0], theValues[0], theValues[2], theValues[3], theValues[4])
                else:
                    results[row[0]] = tuple(theValues)
            elif "Semester" in str(row[1]):
                theValues[1] = str(row[1])
                theValues[2] = str(row[2])
                theValues[3] = str(row[3])
                theValues[4] = str(row[4])
                if self.isKeyinDict(results, row[0]):
                    self.replaceKeyInDic(results, row[0], theValues[1], theValues[2], theValues[3], theValues[4])
                else:
                    results[row[0]] = tuple(theValues)

        if len(theTriples.result) == 0:
            print("Student %s did not take any courses at Concordia." % studentID)
            return

        for key in results:
            print("The student with ID %s took %s %s (%s) in the %s and %s an %s"
                  % (studentID, results[key][3], results[key][4], results[key][2],
                     results[key][1].replace("_", " ").lower(), results[key][0][:3], results[key][0][3:]))

    #This is the sparql query that gets run if the third query is selected
    def queryThree(self, givenTopic):
        theTopicInfo = str(givenTopic)
        topicURLAsIs = str("<http://www.example.org#" + theTopicInfo.replace(" ", "_") + ">")
        topicURLtoLower = str("<http://www.example.org#" + theTopicInfo.lower().replace(" ", "_") + ">")
        topicURLtoUpper = str("<http://www.example.org#" + theTopicInfo.title().replace(" ", "_") + ">")
        topicURLfirstUpper = str("<http://www.example.org#" + theTopicInfo.capitalize().replace(" ", "_") + ">")
        topicURLallUpper = str("<http://www.example.org#" + theTopicInfo.upper().replace(" ", "_") + ">")
        theTriples = self.graph.query(
            """SELECT DISTINCT ?CourseSubject ?CourseCode 
               WHERE 
               {
               {
               {?s  <http://focu.io/schema#courseSubject> ?CourseSubject.}
               {?s  <https://schema.org/courseCode> ?CourseCode.}
               {?s  <http://xmlns.com/foaf/0.1/topic> %s.}
               }
               UNION
               {
               {?s  <http://focu.io/schema#courseSubject> ?CourseSubject.}
               {?s  <https://schema.org/courseCode> ?CourseCode.}
               {?s  <http://xmlns.com/foaf/0.1/topic> %s.}
               }
               UNION
               {
               {?s  <http://focu.io/schema#courseSubject> ?CourseSubject.}
               {?s  <https://schema.org/courseCode> ?CourseCode.}
               {?s  <http://xmlns.com/foaf/0.1/topic> %s.}
               }
               UNION
               {
               {?s  <http://focu.io/schema#courseSubject> ?CourseSubject.}
               {?s  <https://schema.org/courseCode> ?CourseCode.}
               {?s  <http://xmlns.com/foaf/0.1/topic> %s.}
               }
               UNION
               {
               {?s  <http://focu.io/schema#courseSubject> ?CourseSubject.}
               {?s  <https://schema.org/courseCode> ?CourseCode.}
               {?s  <http://xmlns.com/foaf/0.1/topic> %s.}
               }
               }
               """ % (topicURLAsIs, topicURLtoLower, topicURLtoUpper, topicURLfirstUpper, topicURLallUpper))

        if len(theTriples.result) == 0:
            print("There aren't any courses that cover the topic %s." % givenTopic)
            return

        for row in theTriples:
            print("%s %s has the topic %s" % (row[0], row[1], givenTopic))

    #This is the sparql query that gets run if the fourth query is selected
    def queryFour(self, givenTopic):
        theTopicInfo= str(givenTopic)
        topicURLAsIs = str("<http://www.example.org#" + theTopicInfo.replace(" ", "_") + ">")
        topicURLtoLower = str("<http://www.example.org#" + theTopicInfo.lower().replace(" ", "_") + ">")
        topicURLtoUpper = str("<http://www.example.org#" + theTopicInfo.title().replace(" ", "_") + ">")
        topicURLfirstUpper = str("<http://www.example.org#" + theTopicInfo.capitalize().replace(" ", "_") + ">")
        topicURLallUpper = str("<http://www.example.org#" + theTopicInfo.upper().replace(" ", "_") + ">")
        theTriples = self.graph.query(
            """SELECT DISTINCT ?studentID
               WHERE 
               {
               {
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode.}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseID.}
               {?blankNode <http://focu.io/schema#gotA>|<http://focu.io/schema#gotB>|<http://focu.io/schema#gotC>|<http://focu.io/schema#gotD> ?courseID.}
               {?courseID <http://xmlns.com/foaf/0.1/topic> %s.}
               {?s  <http://xmlns.com/foaf/0.1/account> ?studentID.}
               }
                              UNION
               {
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode.}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseID.}
               {?blankNode <http://focu.io/schema#gotA>|<http://focu.io/schema#gotB>|<http://focu.io/schema#gotC>|<http://focu.io/schema#gotD> ?courseID.}
               {?courseID <http://xmlns.com/foaf/0.1/topic> %s.}
               {?s  <http://xmlns.com/foaf/0.1/account> ?studentID.}
               }
                              UNION
               {
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode.}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseID.}
               {?blankNode <http://focu.io/schema#gotA>|<http://focu.io/schema#gotB>|<http://focu.io/schema#gotC>|<http://focu.io/schema#gotD> ?courseID.}
               {?courseID <http://xmlns.com/foaf/0.1/topic> %s.}
               {?s  <http://xmlns.com/foaf/0.1/account> ?studentID.}
               }
                              UNION
               {
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode.}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseID.}
               {?blankNode <http://focu.io/schema#gotA>|<http://focu.io/schema#gotB>|<http://focu.io/schema#gotC>|<http://focu.io/schema#gotD> ?courseID.}
               {?courseID <http://xmlns.com/foaf/0.1/topic> %s.}
               {?s  <http://xmlns.com/foaf/0.1/account> ?studentID.}
               }
                              UNION
               {
               {?s  <http://focu.io/schema#enrolledIn> ?blankNode.}
               {?blankNode  <http://focu.io/schema#takesCourse> ?courseID.}
               {?blankNode <http://focu.io/schema#gotA>|<http://focu.io/schema#gotB>|<http://focu.io/schema#gotC>|<http://focu.io/schema#gotD> ?courseID.}
               {?courseID <http://xmlns.com/foaf/0.1/topic> %s.}
               {?s  <http://xmlns.com/foaf/0.1/account> ?studentID.}
               }
               }
               """ % (topicURLAsIs, topicURLtoLower, topicURLtoUpper, topicURLfirstUpper, topicURLallUpper))

        if len(theTriples.result) == 0:
            print("There are not students who are familiar with the topic %s." % givenTopic)

        for row in theTriples.result:
            print("Student ID %s is familiar with the topic %s." % (row[0], givenTopic))

    #This is a method used for query 2 to be able to connect the grade and the semester
    def isKeyinDict(self, dictionary, key):
        if key in dictionary.keys():
            return True
        return False

    # This is a method used for query 2 to be able to connect the grade and the semester
    def replaceKeyInDic(self, dictionary, key, newValue1, newValue2, old3, old4):
        temp = []
        if (dictionary[key][0] == "temp"):
            firstString = newValue1
            hashIndex1 = firstString.index("#") + 1
            hashIndex2 = dictionary[key][1].index("#") + 1
            temp = [str(firstString[hashIndex1:]), str(dictionary[key][1][hashIndex2:]), str(newValue2), str(old3), str(old4)]
        elif (dictionary[key][1] == "temp"):
            theSemester = newValue1
            hashIndex1 = theSemester.index("#") + 1
            hashIndex2 = dictionary[key][0].index("#") + 1
            temp = [str(dictionary[key][0][hashIndex1:]), str(theSemester[hashIndex2:]), str(newValue2), str(old3), str(old4)]

        del dictionary[key]
        dictionary[key] = tuple(temp)
        return dictionary