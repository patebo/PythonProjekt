
## TASK 1 ##
## Design a Python program that takes the name of a file which contains text and
## prints out an index of that file. Each line of the index should show a word of
## the text followed by the numbers of each line upon which the word appears. The
## words should be in alphabetical order.
# coding: utf-8

# In[1]:


from collections import defaultdict
get_ipython().system(' pip install --user nltk')
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')


# In[2]:


def tokenization(text): #split text into separate words
    return word_tokenize(text)
def preprocess(tokens): #convert all words to lowercase
    result = []
    for token in tokens:
        result.append(token.lower())
    return result


# In[11]:


def index_by_line(filename): #main function
    index = defaultdict(list)
    with open(filename) as file:
        data_lines = file.readlines()
    i = 1
    for line in data_lines:
        line_tokens = preprocess(tokenization(line))
        for item in line_tokens:
            if item.isalpha()==1:
                 index[item].append(i)
        i = i+1
    sorted_index = sorted(index.items(), key=lambda i:i[0])
    for k,v in sorted_index:
        print(k,": ",v)


# In[13]:


import unittest


# In[14]:


class TestIndex(unittest.TestCase):
    def setUp(self):
        pass
    def test_1(self):
        self.assertEqual(index_by_line("sample.txt"),print("a :  [1, 1, 2] \nalphabetical :  [3] \nan :  [1] \nand :  [1] \nappears :  [2]\nbe :  [3]\nby :  [2]\ncontains :  [1]\ndesign :  [1]\neach :  [1, 2]\nfile :  [1, 1]\nfollowed :  [2]\nin :  [3]\nindex :  [1, 2]\nline :  [1, 2]\nname :  [1]\nnumbers :  [2]\nof :  [1, 1, 2, 2, 2]\norder. :  [3]\nout :  [1]\nprints :  [1]\nprogram :  [1]\npython :  [1]\nshould :  [2, 3]\nshow :  [2]\ntakes :  [1]\ntext :  [1, 2]\nthat :  [1, 1]\nthe :  [1, 2, 2, 2, 2, 2]\nupon :  [2]\nwhich :  [1, 2]\nword :  [2, 2]\nwords :  [2]"))
unittest.main(argv=['first-arg-is-ignored'], exit=False)

## TASK 2 ##
## Design a Python program to help a teacher randomly divide a class into teams for a number of assignments.

## The teacher has information about all of the students in the class in students.csv, which is a file in csv format and would like the output to be also written to a csv file, something like assignment-teams.csv.

## The teacher would also like, in so far as is possible,

## for each student to be in a team with different students for each assignment;
##that the teams are all of the same size (plus or minus one);
##The Python program should take four arguments

## the number of assignments
## the number of students per team
## the name of the input csv file
## the name of the output csv file
## Design unit tests for the internal functions of your program.

# coding: utf-8

# In[3]:


import csv
import random
from collections import defaultdict


# In[4]:


def func(students,stu_per_group): #divide students into groups for an assignment
    nr_groups = len(students)//stu_per_group
    remain = len(students)%stu_per_group
    diff = stu_per_group - remain
    buffer = []
    wtv = [''] # for formatting purpose - we will start writing data from column 2 of csv file
    if diff == 0:
            for j in range(0,nr_groups):
                pop = set(students) - set(buffer)
                temp = random.sample(list(pop), k=stu_per_group)
                wtv.append(temp)
                for stu in temp:
                    buffer.append(stu)
    else:
            for i in range(0,remain):
                pop = set(students) - set(buffer)
                temp = random.sample(list(pop), k=stu_per_group+1)
                wtv.append(temp)
                for stu in temp :
                    buffer.append(stu)
            for k in range(remain,nr_groups):
                pop = set(students) - set(buffer)
                temp = random.sample(list(pop), k=stu_per_group)
                wtv.append(temp)
                for stu in temp:
                    buffer.append(stu)
    return wtv


# In[5]:


def name_extract(input_file): #extract names from a given input file
    columns = defaultdict(list)
    with open(input_file,'r') as students_file:
        reader = csv.DictReader(students_file) #read rows into a dictionary format
        for row in reader:
            for (k,v) in row.items():
                columns[k].append(v)
    return columns["name"]


# In[6]:


def student_teams(nr_assig, stu_per_group, input_file, output_file): #main function
    students = name_extract(input_file)
    
    if len(students) < stu_per_group:
        print("Error: The number of students per team is larger than the total number of students")
        return
    nr_groups = len(students)//stu_per_group
    with open(output_file,"w") as ass_teams:
        writer = csv.writer(ass_teams, delimiter=',')
        lst_of_groups = ['']
        for i in range(1,nr_groups+1):
            lst_of_groups.append('group '+str(i))
        writer.writerow(lst_of_groups)
        for i in range(1,nr_assig+1):
            writer.writerow(['Assignment '+str(i)])
            writer.writerow(func(students, stu_per_group))


# In[7]:


import unittest


# In[8]:


def someone_has_group(stu, lst_gro): #this function is designed for testing purpose
    for gro in lst_gro:
        if stu in gro:
            return True 
    return False
def everyone_has_group(lst_stu, lst_gro):#this function is designed for testing purpose
    for stu in lst_stu:
        if someone_has_group(stu,lst_gro) == 0:
            return False
    return True


# In[10]:


class TestTeamDiv(unittest.TestCase):
    def setUp(self):
        pass
    def test_name_extract(self): #check if all the names in the input list are extracted to the program
        self.assertEqual(name_extract("students.csv"),['Adriana','Alexandre','Andrew','Anh','Baran','Barbara','Ben','Eva','FerrÃ¡n','Fionn','InÃ©s','Jan','Jasmijn','Jasper','Javier','Jonas','Joyce','Justus','Koko','Lela','Lily','Ludovica','Lukas','Mai','Miriam','Noortje','Philip','Robert','Sandy','Semi','Sophia','Terts','Tjalie','Tomas','Vera'])
    def test_func_1(self): #check if everyone has a group
        students = ['Baran','Barbara','Ben','Eva','FerrÃ¡n','Fionn','InÃ©s','Jan','Jasmijn','Jasper']
        teams = func(students,4)
        self.assertEqual(everyone_has_group(students,teams),True)
    def test_func_2(self): #check if the total number of students after division is equal to that before division
        students = ['Adriana','Alexandre','Andrew','Anh','Baran','Barbara','Ben','Eva','FerrÃ¡n','Fionn','InÃ©s','Jan','Jasmijn']
        teams = func(students,3)
        total = 0
        for team in teams:
            total += len(team)
        self.assertEqual(len(students),total)
    def test_func_3(self): #check if all teams are of the same size (plus or minus one)
        students = ['Adriana','Alexandre','Andrew','Anh','Baran','Barbara','Ben','Eva','FerrÃ¡n','Fionn','InÃ©s','Jan','Jasmijn']
        teams = func(students,3)
        nr_st_team = set(len(team) for team in teams[1:])  
        self.assertEqual(nr_st_team,{3,4} or {3})
               
unittest.main(argv=['first-arg-is-ignored'], exit=False)

