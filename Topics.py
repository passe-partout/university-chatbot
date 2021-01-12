from rdflib import Namespace, URIRef, Graph
from rdflib.namespace import RDF, FOAF, RDFS, XSD
from rdflib.term import Literal, BNode

class Topics:
    # Default constructor
    def __init__(self):
        self.theGraph = Graph()
        self.studentInfo = {}
        self.data = Namespace("http://www.example.org#")
        self.schema = Namespace('https://schema.org/')
        self.focu = Namespace('http://focu.io/schema#')

    # Constructor
    def __init__(self, dataNameSpace, schemaNameSpace, focuNameSpace, dbpediaNameSpace, otology):
        self.theGraph = Graph()
        self.data = dataNameSpace
        self.schema = schemaNameSpace
        self.focu = focuNameSpace
        self.dbpedia = dbpediaNameSpace
        self.otology = otology
        self.studentInfo = {}

    def linkNameWithURL(self):
        file = open("id_keywords_uri.txt", encoding = "utf-8")

        #To test on a smaller subset
        #file = open("input/SmallerTestData/id_keywords_uri_smaller.txt")
        line = file.readline()
        while line:
            theLine = str(line)
            topicID = theLine[:6].strip()
            httpIndex = theLine.index("http")
            theName = theLine[6:httpIndex].strip().replace(" ", "_")
            theURL = theLine[httpIndex:].strip()
            URLforName = self.data + str(theName)
            self.theGraph.add((URIRef(self.data + str(topicID)), FOAF.topic, URIRef(URLforName)))
            self.theGraph.add((URIRef(URLforName), self.focu.topicLink, URIRef(str(theURL))))
            line = file.readline()
        return self.theGraph

    def createTopicURL(self):
        self.theGraph.add((URIRef(self.focu.topicLink), FOAF.a, FOAF.property))
        self.theGraph.add((URIRef(self.focu.hasCourse), RDFS.label, Literal("Topic Link")))

