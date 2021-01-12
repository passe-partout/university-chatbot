from rdflib import Namespace, URIRef, Graph
from rdflib.namespace import RDF, FOAF, RDFS, XSD
from rdflib.term import Literal, BNode


class Student:
    #Default constructor
    def __init__(self):
        self.theGraph = Graph()
        self.studentInfo = {}
        self.data = Namespace("http://www.example.org#")
        self.schema = Namespace('https://schema.org/')
        self.focu = Namespace('http://focu.io/schema#')

    #Constructor
    def __init__(self, dataNameSpace, schemaNameSpace, focuNameSpace, dbpediaNameSpace, otology):
        self.theGraph = Graph()
        self.data = dataNameSpace
        self.schema = schemaNameSpace
        self.focu = focuNameSpace
        self.dbpedia = dbpediaNameSpace
        self.otology = otology
        self.studentInfo = {}

    def returnGraph(self):
        return self.theGraph

    def createFile(self):
        self.readFile()
        self.addToGraph()
        self.addProperties()
        self.associateStudentsWithPerson()
        return self.theGraph

    def readFile(self):
        #Testing on a smaller file
        #file = open("Input/SmallerTestData/StudentInfoLess.txt")

        # The file with all 10 students
        file = open("Input/StudentInfo.txt")

        line = file.readline()
        while line:
            self.studentInfo = self.addToDictionary(line)
            line = file.readline()

    def addToGraph(self):
        counter = 0
        for key in self.studentInfo:
            counter = counter + 1
            theKey = key
            id = self.data + str(self.studentInfo[key][3])
            self.theGraph.add((URIRef(id), FOAF.schoolHomepage, (URIRef(self.dbpedia.Concordia_University))))
            data = {}
            data[counter] = BNode()
            for x in range(7):
                if x == 0:
                    self.theGraph.add((URIRef(id), FOAF.firstName, Literal(self.studentInfo[theKey][x])))
                elif x == 1:
                    self.theGraph.add((URIRef(id), FOAF.lastName, Literal(self.studentInfo[theKey][x])))
                elif x == 2:
                    self.theGraph.add((URIRef(id), FOAF.mbox, Literal(self.studentInfo[theKey][x])))
                elif x == 3:
                    self.theGraph.add((URIRef(id), FOAF.account, Literal(self.studentInfo[theKey][x], datatype=XSD.integer)))
                elif x == 4:
                    self.theGraph.add((URIRef(id), self.focu.enrolledIn, data[counter]))
                    courseID = self.data + str(self.studentInfo[theKey][x])
                    self.theGraph.add((data[counter], self.focu.takesCourse, URIRef(courseID)))
                elif x == 5:
                    self.addTripleForGrade(self.studentInfo[theKey][x], id, courseID, data[counter])
                elif x == 6:
                    self.addTriplesForSemester(self.studentInfo[theKey][x], id, courseID,data[counter])

    #This function is used to add all the properties to the graph
    def addProperties(self):
        self.createEnrolledProperty()
        self.createTakesCourseProperty()
        self.createGradeAProperty()
        self.createGradeBProperty()
        self.createGradeCProperty()
        self.createGradeDProperty()
        self.createGradeFProperty()
        self.createFall2019Property()
        self.createWinter2019Property()


    # To create a property that a student takes a course
    def createEnrolledProperty(self):
        self.theGraph.add((URIRef(self.focu.enrolledIn), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.enrolledIn), RDFS.label, Literal("WasEnrolledIn")))
        self.theGraph.add((URIRef(self.focu.enrolledIn), RDFS.comment, Literal("links a student with a blank node")))
        self.theGraph.add((URIRef(self.focu.enrolledIn), RDFS.domain, FOAF.student))
        self.theGraph.add((URIRef(self.focu.enrolledIn), RDFS.range, BNode()))

    def createTakesCourseProperty(self):
        self.theGraph.add((URIRef(self.focu.takesCourse), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.takesCourse), RDFS.label, Literal("TakesCourse")))
        self.theGraph.add((URIRef(self.focu.takesCourse), RDFS.comment, Literal("Describes the courses that a student takes")))
        self.theGraph.add((URIRef(self.focu.takesCourse), RDFS.domain, BNode()))
        self.theGraph.add((URIRef(self.focu.takesCourse), RDFS.range, self.schema.Course))

    def createGradeAProperty(self):
        self.theGraph.add((URIRef(self.focu.gotA), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.gotA), RDFS.label, Literal("GotAIn")))
        self.theGraph.add((URIRef(self.focu.gotA), RDFS.comment, Literal("Property corresponding to when a student receives a grade A")))
        self.theGraph.add((URIRef(self.focu.gotA), RDFS.domain, BNode()))
        self.theGraph.add((URIRef(self.focu.gotA), RDFS.range, self.schema.Course))

    def createGradeBProperty(self):
        self.theGraph.add((URIRef(self.focu.gotB), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.gotB), RDFS.label, Literal("GotBIn")))
        self.theGraph.add((URIRef(self.focu.gotB), RDFS.comment, Literal("Property corresponding to when a student receives a grade B")))
        self.theGraph.add((URIRef(self.focu.gotB), RDFS.domain, BNode()))
        self.theGraph.add((URIRef(self.focu.gotB), RDFS.range, self.schema.Course))

    def createGradeCProperty(self):
        self.theGraph.add((URIRef(self.focu.gotC), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.gotC), RDFS.label, Literal("GotCIn")))
        self.theGraph.add((URIRef(self.focu.gotC), RDFS.comment, Literal("Property corresponding to when a student receives a grade C")))
        self.theGraph.add((URIRef(self.focu.gotC), RDFS.domain, BNode()))
        self.theGraph.add((URIRef(self.focu.gotC), RDFS.range, self.schema.Course))

    def createGradeDProperty(self):
        self.theGraph.add((URIRef(self.focu.gotD), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.gotD), RDFS.label, Literal("GotDIn")))
        self.theGraph.add((URIRef(self.focu.gotD), RDFS.comment, Literal("Property corresponding to when a student receives a grade D")))
        self.theGraph.add((URIRef(self.focu.gotD), RDFS.domain, BNode()))
        self.theGraph.add((URIRef(self.focu.gotD), RDFS.range, self.schema.Course))

    def createGradeFProperty(self):
        self.theGraph.add((URIRef(self.focu.gotF), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.gotF), RDFS.label, Literal("GotFIn")))
        self.theGraph.add((URIRef(self.focu.gotF), RDFS.comment, Literal("Property corresponding to when a student receives a grade F")))
        self.theGraph.add((URIRef(self.focu.gotF), RDFS.domain, BNode()))
        self.theGraph.add((URIRef(self.focu.gotF), RDFS.range, self.schema.Course))

    def createFall2019Property(self):
        self.theGraph.add((URIRef(self.focu.Semester_Fall_2019), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.Semester_Fall_2019), RDFS.label, Literal("Semester_Fall_2019")))
        self.theGraph.add((URIRef(self.focu.Semester_Fall_2019), RDFS.comment, Literal("Property corresponding to the semester of fall 2019")))
        self.theGraph.add((URIRef(self.focu.Semester_Fall_2019), RDFS.domain, BNode()))
        self.theGraph.add((URIRef(self.focu.Semester_Fall_2019), RDFS.range, self.schema.Course))

    def createWinter2019Property(self):
        self.theGraph.add((URIRef(self.focu.Semester_Winter_2020), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.Semester_Winter_2020), RDFS.label, Literal("Semester_Winter_2019")))
        self.theGraph.add((URIRef(self.focu.Semester_Winter_2020), RDFS.comment, Literal("Property corresponding to winter 2019")))
        self.theGraph.add((URIRef(self.focu.Semester_Winter_2020), RDFS.domain, BNode()))
        self.theGraph.add((URIRef(self.focu.Semester_Winter_2020), RDFS.range, self.schema.Course))

    def addTriplesForSemester(self, string, id, courseID, anode):
        if string == "Fall 2019":
            self.theGraph.add((anode, self.focu.Semester_Fall_2019, URIRef(courseID)))
        if string == "Winter 2019":
            self.theGraph.add((anode, self.focu.Semester_Winter_2019, URIRef(courseID)))

    def addTripleForGrade(self, string, id, courseID, anode):
        if string == "A":
            self.theGraph.add((anode, self.focu.gotA, URIRef(courseID)))
        if string == "B":
            self.theGraph.add((anode, self.focu.gotB, URIRef(courseID)))
        if string == "C":
            self.theGraph.add((anode, self.focu.gotC, URIRef(courseID)))
        if string == "D":
            self.theGraph.add((anode, self.focu.gotD, URIRef(courseID)))
        if string == "F":
            self.theGraph.add((anode, self.focu.gotF, URIRef(courseID)))

    def addToDictionary(self, line):
        id, values = line.strip().split(',', 1)
        self.studentInfo[id] = tuple(values.split(','))
        return self.studentInfo;

    # To associated students with being a person
    def associateStudentsWithPerson(self):
        self.theGraph.add((FOAF.student, RDF.type, FOAF.person))








