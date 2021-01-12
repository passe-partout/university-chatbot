from rdflib import Namespace, URIRef, Graph
from rdflib.namespace import RDF, FOAF, RDFS, XSD
from rdflib.term import Literal, BNode

class University:
    #Default constructor
    def __init__(self):
        self.theGraph = Graph()
        self.studentInfo = {}
        self.data = Namespace("http://www.example.org#")
        self.schema = Namespace('https://schema.org/')
        self.focu = Namespace('http://focu.io/schema#')

    #Parametrized constructor
    def __init__(self, dataNameSpace, schemaNameSpace, focuNameSpace, dbpediaNameSpace, otology):
        self.theGraph = Graph()
        self.data = dataNameSpace
        self.schema = schemaNameSpace
        self.focu = focuNameSpace
        self.dbpedia = dbpediaNameSpace
        self.otology = otology
        self.studentInfo = {}

    def createUniversityInfo(self):
        self.addToGraph()
        return self.theGraph

    def addToGraph(self):
        self.theGraph.add((URIRef(self.dbpedia.Concordia_University), RDF.type, URIRef(self.otology.University)))
        self.theGraph.add((URIRef(self.dbpedia.Concordia_University), self.otology.city, URIRef(self.dbpedia.Montreal)))
        self.theGraph.add((URIRef(self.dbpedia.Concordia_University), FOAF.homepage, URIRef("https://www.concordia.ca")))
        self.theGraph.add((URIRef(self.otology.University), FOAF.a, FOAF.Class))
        self.theGraph.add((URIRef(self.otology.University), RDFS.subClassOf, FOAF.organization))

    def returnGraph(self):
        return self.theGraph