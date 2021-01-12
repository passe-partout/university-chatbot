from Student import Student
from rdflib import Namespace, URIRef, Graph
from rdflib.namespace import RDF, FOAF, RDFS, XSD
from rdflib.term import Literal

class Course:
    def __init__(self):
        self.theGraph = Graph()
        self.studentInfo = {}
        self.data = Namespace("http://www.example.org#")
        self.schema = Namespace('https://schema.org/')
        self.focu = Namespace('http://focu.io/schema#')
        self.courseInfo = {}

    def __init__(self, dataNameSpace, schemaNameSpace, focuNameSpace, dbpediaNameSpace, otologyNameSpace):
        self.theGraph = Graph()
        self.data = dataNameSpace
        self.schema = schemaNameSpace
        self.focu = focuNameSpace
        self.dbpedia = dbpediaNameSpace
        self.otology = otologyNameSpace
        self.courseInfo = {}

    def readFile(self):
        file = open("output/course_info.csv", encoding = "utf-8")
        #Removes the first line of the file
        file.readline()
        for line in file:
            self.courseInfo = self.addToDictionary(line)


    #Used for testing with a smaller file
    def readTestFile(self):
        file = open("input/SmallerTestData/course_info_smaller.csv")
        line = file.readline()
        while line:
            self.courseInfo = self.addToDictionary(line)

    def linkCourseWithInfo(self):
        self.addProperties()

        #This is the lien that will be used to read all of the data
        self.readFile()

        #The line below is used to test a smaller file
        #self.readTestFile()

        for key in self.courseInfo:
            id = self.data + str(key)
            self.theGraph.add((URIRef(id), RDF.type, URIRef(self.schema.course)))

            self.theGraph.add((URIRef(self.dbpedia.Concordia_University), self.focu.hasCourse, URIRef(id)))

            for x in range(4):
                if x == 0:
                    self.theGraph.add((URIRef(id), self.focu.courseSubject, Literal(self.courseInfo[key][x])))
                if x == 1:
                    self.theGraph.add((URIRef(id), self.schema.courseCode, Literal(self.courseInfo[key][x])))
                if x == 2:
                    self.theGraph.add((URIRef(id), FOAF.name, Literal(self.courseInfo[key][x])))
                if x == 3:
                    self.theGraph.add((URIRef(id), self.schema.about, Literal(self.courseInfo[key][x])))
        return self.theGraph

    #This function is used to add all the properties to the graph
    def addProperties(self):
        self.createCourseProperty()
        self.createCourseSubject()


    def createCourseProperty(self):
        self.theGraph.add((URIRef(self.focu.hasCourse), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.hasCourse), RDFS.label, Literal("hasCourse")))
        self.theGraph.add((URIRef(self.focu.hasCourse), RDFS.comment, Literal("Corresponds to the courses offered at a university")))
        self.theGraph.add((URIRef(self.focu.hasCourse), RDFS.domain, URIRef(self.otology.University)))

    def createCourseSubject(self):
        self.theGraph.add((URIRef(self.focu.courseSubject), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.hasCourse), RDFS.label, Literal("CourseSubject")))
        self.theGraph.add((URIRef(self.focu.hasCourse), RDFS.comment, Literal("Corresponds to the subject associated with a course")))

    def addToDictionary(self, line):
        id, values = line.strip().split(',', 1)
        description = values.split("\"")
        tempSplit = tuple(values.split(','))
        self.courseInfo[id] = (tempSplit[0],tempSplit[1], tempSplit[2], description)
        return self.courseInfo
