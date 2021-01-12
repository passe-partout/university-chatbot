# from Student import Student
# from Course import Course
# from Topics import Topics
# from University import University
# from Query import Query
# from rdflib import Namespace, Graph
#
# theGraph = Graph()
# data = Namespace("http://www.example.org#")
# schema = Namespace('https://schema.org/')
# focu = Namespace('http://focu.io/schema#')
# dbpedia = Namespace('http://dbpedia.org/resource/')
# otology = Namespace('http://dbpedia.org/ontology/')
#
# #Creating the univeristy triples
# print("Creating the triples for Concordia University...")
# universityFile = University(data, schema, focu, dbpedia, otology)
# theGraph = theGraph + universityFile.createUniversityInfo()
#
#
# #To obtain the student information
# print("Creating the triples for students...")
# studentFile = Student(data, schema, focu, dbpedia, otology)
# theGraph = theGraph + studentFile.createFile()
#
# #To obtain the course information
# print("Creating the triples for courses...")
# courseFile = Course(data, schema, focu,dbpedia, otology)
# theGraph = theGraph + courseFile.linkCourseWithInfo()
#
# #To create the topic information
# print("Creating the triples for topics...")
# topicFile = Topics(data, schema, focu,dbpedia, otology)
# theGraph = theGraph + topicFile.linkNameWithURL()
#
# #Creates the triples and puts them in the file "TheTriples.txt"
# theGraph.serialize(destination='output/TheTriples.txt', format='turtle')
#
# print("The knowledge graph has been created and also saved in output/TheTriples.txt. Now we can query on it")
# theQueries = Query(theGraph)
# toContinue = True
# anotherQuestion = True
#
# while True:
#     while (toContinue):
#         value = input("Select "
#                       "\n 1 - To get the total number of triples"
#                       "\n 2 - To get the total number of students, courses, and topics"
#                       "\n 3 - To get the topics associated with a course "
#                       "\n 4 - To get courses associated with a student"
#                       "\n 5 - For students familiar with a topic"
#                       "\n 6 - All topics that a particular student is familiar with"
#                       "\n 7 - Other \n"
#                       )
#         if (not (value.isdigit())):
#             print("Invalid request. Please try again.")
#         if (value.isdigit()):
#             toContinue = False
#     if (int(value) == 1):
#         theQueries.queryOne()
#     if (int(value) == 2):
#         theQueries.queryTwo()
#     if (int(value) == 3):
#         courseInfo = input("Enter the course subject and code with a space in between: ")
#         courseInformation = courseInfo.split(" ")
#         theQueries.queryThree(courseInformation[0].upper().strip(), courseInformation[1].strip())
#     if (int(value) == 4):
#         firstLastName = input("Enter the student's first and last name: ")
#         studentInfo = firstLastName.split(" ")
#         theQueries.queryFour(studentInfo[0].capitalize().strip(), studentInfo[1].capitalize().strip())
#     if (int(value) == 5):
#         topic = input("Enter a topic ")
#         theQueries.queryFive(topic)
#     if (int(value) == 6):
#         firstLastName = input("Enter the student's first and last name: ")
#         studentInfo = firstLastName.split(" ")
#         theQueries.querySix(studentInfo[0].capitalize().strip(), studentInfo[1].capitalize().strip())
#     if (int(value) == 7):
#         theQuery = input("Enter the query: ")
#         theQueries.querySeven(theQuery)
#     doesUserContinue = input("Do you want to continue? (Y/N)")
#     if (doesUserContinue == "Yes" or doesUserContinue == "Y" or doesUserContinue == "yes" or doesUserContinue == "y"):
#         toContinue = True
#         continue
#     if (doesUserContinue == "No" or doesUserContinue == "N" or doesUserContinue == "n" or doesUserContinue == "no"):
#         break