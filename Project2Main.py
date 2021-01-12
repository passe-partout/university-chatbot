#This is the main class for Project 2. This uses the previously created RDF file that was created from Assignment 1.
#However, if you wish to rerun the triples, it can be done from Project1Main.py
from rdflib import Namespace, Graph
from Queryp2 import Queryp2
import aiml_bot

g = Graph()
g.load("output/TheTriples.txt", format="n3")
theQueries = Queryp2(g)
bot = aiml_bot.Bot(learn="mybot.aiml")
shouldContinue = True
print("\nWelcome to the university chatbot!")
print("======================================\n")

while shouldContinue:
    test = bot.respond(input("What can I help you with? "))
    text = test.split(' ')
    if text[0] == "question1":
        #Error handling
        if len(text) != 3:
            print("Invalid information entered. Try again.")
        else:
            theQueries.queryOne(text[1].upper(), text[2])
    elif text[0] == "question2":
        index = test.find(' ')
        givenString = test[(index + 1):]
        if (givenString.isdigit()):
            theQueries.queryTwoWithID(givenString)
        else:
            splitName = test.split(' ')
            theQueries.queryTwoWithName(splitName[1], splitName[2])
    elif text[0] == "question3":
        if len(text) == 2:
            theQueries.queryThree(text[1])
        else:
            index = test.find(' ')
            givenString = test[(index + 1):]
            theQueries.queryThree(givenString)
    elif text[0] == "question4":
        index = test.find(' ')
        givenString = test[(index + 1):]
        theNewString = givenString.replace(" ", "_")
        theQueries.queryFour(givenString)
    programContinue = input("Do you want to continue? Y/N ").lower()
    if programContinue == 'y' or programContinue == "yes":
        shouldContinue = True
    else:
        shouldContinue = False
        print("Goodbye. See you next time!")
