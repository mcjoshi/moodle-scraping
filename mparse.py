# run it as python3 mparse.py <LDAPID> <password> <pattern_to_be_searched_in_quotes>

from bs4 import BeautifulSoup
import requests
import sys, re

HomePageUrl = 'http://moodle.iitb.ac.in/login/index.php'

#**************** Check for command line arguments ***********

# storing input arguments into variable for future use
if len(sys.argv) > 3: # len = filename + input arguments = 1 + 3 = 4 , so minimum len = 4
	Username , Password = sys.argv[1], sys.argv[2]
	pattern = ' '.join(sys.argv[3:]) #pattern to be searched 
else :
	print("\nProvide Username, password and pattern to be searched as command line arguments\n")
	exit()

newPattern = '^' + pattern + '$' # new pattern by appending ^ and $ to end
session = requests.session() # make a session

#**************************************************************************************************************

def login() : #username and passwords are given as command line arguments
	s = session.post(HomePageUrl, data = {'username' :  Username, 'password' : Password})

#**************************************************************************************************************

def BSobject(url) :
	webSession = session.get(url)
	return BeautifulSoup(webSession.text, 'html.parser')
	
#**************************************************************************************************************

def findcourses() : # it return all courses a person has registered for 
	courses = [] 
	coursename = []
	CoursePageUrl = 'http://moodle\.iitb\.ac\.in\/course\/view\.php' # Hardcoded coursePageUrl
	for link in bsobject.find_all("a", href=re.compile(CoursePageUrl)):
    		courses.append(link['href'])
    		coursename.append(link.get('title'))
	cours = {}
	for i in range(0,len(coursename)):
		if not (coursename[i] in cours.keys()) and coursename[i]:
			cours[coursename[i]] = courses[i]
	return cours

#**************************************************************************************************************

# now we need to access forum page 
def AccessForum():
	finalMessage = []
	ForumWithinCourse = 'http://moodle\.iitb\.ac\.in\/mod\/forum\/view\.php'
	for course in course_object.find_all("a", href = re.compile(ForumWithinCourse)):
		finalMessage.append(course['href'])

	forumlink = str(finalMessage[0]) # forum link 
	return BSobject(forumlink) # get forum object

#****************************************************************************************************************

def getDiscussLinks(forumObject):
	discuss_links =[]
	RegExp_for_forum = 'http://moodle\.iitb\.ac\.in\/mod\/forum\/discuss\.php\?d\=\d{1,5}$'
	for forum in forumObject.find_all("a", href = re.compile(RegExp_for_forum)) :
		discuss_links.append(forum['href'])

	discuss_links = list(set(discuss_links))
	return discuss_links

#***************************************************************************************************************
def split_on_div(posts):
	finalMessage = []
	tempMessage = []
	for text in posts:
		splitted_text  = re.sub('<div .*?>','',str(text)) # remove all div tags  [? makes sure that its not greedy search]
		splitted_text = re.sub('</div>','',splitted_text) # all closing div tags are removes 
		finalMessage.append(splitted_text)

	return finalMessage

def split_on_pTag(finalMessage):
	#Below loop breaks list elements contained in div elements based on <p> tag. means it will help us when there are multilpe lines 
	#within a same post , we classify multiple lines on the basis of <p> tag
	tempMessage = []
	for text in finalMessage :
		splitted_text = text.split('<p>') # split the list element when you see <p> tag
		for line in splitted_text: # and then for each splitted part append it in another list
			if line != '': # make sure you check it is not empty
				tempMessage.append(line.strip()) # we need to strip as +1 may contain spaces within <p> tag
	return tempMessage

def split_on_brTag(tempMessage):
	finalMessage  = [] # split on <br> tag now
	for text in tempMessage:
		splitted_text = text.split('<br/>')
		for line in splitted_text:
			if line != '':
				line = re.sub('<.*?>','',line)  # remove all tags remaining now like <b> or anything else
				finalMessage.append(line.strip())
	return finalMessage
#*************************************************************************************************************

def countPattern(url) : # counts pattern of a single discussion thread
	soup = BSobject(url)
	posts = soup.find_all(class_ = 'posting fullpost') # All post are captured by using class
	
	Message_splitted_on_div = split_on_div(posts) # Split Posts on div tag
	tempMessage = split_on_pTag(Message_splitted_on_div)
	finalMessage = split_on_brTag(tempMessage)
	
	count = 0
	for eachmsg in finalMessage:
		if re.match(newPattern,eachmsg): # if pattern matches increment count
			count+=1
	return count

#***********************************************************************************************************************

login() # login to moodle 

myPage = 'http://moodle.iitb.ac.in/my'
bsobject = BSobject(myPage)
courses = findcourses()

print('\nHi, Courses to which you have access in moodle are >> \n')

CourseNo = 1 # Course no. to be printed is started from 1 
for courseName in courses : 
	print(str(CourseNo) +'.' + courseName)
	CourseNo+=1

SelectedCourse = int(input('\nEnter the course no. [1-' +str(CourseNo-1)+ '] where you want to search pattern : '))
del CourseNo, myPage,HomePageUrl,Username,Password # No longer needed
key = str(list(courses.keys())[SelectedCourse-1]) #makes a list of keys and then returns the [no-1]th element because list index starts from 0
# whereas i have named courses to start from 1.

courseUrl = courses[key] # it contains url of course selected in above step
course_object = BSobject(courseUrl) # get course page as  object 

#******************* Access Course Forum *************
forumObject = AccessForum()

# Find all threads now and store them
discuss_links = getDiscussLinks(forumObject) # list containig the url of all the threads of a course forum             

print('\nHey, As of now there are ' + str(len(discuss_links)) + ' threads in this course forum\n')

count_of_pattern_in_course_forum = 0

for link in discuss_links:
	link_count = countPattern(link)
	count_of_pattern_in_course_forum += link_count
	
print("Count of " + pattern + ' = ' + str(count_of_pattern_in_course_forum))

