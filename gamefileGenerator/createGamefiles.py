import random
import copy
from csv import reader
import sys
import xlsxwriter

# One school subject contains name and a list of questions with answers (pair)
class Subject:
    def __init__(self, name):
        self.name = name
        self.questions = []
        self.nr_available_questions = 0

    def print(self):
        #print(self.questions)
        print(self.nr_available_questions)
        print(self.name)
        print("-----")

    # Method add a new question with answer (as a pair)
    def add_question(self, question, answer):
        self.questions.append((question, answer))
        self.nr_available_questions += 1

    # Method to pop random question out of the subject
    def pop(self):
        randomly_picked_question_index = random.randint(0, len(self.questions)-1)
        randomly_picked_question = self.questions.pop(randomly_picked_question_index)
        self.nr_available_questions -= 1
        return randomly_picked_question[0], randomly_picked_question[1]


class Gamefile:
    def __init__(self, name):
        self.name = name
        self.name_questions_answers = []


class Databank:
    def __init__(self):
        self.subjects = []
        self.retired_subjects = []
        self.lottery_list = [] # For every question in every subject this lottery list has a ticket with subject name.
        self.gamefile_list = [] # List of generated gamefiles
        self.OUTPUT_NAME = "output.xlsx"

    # Check if subject name is present in databank
    # Method returns Bool value and a index of item in list. (-1 if not found)
    # This is a slow and hacky bodge, who cares for 1k items...
    def find_subject(self, subject_name):
        subject_already_present = False
        subject_index = 0
        for subject in self.subjects:
            if subject.name == subject_name:
                subject_already_present = True
                break
            subject_index += 1

        if subject_already_present == False:
            subject_index = -1

        return subject_already_present, subject_index

    # Insert question into databank. If Subject does not exist yet, it creates a new one.
    def insert_question(self, subject_name, question, answer):
        # Check if subject name is present in databank
        subject_found, subject_index = self.find_subject(subject_name)
        # If not found, create it.
        if subject_found == False:
            # Create new subject
            new_subject = Subject(subject_name)
            self.subjects.append(new_subject)
            # Recalculate index
            subject_found, subject_index = self.find_subject(subject_name)

        # Now subject definetely exists (hacky, i know)
        # - Create a corresponding lottery ticket & shuffle lottery
        self.lottery_list.append(subject_name)
        random.shuffle(self.lottery_list)
        # - Insert new question into the correct subject in this databank
        self.subjects[subject_index].add_question(question, answer)

    # Load subjects into databank from CSV file (subject name, question, answer)
    def load_from_csv(self, csv_filename):
        # For each line
        # It is very unsafe to have the name of the file as a variable. Kokes is sad.
        # open file in read mode
        # https://thispointer.com/python-read-a-csv-file-line-by-line-with-or-without-header/
        with open(csv_filename, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                # Read the first three columns
                self.insert_question(row[0], row[1], row[2])
 
    # Pop N elements from subject with specified index
    # Returns a list of tuples (name, question, answer) for the new gamefile
    def pop_from_subject(self, how_many_to_pop, subject_index):
        new_name_questions_answers = []
        # Pick N questions from defined subject
        for i in range(0, how_many_to_pop):
            # Pop a question and print it
            popped_name = self.subjects[subject_index].name
            popped_question, popped_answer = self.subjects[subject_index].pop()
            new_name_questions_answers.append((popped_name, popped_question, popped_answer))
            # print(popped_name, popped_question, popped_answer) # Too much printing causes I/O error on pythonanywhere
            # For this subject, remove "one ticket" from lottery list. (To keep the lottery fair)
            ticket_index = self.lottery_list.index(popped_name)
            self.lottery_list.pop(ticket_index)
        return new_name_questions_answers

    # Pick a random subject from subject array
    def pick_random_subject(self):
        #picked_random_subject = random.randint(0, len(self.subjects)-1)
        #return picked_random_subject
        # Pick random subject from lottery list
        picked_random_subject = random.choice(self.lottery_list)
        return self.find_subject(picked_random_subject)[1]

    # Check if subject has enough questions left. If not, retire it.
    # True if subject retired, False if subject healthy
    def try_to_retire_subject(self, subject_index, questions_per_subject):
        if self.subjects[subject_index].nr_available_questions < questions_per_subject:
            # Retire, not enough questions
            # print(">>> Retiring", self.subjects[subject_index].name)
            copy_of_retiring_subject = copy.deepcopy(self.subjects[subject_index])
            self.retired_subjects.append(copy_of_retiring_subject)
            self.subjects.pop(subject_index)
            # TODO Retiring a subject means modifying the lottery array accordingly
            return True
        # This subject is healthy with enough questions
        return False

    # Retire all subject left in this subjects array
    def retire_all(self):
        # Until the subject list is empty
        while len(self.subjects) != 0:
            # Retire a subject
            self.try_to_retire_subject(0, self.subjects[0].nr_available_questions +1 )

    # Dump a gamefile. Must contains N questions. Categories must differ.
    # Create a Gamefile with X distinct subject and N questions per subject
    def create_gamefile(self, name, distinct_subjects, questions_per_subject):
        new_gamefile = Gamefile(name)
        distinct_subject_names = []
        flag = 0 # Count if the loop does not exceed reasonable maximum (100 times number of subjects iterations)
        # Until you have an array with X distinct subjects
        while len(distinct_subject_names) != distinct_subjects:
            # Pick a random subject from subject array
            picked_subject_name = self.subjects[self.pick_random_subject()].name
            # If it was aready picked, return it back and continue
            if picked_subject_name in distinct_subject_names:
                flag += 1
                if flag > (100*len(self.subjects)):
                    raise Exception("Number of iterations exceeded reasonable bumber.")
                continue
            else:
                distinct_subject_names.append(picked_subject_name)
                subject_index = self.find_subject(picked_subject_name)[1]
                # If we found a distinct new subject >> pop questions into new gamefile
                for line in self.pop_from_subject(questions_per_subject, subject_index):
                    new_gamefile.name_questions_answers.append(line)
                # Check if there are questions left in subject, if not retire the subject
                self.try_to_retire_subject(subject_index, questions_per_subject)

        # Add the created gamefile to the gamefile list of the databank
        self.gamefile_list.append(new_gamefile)
        return True

    # Export gamefile_list and retired_subjets to one xlsx for nice editation
    def export_to_xlsx(self):
        workbook   = xlsxwriter.Workbook(str(self.OUTPUT_NAME))

        # For each gamefile in the current list of gamefiles
        for gamefile in self.gamefile_list:
            # Create new worksheet
            current_worksheet = workbook.add_worksheet("Game " + str(gamefile.name))
            current_worksheet.set_column('B:C', 75)  # Column  E   width set to 20.
            # Create header
            current_worksheet.write('A1', "Název")
            current_worksheet.write('B1', str(gamefile.name))
            current_worksheet.write('A2', "Tajenka")
            current_worksheet.write('B2', "???")
            current_worksheet.write('A4', "Kategorie")
            current_worksheet.write('B4', "Otázka")
            current_worksheet.write('C4', "Odpověď")
            current_worksheet.write('A5', "---")
            current_worksheet.write('B5', "---")
            current_worksheet.write('C5', "---")
            # Dump (subject name, question, answer)
            line_number = 5 # staring after the header
            for name_question_answer in gamefile.name_questions_answers:
                current_worksheet.write(line_number,0, name_question_answer[0])
                current_worksheet.write(line_number,1, name_question_answer[1])
                current_worksheet.write(line_number,2, name_question_answer[2])
                line_number += 1

        # Export retired questions to csv
        retired_worksheet =  workbook.add_worksheet("Unused questions")
        retired_worksheet.set_column('B:C', 75)  # Column  E   width set to 20.
        line_number = 0
        # For every retired subject
        for grandpa in self.retired_subjects:
            # Write all questions to next line
            for unused_question in grandpa.questions:
                retired_worksheet.write(line_number,0, grandpa.name)
                retired_worksheet.write(line_number,1, unused_question[0])
                retired_worksheet.write(line_number,2, unused_question[1])
                line_number += 1


        workbook.close()

def generate_gamefiles(FILE_NAME,
                       OUTPUT_NAME,
                       NUMBER_OF_GAMEFILES,
                       NUMBER_OF_SUBJECTS_IN_GAMEFILE,
                       NUMBER_OF_QUESTIONS_PER_SUBJECT):
    banka = Databank()
    banka.OUTPUT_NAME = OUTPUT_NAME
    banka.load_from_csv(FILE_NAME)
    generation_error = False  # Track if there was any error during generation

    # Try to create the gamefiles
    try:
        for i in range(0, NUMBER_OF_GAMEFILES):
            banka.create_gamefile(i,NUMBER_OF_SUBJECTS_IN_GAMEFILE, NUMBER_OF_QUESTIONS_PER_SUBJECT)
            # print("-------------------------------")
            print("> Gamefile", i, "created successfully.")
    except Exception as e:
        print("-----------------------------------------------")
        print("> Crash loop back off!")
        print("-----------------------------------------------")
        print("This run was not able to fulfill all")
        print("requirements with the specified CSV file")
        print("How to fix?")
        print("- Run it again. Maybe it was a close call")
        print("  but the odds were not in your favour.")
        print("- Add more subjects and questions into the CSV.")
        print("- Relax the requirements. Try to require")
        print("  less questions/subjects in each gamefile.")

        # print("--------------------------------")
        # print("Crash loop back off!\n"
        #       "This run was not able to fulfill the requirements with the specified CSV file\n"
        #       "How to fix?\n"
        #       "1) Run it again. Maybe it was a close call but the odds were not in your favour.\n"
        #       "2) Add more subjects and questions into the CSV file.\n"
        #       "3) Relax the requirements. Try to require less questions/subjects in each gamefile.")
        generation_error = True

    # Retire all other unused subjects into unused questions
    try:
        banka.retire_all()
    except:
        print("Error when retiring subjects.")

    # Export to XLSX
    export_error = False
    try:
        banka.export_to_xlsx()
    except:
        print("Error when exporting to xlsx.")
        export_error = True

    # Count how many gamefiles were written
    gamefiles_written = len(banka.gamefile_list)
    print("-----------------------------------------------")
    print("Number of gamefiles written:", gamefiles_written)
    print("-----------------------------------------------")

    print("> Gamefile generation finished.", end='')

    # Consider it a success if any gamefiles were written and export worked
    success = gamefiles_written > 0 and not export_error

    return success, gamefiles_written, generation_error