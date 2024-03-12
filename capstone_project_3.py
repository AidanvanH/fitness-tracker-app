import sqlite3
from sqlite3 import IntegrityError

db = sqlite3.connect('fitness_tracker_app')
cur = db.cursor()

category_lst = []       # List that stores all exercise category names
category_ids = []       # List that stores all exercise category id's
categories_and_exercises_dict = {}  # Stores the categories as keys and the exercises as values
all_exercises_lst = []      # List that stores all exercises across all exercise categories
exercises_in_routine = []  # This holds all the exercise names the user adds to their workout routine
routine_lst = []    # This will hold the exercise routines of a particular exercise category
routine_lst_all = []    # Encapsulates all routines. Will be used later to check if user indeed has routines
workout_routine_names = []      # List that stores workout routine names
workout_descriptions_lst = []   # List that stores the workout descriptions for each exercise from workout routine table

# Initializing classes for various sqlite3 tables
class ExerciseCategory:

    # Creates a table for the user's exercise categories
    def create_table():
        cur.execute('''CREATE TABLE IF NOT EXISTS exercise_category
                    (exercise_category_id INTEGER PRIMARY KEY, exercise_category_name TEXT UNIQUE)''')
        
    # Inserts exercise categories that the user adds 
    def execute(new_data):
        cur.execute('''INSERT INTO exercise_category(exercise_category_name) 
                    VALUES (?)''', (new_data,))
        db.commit()

    # Prints out each exercise category that the user has
    def view_all_categories():
        cur.execute('''SELECT * FROM exercise_category''')
        for row in cur:
            print(row[1])  

    # Appends each exercise category's name to list
    def lst_all_categories():
        cur.execute('''SELECT exercise_category_name FROM exercise_category''')
        for row in cur:
            category_lst.append(row[0])

    # Fetches the exercise category's id and returns it
    def retrieve_category_id(category):
        cur.execute('''SELECT exercise_category_id FROM exercise_category WHERE
                    exercise_category_name=?''', (category,))
        c = cur.fetchone()
        return c[0]

    # Deletes an exercise category of the user's choosing
    def delete(delete_exercise_category):
        cur.execute('''DELETE FROM exercise_category WHERE exercise_category_name = ? ''',
                    (delete_exercise_category,))
        db.commit()

class Exercise:
    
    # Creates a table for the exercise category's respective exercises
    def create_table():
        cur.execute('''CREATE TABLE IF NOT EXISTS exercises
                    (exercise_id INTEGER PRIMARY KEY, exercise_name TEXT UNIQUE, exercise_category_id)''')

    # Inserts the exercise categories into table
    def execute(new_exercise, exercise_cat):
        cur.execute('''INSERT INTO exercises(exercise_name, exercise_category_id) VALUES(?,?)''',
                    (new_exercise, exercise_cat))
        db.commit()

    # Method that creates keys for exercise categories and values for their exercises 
    def populate_dict(exercise_category):
        for i in category_lst:
            cur.execute('''SELECT exercise_category_id FROM exercise_category WHERE
                        exercise_category_name=?''', (i,))
            convert_id = int(''.join(map(str, cur.fetchone()))) # Fetches the category's id
            categories_and_exercises_dict[i] = None     # Initialises dictionary with 'None' values
            cur.execute('''SELECT exercise_name FROM exercises WHERE exercise_category_id=?''', (convert_id,))
            # Fetches the category exercises as values and stores them in the appropriate key
            categories_and_exercises_dict[i] = cur.fetchall()   

    # Method that prints out an exercise category's exercises
    def print_exercise_categories(exercise_category):
        for i in category_lst:
            cur.execute('''SELECT exercise_category_id FROM exercise_category WHERE
                        exercise_category_name=?''', (i,))
            convert_id = int(''.join(map(str, cur.fetchone()))) # Fetches the category's id
            categories_and_exercises_dict[i] = None
            cur.execute('''SELECT exercise_name FROM exercises WHERE exercise_category_id=?''', (convert_id,))
            categories_and_exercises_dict[i] = cur.fetchall()
            # Prints out category's exercises
        for x in categories_and_exercises_dict[exercise_category]:
            print(x[0])

    # Deletes an exercise that the user chooses from exercises table
    def delete(delete_exercise_by_category):
        cur.execute('''DELETE FROM exercises WHERE exercise_name=?''',
                    (delete_exercise_by_category,))
        db.commit()

    # Deletes all exercises from a specified exercise category of the user's choosing
    def delete_all_exercises(category_id):
        cur.execute('''DELETE FROM exercises WHERE exercise_category_id=?''',
                    (category_id,))
        db.commit()

    # Appends all exercises in the exercise table to list
    def all_exercises():
        cur.execute('''SELECT exercise_name FROM exercises''')
        for e in cur:
            all_exercises_lst.append(e)

    # Appends all exercises from a specified exercise category to list
    def all_category_exercises(exercise_cat, lst):
        cur.execute('''SELECT exercise_name FROM exercises
                    WHERE exercise_category_id=?''', (exercise_cat,))
        for e in cur:
            lst.append(e)

class WorkoutRoutine:   

    # Creates a table for the workout routine
    def create_table():     
        cur.execute('''CREATE TABLE IF NOT EXISTS workout_routine
                    (workout_routine_name TEXT, workout_routine_exercise TEXT, 
                    workout_description TEXT, exercise_category_id)''')
        
    # Inserts workout routines into table
    def execute_workout_routine(routine_name, routine_exercises, routine_description, exercise_routine_id):      
        cur.execute('''INSERT INTO workout_routine(workout_routine_name, workout_routine_exercise,
                    workout_description, exercise_category_id) VALUES (?,?,?,?)''', 
                    (routine_name, routine_exercises, routine_description, exercise_routine_id))
        db.commit()

    # Prints out the exercises from a particular workout routine
    def view_workout_routine_exercises(routine_name):
        cur.execute('''SELECT workout_routine_exercise FROM workout_routine WHERE
                    workout_routine_name=?''', (routine_name,))
        for r in cur:
            print(r[0])

    # Prints out the exercises and its descriptions from a particular workout routine
    def view(exercise_name):    
        cur.execute('''SELECT workout_routine_exercise, workout_description FROM workout_routine
                    WHERE workout_routine_name=?''', (exercise_name,))
        for j in cur:
            print(j[0], '-', j[1])
    
    # Appends workout routine names from table into list
    def workout_routine_lst_names(category_id):
        lst = []
        cur.execute('''SELECT workout_routine_name FROM workout_routine
                    WHERE exercise_category_id=?''', (category_id,))
        # Prevents duplicate workout routine names from being appended to list
        for routine_name in cur:
            if not routine_name in lst:
                lst.append(routine_name[0])
        for i in lst:
            if not i in workout_routine_names:
                workout_routine_names.append(i)

    # Appends the exercises from a particular workout routine to list
    def exercises_in_routine(routine):
        cur.execute('''SELECT workout_routine_exercise FROM 
                    workout_routine WHERE workout_routine_name=?''',
                    (routine,))
        for exercise in cur: 
            exercises_in_routine.append(exercise[0])

    # Appends workout routine name from workout routine based on exercise category's id
    def lst_of_routines(exercise_id):
        cur.execute('''SELECT workout_routine_name FROM workout_routine
                    WHERE exercise_category_id=?''', (exercise_id,))
        for r in cur:
            routine_lst.append(r[0])

    # Appends all workout routine names to list
    def all_routines():
        cur.execute('''SELECT * FROM workout_routine''')
        for routine in cur:
            routine_lst_all.append(routine[0])

    # Prints out the workout description of a particular exercise in a workout routine
    def print_exercise_description(routine, exercise):
        cur.execute('''SELECT workout_description FROM workout_routine 
                    WHERE workout_routine_name=? AND workout_routine_exercise=?''', 
                    (routine, exercise))
        for exercise in cur:
            print(exercise[0])
    
    # Appends the exercise descriptions of a particular workout routine to list
    def description_list(routine):
         cur.execute('''SELECT workout_description FROM workout_routine 
                    WHERE workout_routine_name=?''',
                    (routine,))
         for i in cur:
             workout_descriptions_lst.append(i[0].split('\n'))
        
    # Updates exercises workout description of a particular workout routine
    def update_workout_description(new_description, routine, exercise):
        cur.execute('''UPDATE workout_routine SET workout_description=?
                    WHERE workout_routine_name=? AND workout_routine_exercise=?''', 
                    (new_description, routine, exercise))
        db.commit()

    # Deletes workout routine 
    def delete_workout_routine(delete_routine):
        cur.execute('''DELETE FROM workout_routine WHERE workout_routine_name=?''',
                    (delete_routine,))
        db.commit()

    # Deletes exercise from workout routine
    def delete_exercise(exercise):
        cur.execute('''DELETE FROM workout_routine WHERE
                    workout_routine_exercise=?''', (exercise,))
        db.commit()

    # Deletes workout routine
    def delete(d):  
        cur.execute('''DELETE FROM workout_routine WHERE exercise_category_id=?''',
                    (d,))
        db.commit()

    # Deletes an exercise and its description from workout routine table
    def delete_routine_exercise(routine_name, routine_exercise):
        cur.execute('''DELETE FROM workout_routine WHERE workout_routine_name=?
                    AND workout_routine_exercise=?''', (routine_name, routine_exercise))
        db.commit()

class CreateWorkout:      

    # The following method allows users to select their own parameters for the workout routines they make
    def choose_own_param(exercises):      # List of all exercises the user aims to include in workout routine

        str_of_description_info = ''    # String to hold each exercises descriptions
        start = True        
        while start:

            for exercise in exercises:
                advance = True
                while advance:
                    print('''
Enter 1 to add new parameter to your workout for ''' + exercise + '''
Enter 2 to move on once you're done picking
''')
                    select = input('Enter the command you would like to do: ')

                    if select == '1':

                        select_option = True
                        while select_option:
                            print('''
Please select the number that relates to the parameter of your choosing
1 - Sets
2 - Reps
3 - Weight
4 - Total time
5 - Distance
6 - Time structure
7 - Additional info
''')
                            option = input('Enter the command you wish to do: ')

                            if option == '1':

                                add_description = True
                                while add_description:
                                    sets = input(f'Enter the number of sets you would like for {exercise}: ')   # Once this is all sorted, replace 'this exercise' with the name of the exercise
                                    if sets.strip == '':
                                        print('Invalid')
                                    else:
                                        # Adds the description of exercises final set to empty string
                                        final_sets = f'The number of sets for this {exercise} is: {sets}'
                                        str_of_description_info += final_sets + '\n'
                                        add_description = False
                                        select_option = False

                            elif option == '2':

                                add_description = True
                                while add_description:
                                    reps = input(f'Enter the number of reps you would like for {exercise}: ')
                                    if reps.strip() == '':
                                        print('Invalid')
                                    else:
                                        # Adds the description of exercises final reps to empty string
                                        final_reps = f'The number of reps you have for {exercise} is: {reps}'
                                        str_of_description_info += final_reps + '\n'
                                        add_description = False
                                        select_option = False

                            elif option == '3':

                                add_description = True
                                while add_description:
                                    weight = input(f'Enter the amount of weight you would like for {exercise}: ')
                                    if weight.strip() == '':
                                        print('Invalid')
                                    else:
                                        # Adds the description of exercises final weight to empty string
                                        final_weight = f'The amount of weight you\'re using for {exercise} is: {weight}'
                                        str_of_description_info += final_weight + '\n'
                                        add_description = False
                                        select_option = False

                            elif option == '4':

                                add_description = True
                                while add_description:
                                    time = input(f'Enter the amount of time you would like to spend on {exercise}: ')
                                    if time.strip() == '':
                                        print('Invalid')
                                    else:
                                        # Adds the description of exercises final time to empty string
                                        final_time = f'The total time you are spending on {exercise} is: {time}'
                                        str_of_description_info += final_time + '\n'
                                        add_description = False
                                        select_option = False

                            elif option == '5':

                                add_description = True
                                while add_description:
                                    distance = input(f'Enter the distance you wish to cover for {exercise}: ')
                                    if distance.strip() == '':
                                        print('Invalid')
                                    else:
                                        # Adds the description of exercises final distance to empty string
                                        final_distance = f'The total distance you are covering for {exercise} is: {distance}'
                                        str_of_description_info += final_distance + '\n'
                                        add_description = False
                                        select_option = False

                            elif option == '6':

                                add_description = True
                                while add_description:
                                    time_structure = input(f'Enter the time structure you would like to use for {exercise}: ')
                                    if time_structure.strip() == '':
                                        print('Invalid')
                                    else:
                                        # Adds the description of exercises time structure to empty string
                                        final_time_structure = f'The time structure that you are using for {exercise} is: {time_structure}'
                                        str_of_description_info += final_time_structure + '\n'
                                        add_description = False
                                        select_option = False

                            elif option == '7':

                                add_description = True
                                while add_description:
                                    additional_info = input(f'Enter any additional information you would like to add for {exercise}: ')
                                    if additional_info.strip() == '':
                                        print('Invalid')
                                    else:
                                        # Adds the additional information for the exercise to empty string
                                        final_info = f'Additional information that was added is: {additional_info}'
                                        str_of_description_info += final_info + '\n'
                                        add_description = False
                                        select_option = False
                            else:
                                print('Invalid')
                
                    elif select == '2':
                        WorkoutRoutine.execute_workout_routine(routine_name, exercise, str_of_description_info, category_id)  
                        exercises.remove(exercise)  # Removes the current exercise from for loop and moves on
                        str_of_description_info = ''    # Emptying the string for next exercise
                        if exercises == []:     # Exits loop if there are no more exercises in for loop
                            advance = False
                            start = False
                        elif exercises != []:
                            advance = False     # Repeats process if there are more exercises in for loop
                    else:
                        print('Invalid')

class FitnessGoal:  

    # Creates a table for the fitness goal
    def create_table():
        cur.execute('''CREATE TABLE IF NOT EXISTS fitness_goal
                    (fitness_goal_id INTEGER PRIMARY KEY, fitness_goal_input TEXT UNIQUE,
                    fitness_goal_achieve_date TEXT, fitness_goal_progress TEXT,
                    fitness_goal_progress_date TEXT, fitness_goal_exercise_category INTEGER)''')
        
    # Inserts user's fitness goals into table
    def insert_into_goal(fitness_goal_insert, fitness_goal_date, fitness_goal_category_id):
        cur.execute('''INSERT INTO fitness_goal(fitness_goal_input, fitness_goal_achieve_date,
                    fitness_goal_exercise_category) VALUES (?,?,?)''', 
                    (fitness_goal_insert, fitness_goal_date, fitness_goal_category_id))
        db.commit()
        
    # Inserts user's progress towards fitness goal
    def insert_into_goal_progress(fitness_goal_progress_input, fitness_goal_progress_date_input, fitness_goal_id):
        cur.execute('''UPDATE fitness_goal SET
                    fitness_goal_progress=?,
                    fitness_goal_progress_date=?
                    WHERE fitness_goal_exercise_category=?''',
                    (fitness_goal_progress_input, fitness_goal_progress_date_input, fitness_goal_id))
        db.commit()
        
    # Prints out all the details relating to a fitness goal
    def view_fitness_goal(id_input):
        cur.execute('''SELECT fitness_goal_input, fitness_goal_achieve_date, fitness_goal_progress,
                    fitness_goal_progress_date FROM fitness_goal WHERE fitness_goal_exercise_category=?''',
                    (id_input,))
        for f in cur:
            final = f'Your fitness goal is: {f[0]}\nYour achieve date is: {f[1]}\nYour last progress input is: {f[2]}\nYour last progress date is: {f[3]}'
        print(final)

    # This method will ensure that the user is only granted access to the fitness goals table once a 
    # fitness goal has been set 
    def view_fitness_goal_category():
        cur.execute('''SELECT fitness_goal_exercise_category FROM fitness_goal''')
        for f in cur:
            category_ids.append(f[0])

    # Updates the user's progress towards fitness goal
    def update_goal_progress_all(update_goal, new_date, category_id):
        cur.execute('''UPDATE fitness_goal SET 
                    fitness_goal_input=?,
                    fitness_goal_achieve_date=?
                    WHERE fitness_goal_exercise_category=?''',
                    (update_goal, new_date, category_id))
        db.commit()
        
    # Updates the fitness goal that the user has set
    def update_goal(update_goal, category_id):
        cur.execute('''UPDATE fitness_goal SET fitness_goal_input=?
                    WHERE fitness_goal_exercise_category=?''',
                    (update_goal, category_id))
        db.commit()

    # Updates the fitness goal's desired achieve date
    def update_goal_date(new_date, category_id):
        cur.execute('''UPDATE fitness_goal SET fitness_goal_achieve_date=?
                    WHERE fitness_goal_exercise_category=?''',
                    (new_date, category_id))
        db.commit()

    # Deletes exercise category's fitness goal
    def delete_fitness_goal(fitness_id):
        cur.execute('''DELETE from fitness_goal WHERE fitness_goal_exercise_category=?''',
                    (fitness_id,))
        db.commit()

    # Prints out an exercise category's fitness goal
    def print_fitness_goal(id_cat):
        cur.execute('''SELECT fitness_goal_input FROM fitness_goal
                    WHERE fitness_goal_exercise_category=?''',
                    (id_cat,))
        for i in cur:
            print(i[0])

# Section for user input
while True:

    option = input('''
Select an option:
1.  Add exercise category
2.  View all exercise categories
3.  Delete exercise category
4.  Add exercise by category
5.  View exercise by category
6.  Delete exercise by category
7.  Create Workout Routine 
8.  View Workout Routine
9.  View Exercise Progress
10. Update Workout Routine
11. Delete Workout Routine 
12. Set Fitness Goal (one per category)
13. Insert Progress towards Fitness Goals
14. View Fitness Goals by Category
15. Update Fitness Goals
16. Delete Fitness Goal by Category
17. Quit
''')    

    if option == '1':

        ExerciseCategory.create_table()

        while True:
            try:
                # Removes leading and trailing whitespace  
                category = input('Please input an exercise category: ').strip() 
                if category.isdigit():  # Prevents numeric inputs
                    print('Exercise category cannot contain digits or empty whitespace')
                elif category.strip() == '':    # Prevents empty whitespace
                    print('Exercise category cannot contain digits or empty whitespace')
                else:
                    ExerciseCategory.execute(category)  # Adds exercise category to table
                    print('Exercise category successfully added')
                    break
            except IntegrityError:
                print('Exercise category already exists')

    elif option == '2':

        # Populates the category list. Prevents access to users that have no exercise categories
        ExerciseCategory.lst_all_categories()
        if category_lst == []:
            print('You have no exercise categories')
        else:
            print('You have the following exercise categories:')
            ExerciseCategory.view_all_categories()  
            category_lst.clear()     # Clears the list so no duplicate values are present

    elif option == '3':

        ExerciseCategory.lst_all_categories()       # Fetches all the exercise category names from table
        if category_lst == []:  # Checks to see if the user has made exercises categories
            print('You have no exercise categories')
        else:
            print('You have the following exercise categories:')
            ExerciseCategory.view_all_categories()
            while True:
                delete_category = input('Which exercise category would you like to delete: ')
                if delete_category in category_lst: # Checks to see if the category exists
                    # Retrieves category id of the exercise category
                    cat_id = ExerciseCategory.retrieve_category_id(delete_category)
                    # Deleted categories fitness goal if it has one
                    FitnessGoal.delete_fitness_goal(cat_id)
                    # Deletes categories workout routine(s) if it has one
                    WorkoutRoutine.delete(cat_id)
                    # Deletes the exercises associated with this category
                    Exercise.delete_all_exercises(cat_id)   
                    # Deletes category if exist
                    ExerciseCategory.delete(delete_category) 
                    print('Exercise category successfully removed')
                    category_lst.clear()    # Clears the remaining items from the list so there are no duplicates
                    break
                else:
                    print('Exercise category does not exist')

    elif option == '4':

        Exercise.create_table()     # Creates the exercises table
        ExerciseCategory.lst_all_categories()   # Fetches all the exercise category names from table

        if category_lst == []:
            print('You have no exercise categories!') 
            print('You need to create exercise categories before adding exercises')
        else:
            while True:
                which_category = input('Which exercise will this category belong to: ')
                if which_category not in category_lst:  # Checks to see if exercise category exists
                    print('Exercise category does not exist')
                else:
                    while True:
                    # Retrieving the inserted exercise's category id
                        category_id = ExerciseCategory.retrieve_category_id(which_category) 
                        try:
                            exercise = input('Which exercise would you like to add to the ' + which_category + ' category: ').strip()
                            if exercise.isdigit():
                                print('Exercise cannot contain digits or empty whitespace') 
                            elif exercise.strip() == '':
                                print('Exercise cannot contain digits or empty whitespace')
                            else:
                                # Inserts the new exercise and category id into exercises table
                                Exercise.execute(exercise, category_id)
                                category_lst.clear() # SEE IF THIS IS NEEDED, IF YES PROVIDE A COMMENT
                                print('Exercise successfully saved')
                                break
                        except IntegrityError:  # Prevents identical exercises from being saved to database
                            print('Exercise already exists')
                    break

    elif option == '5':    

        ExerciseCategory.lst_all_categories()       # Fetches all the exercise category names from table
        Exercise.all_exercises()    # Fetches all the exercise names from the exercises table
        exercises_lst = []      # List for all exercise category's exercise names

        if category_lst == []:
            print('You have no exercise categories')
        elif all_exercises_lst == []:
            print('You have not created any exercises')
        else:
            while True:
                which_input = input('Which exercise category?: ')
                if not which_input in category_lst:
                    print('Exercise category does not exist')
                else:
                    # Retrieves the exercise category's id
                    cat_id = ExerciseCategory.retrieve_category_id(which_input)
                    # Fetches the exercise category's exercise names and appends it list
                    Exercise.all_category_exercises(cat_id, exercises_lst)
                    # Prints appropriate message if category has no exercises
                    if exercises_lst == []:
                        print('Exercise category has no exercises')
                    else:
                        print('You have the following exercises in the ' + which_input + ' category:\n')
                        # Displays all exercises under the inserted category
                        Exercise.print_exercise_categories(which_input) 
                        category_lst.clear()
                        break
                
    elif option == '6':     # Another thing to add, if user deletes exercise and the exercise is in a workout routine, delete the exercise from the workout routine
        
        ExerciseCategory.lst_all_categories()   # Fetches all the exercise category names from table
        Exercise.all_exercises()
        lst = []

        if category_lst == []:
            print('You have no exercise categories!')
        elif all_exercises_lst == []:
            print('You have not created any exercises')
        else:
            category_condition = True
            while category_condition:
                which_input_to_del = input('Which exercise category do you want to delete from?: ')
                if not which_input_to_del in category_lst:
                    print('Exercise category does not exist')
                else:
                    exercise_condition = True
                    while exercise_condition:
                        # Populates dictionary with key-value pairs consisting of categories and their exercises
                        Exercise.populate_dict(which_input_to_del) 
                        # Checks to see if the category has exercises assigned to it
                        all_exercises = categories_and_exercises_dict[which_input_to_del]
                        if all_exercises == []:
                            print('Category has no exercises')
                            exercise_condition = False  
                        else:
                            print('These are the exercises you currently have in the ' + which_input_to_del + ' category:')
                            # Prints out exercises from the chosen category
                            Exercise.print_exercise_categories(which_input_to_del)
                            which_exercise_to_del = input('Which exercise do you wish to delete: ')
                            # Fills list with all exercises related to the chosen category
                            for y in categories_and_exercises_dict[which_input_to_del]:
                                lst.append(y[0])
                                # Checks to see if the exercise to delete exists
                            if which_exercise_to_del in lst:   
                                # Removes exercise from workout routine if present in routine
                                WorkoutRoutine.delete_exercise(which_exercise_to_del)
                                # Deletes the exercise that the user selects
                                Exercise.delete(which_exercise_to_del)  
                                print(which_exercise_to_del + ' was successfully deleted')
                                category_lst.clear()
                                exercise_condition = False
                                category_condition = False
                            else:
                                print('Exercise does not exist\n')

    elif option == '7':     

        WorkoutRoutine.create_table()       # Creates the workout routine's table
        ExerciseCategory.lst_all_categories()   # Fetches all the exercise category names from table    
        Exercise.all_exercises()

        category_exercises = [] # Holds the exercises of the category that the user chooses
        if category_lst == []:
            print('You have no exercise categories!')
        elif all_exercises_lst == []:
            print('You have not created any exercises')
        else:
            routine_category = True
            while routine_category:
                workout_routine_category = input('Which workout category will this routine belong to: ')
                if not workout_routine_category in category_lst:
                    print('Exercise category does not exist')
                else:
                     # Stores the category's exercises in dictionary 
                    Exercise.populate_dict(workout_routine_category)   
                    for x in categories_and_exercises_dict[workout_routine_category]:
                        category_exercises.append(x[0])     # Fetches category's exercises and appends them to list
                    if category_exercises == []:   
                        print('Exercise category has no exercises. You need to create exercises before routines')
                    else:
                        name = True
                        while name:
                            # Retrieving category id
                            category_id = ExerciseCategory.retrieve_category_id(workout_routine_category)
                            # Appends workout routine names from workout_routine table into workout_routine_names
                            WorkoutRoutine.workout_routine_lst_names(category_id)
                            routine_name = input('Give this routine a name: ')
                            if routine_name.strip() == '':
                                print('Invalid input')
                            elif routine_name in workout_routine_names:     # Prevents duplicate routine names
                                print('Workout routine name already exists')
                            else:
                                add_exercise = True 
                                while add_exercise:
                                    command = ''
                                    print('These are the exercises you have in the ' + workout_routine_category + ' category:\n')
                                    # Prints out the exercises in the chosen workout routine
                                    Exercise.print_exercise_categories(workout_routine_category)
                                    which_exercise = input('\nWhich exercise would you like to add to your routine: ').strip()
                                    if which_exercise in exercises_in_routine:
                                        print('Exercise already added to routine\n')    # Prevents duplicate values from being entered
                                    elif not which_exercise in category_exercises:
                                        print('Exercise does not exist')
                                    else:
                                        # Appends exercise to list
                                        exercises_in_routine.append(which_exercise) 
                                        category_exercises.remove(which_exercise)
                                        program = True   
                                        while program:
                                            print('''
Enter 1 to enter more exercises to your workout routine
Enter 2 to move on''')
                                            try:
                                                command = int(input('> '))
                                            except ValueError:
                                                print('Only numbers please')
                                            if command == 1 and category_exercises == []:
                                                print('You have no exercises left to add to the routine')
                                                continue
                                            elif command == 1 and category_exercises != []:
                                                break
                                            elif command == 2:
                                                # Calls the choose_own_param method for users to select exercise parameters for their chosen exercise
                                                CreateWorkout.choose_own_param(exercises_in_routine)
                                                print(f'{routine_name} successfully saved')
                                                exercises_in_routine.clear()
                                                program = False
                                                add_exercise = False
                                                name = False
                                                routine_category = False
                                            else:
                                                print('Invalid')
    elif option == '8': 
        
        ExerciseCategory.lst_all_categories()       # Fetches all the exercise category names from table
        WorkoutRoutine.all_routines()       # Appends all workout routines to routines_all_lst
        unique_list = []

        if category_lst == []:
            print('You have no exercise categories')
        elif routine_lst_all == []:
            print('You have no workout routines')
        else:
            # Used to prevent program from breaking if inserted category has no workout routine 
            exercise_category = True
            while exercise_category:
                which = input('Enter the workout category you would like to view: ')    
                if not which in category_lst:
                    print('Exercise category does not exist')
                else:
                    workout_routine = True
                    while workout_routine:
                        ex_id = ExerciseCategory.retrieve_category_id(which)
                        WorkoutRoutine.lst_of_routines(ex_id)
                        if routine_lst == []:
                            print('Exercise category has no workout routines')
                            break
                        else:
                            print(f'These are the following workout routines you have in the {which} category:')
                            for i in routine_lst:
                                if not i in unique_list:
                                    unique_list.append(i)   # Only appends unique routines to list
                            print(*unique_list, sep='\n')   # Prints out items from list without loop
                            input_routine = input('\nType in the workout routine you would like to view: ')
                            if not input_routine in routine_lst:
                                print('Workout routine does not exist')
                                routine_lst.clear()
                            else:
                                print()
                                WorkoutRoutine.view(input_routine)
                                category_lst.clear()    
                                routine_lst.clear()
                                workout_routine = False
                                exercise_category = False

    elif option == '9':

        ExerciseCategory.lst_all_categories()       # Fetches all the exercise category names from table
        WorkoutRoutine.all_routines()       # Appends all workout routines to routines_all_lst
        unique_list2 = []
        lst_of_completed_exercises = [] 

        if category_lst == []:
            print('You have no exercise categories')
        elif routine_lst_all == []:
            print('You have no workout routines')
        else:
            category_condition = True
            while category_condition:
                category_input = input('Which exercise category are you currently busy with: ')
                if not category_input in category_lst:
                    print('Exercise category does not exist')
                else:
                    routine_condition = True
                    while routine_condition:
                        category_id = ExerciseCategory.retrieve_category_id(category_input)
                        WorkoutRoutine.lst_of_routines(category_id)
                        if routine_lst == []:
                            print('Exercise category has no routines')
                            break
                        else:
                            for i in routine_lst:
                                if not i in unique_list2:
                                    unique_list2.append(i)
                            print(*unique_list2, sep='\n')   # Prints out the items in routine_lst
                            routine_name = input('Which of the above exercise routines are you doing?: ') 
                            if not routine_name in routine_lst:
                                print('Routine name does not exist')
                                routine_lst.clear() # Prevents routines being repeatedly added to list
                            else:
                                WorkoutRoutine.exercises_in_routine(routine_name)
                                command_input = ''
                                while command_input != '2':
                                    print('''
Enter the command you wish to do:
1: To add completed exercises
2: To quit, once all completed exercises have been added
''')
                                    command_input = input('Enter the command you wish to do: ')
                                    if command_input == '1':
                                        while True: 
                                            # Takes user back if there are no exercises left to mark off
                                            if exercises_in_routine == []:
                                                print('You have no more exercises left in workout routine')
                                                break
                                            else:   
                                                WorkoutRoutine.view_workout_routine_exercises(routine_name)
                                                completed_exercise = input('Which of the above exercise have you completed in the ' + category_input + ' category: ')   # PRINT OUT THE EXERCISE NAMES FOR THE USER TO MAKE IT EASIER TO REMEMBER
                                                if not completed_exercise in exercises_in_routine and completed_exercise in lst_of_completed_exercises:
                                                    print('Exercise already marked off as complete')
                                                    break
                                                if not completed_exercise in exercises_in_routine and not completed_exercise in lst_of_completed_exercises:
                                                    print('Exercise doesn\'t exist in the ' + category_input + ' category')
                                                else:
                                                    exercises_in_routine.remove(completed_exercise)
                                                    lst_of_completed_exercises.append(completed_exercise)
                                                    break
                                    elif command_input == '2':
                                        print('You have the following exercises in the ' + routine_name + ' exercise routine:')
                                        print()
                                        if exercises_in_routine == []:
                                            print('You have completed your workout. Great job')
                                            routine_condition = False
                                            category_condition = False
                                        else:
                                            for routine in exercises_in_routine:
                                                print(routine)
                                                WorkoutRoutine.print_exercise_description(routine_name, routine)
                                            exercises_in_routine.clear()
                                            routine_lst.clear() 
                                            routine_condition = False
                                            category_condition = False
                                    else:
                                        print('Invalid option')   

    elif option == '10':
        
        ExerciseCategory.lst_all_categories()  # Fetches all the exercise category names from exercise category table
        WorkoutRoutine.all_routines()       # Appends all workout routines to routines_all_lst
        lst_of_exercise_names = []  # Stores the exercise names from exercise category
        descrip_info = []   # Stores the description information of new exercises for workout routine
        final_str = ''      # Will be used to gather each parameter's description for new exercise 
        lst = []        # Holds the exercise the user wishes to update
        description_info = ''   # String to hold all the updated exercise description
        
        if category_lst == []:
            print('You have no exercise categories')
        elif routine_lst_all == []:
            print('You have no workout routines')
        else:
            category = True
            while category:
                workout_routine_category = input('Which exercise category does the workout routine that you want to update belong to: ')
                if not workout_routine_category in category_lst:
                    print('Exercise category does not exist')
                else:
                    category_id = ExerciseCategory.retrieve_category_id(workout_routine_category)
                    WorkoutRoutine.lst_of_routines(category_id)
                    if routine_lst == []:
                        print('Exercise category has no routines')
                    else:
                        workout_routine = True
                        while workout_routine:
                            WorkoutRoutine.workout_routine_lst_names(category_id)
                            print('You have the following workout routines in the ' + workout_routine_category + ' category:')
                            # Prints out workout routines from exercise category
                            print(*workout_routine_names, sep='\n')
                            routine_name = input('Which routine do you want to update: ')
                            if not routine_name in workout_routine_names:
                                print('Workout routine does not exist')
                            else:
                                exercises = True
                                while exercises:     # Find out which list to use as parameter
                                    change = input('''
Enter 1 if you wish to add an exercise to an existing workout routine
Enter 2 if you wish to replace an exercise's description 
Enter 3 if you wish to delete an exercise and its description
''')

                                    if change == '1': 

                                        while True:
                                            Exercise.populate_dict(workout_routine_category)
                                            # Appends exercise names from exercise category to list
                                            for i in categories_and_exercises_dict[workout_routine_category]:
                                                lst_of_exercise_names.append(i[0])
                                            # Will be used to check if the exercise the user inputs already exists in workout routine
                                            WorkoutRoutine.exercises_in_routine(routine_name)
                                            # Prints out all the exercises in category
                                            Exercise.print_exercise_categories(workout_routine_category)
                                            which_to_add = input(f'Which of the above exercises do you want to add to the {routine_name} workout routine: ')
                                            if not which_to_add in lst_of_exercise_names:
                                                print('Exercise does not exist in exercise category')
                                            elif which_to_add in exercises_in_routine:
                                                print('Exercise already in workout routine')
                                                exercises_in_routine.clear()
                                            else:
                                                advance = True
                                                while advance:
                                                    print('''
Enter 1 to add new parameter to your workout for ''' + which_to_add + '''
Enter 2 to move on once you're done picking
''')
                                                    select = input('Enter the command you would like to do: ')

                                                    if select == '1':

                                                        select_option = True
                                                        while select_option:
                                                            print('''
Please select the number that relates to the parameter of your choosing
1 - Sets
2 - Reps
3 - Weight
4 - Total time
5 - Distance
6 - Time structure
7 - Additional info
''')
                                                            option = input('Enter the command you wish to do: ')

                                                            if option == '1':

                                                                add_description = True
                                                                while add_description:
                                                                    sets = input(f'Enter the number of sets you would like for {which_to_add}: ')   # Once this is all sorted, replace 'this exercise' with the name of the exercise
                                                                    if sets.strip == '':
                                                                        print('Invalid')
                                                                    else:
                                                                        # Appends the description of final_sets to list
                                                                        final_sets = f'The number of sets for this {which_to_add} is: {sets}'
                                                                        descrip_info.append(final_sets)
                                                                        add_description = False
                                                                        select_option = False

                                                            elif option == '2':

                                                                add_description = True
                                                                while add_description:
                                                                    reps = input(f'Enter the number of reps you would like for {which_to_add}: ')
                                                                    if reps.strip() == '':
                                                                        print('Invalid')
                                                                    else:
                                                                        # Appends the description of final_reps to list
                                                                        final_reps = f'The number of reps you have for {which_to_add} is: {reps}'
                                                                        descrip_info.append(final_reps)
                                                                        add_description = False
                                                                        select_option = False

                                                            elif option == '3':

                                                                add_description = True
                                                                while add_description:
                                                                    weight = input(f'Enter the amount of weight you would like for {which_to_add}: ')
                                                                    if weight.strip() == '':
                                                                        print('Invalid')
                                                                    else:
                                                                        # Appends the description of final_weight to list
                                                                        final_weight = f'The amount of weight you\'re using for {which_to_add} is: {weight}'
                                                                        descrip_info.append(final_weight)
                                                                        add_description = False
                                                                        select_option = False

                                                            elif option == '4':

                                                                add_description = True
                                                                while add_description:
                                                                    time = input(f'Enter the amount of time you would like to spend on {which_to_add}: ')
                                                                    if time.strip() == '':
                                                                        print('Invalid')
                                                                    else:
                                                                        # Appends the description of final_time to list
                                                                        final_time = f'The total time you are spending on {which_to_add} is: {time}'
                                                                        descrip_info.append(final_time)
                                                                        add_description = False
                                                                        select_option = False

                                                            elif option == '5':

                                                                add_description = True
                                                                while add_description:
                                                                    distance = input(f'Enter the distance you wish to cover for {which_to_add}: ')
                                                                    if distance.strip() == '':
                                                                        print('Invalid')
                                                                    else:
                                                                        # Appends the description of final_distance to list
                                                                        final_distance = f'The total distance you are covering for {which_to_add} is: {distance}'
                                                                        descrip_info.append(final_distance)
                                                                        add_description = False
                                                                        select_option = False

                                                            elif option == '6':

                                                                add_description = True
                                                                while add_description:
                                                                    time_structure = input(f'Enter the time structure you would like to use for {which_to_add}: ')
                                                                    if time_structure.strip() == '':
                                                                        print('Invalid')
                                                                    else:
                                                                        # Appends the description of time_structure to list
                                                                        final_time_structure = f'The time structure that you are using for {which_to_add} is: {time_structure}'
                                                                        descrip_info.append(final_time_structure)
                                                                        add_description = False
                                                                        select_option = False

                                                            elif option == '7':

                                                                add_description = True
                                                                while add_description:
                                                                    additional_info = input(f'Enter any additional information you would like to add for {which_to_add}: ')
                                                                    if additional_info.strip() == '':
                                                                        print('Invalid')
                                                                    else:
                                                                        # Appends the additional information to list
                                                                        final_info = f'Additional information that was added is: {additional_info}'
                                                                        descrip_info.append(final_info)
                                                                        add_description = False
                                                                        select_option = False
                                                            else:
                                                                print('Invalid')
                
                                                    elif select == '2':
                                                        for descrip in descrip_info:
                                                            final_str += descrip + '\n'
                                                        # Adds the new exercise and its description to workout routine table
                                                        WorkoutRoutine.execute_workout_routine(routine_name, which_to_add, final_str, category_id)
                                                        select_option = False
                                                        advance = False
                                                        exercises = False
                                                        workout_routine = False
                                                        category = False
                                                    else:
                                                        print('Invalid')
                                                break

                                    elif change == '2':

                                        print(f'You have the following exercises in the {routine_name} category:')
                                        WorkoutRoutine.view_workout_routine_exercises(routine_name)   
                                        WorkoutRoutine.exercises_in_routine(routine_name)
                                        update = input('Which exercise in the routine do you wish to update: ')
                                        if not update in exercises_in_routine:
                                            print('Exercise does not exist in workout routine')
                                        else:
                                            lst.append(update)
                                            exercise_to_update = True
                                            while exercise_to_update:
                                                print(f'The following is the exercise description you have for {update}:\n')
                                                a = WorkoutRoutine.print_exercise_description(routine_name, update) 
                                                print('''
Enter 1 to add new parameter to your workout for ''' + update + '''
Enter 2 to move on once you're done picking
''')
                                                select = input('Enter the command you would like to do: ')

                                                if select == '1':

                                                    select_option = True
                                                    while select_option:
                                                        print('''
Please select the number that relates to the parameter of your choosing
1 - Sets
2 - Reps
3 - Weight
4 - Total time
5 - Distance
6 - Time structure
7 - Additional info
''')
                                                        option = input('Enter the command you wish to do: ')

                                                        if option == '1':

                                                            add_description = True
                                                            while add_description:
                                                                sets = input(f'Enter the number of sets you would like for {update}: ')   # Once this is all sorted, replace 'this exercise' with the name of the exercise
                                                                if sets.strip == '':
                                                                    print('Invalid')
                                                                else:
                                                                    # Adds the description of final_sets to string
                                                                    final_sets = f'The number of sets for this {update} is: {sets}'
                                                                    description_info += final_sets + '\n'
                                                                    add_description = False
                                                                    select_option = False

                                                        elif option == '2':

                                                            add_description = True
                                                            while add_description:
                                                                reps = input(f'Enter the number of reps you would like for {update}: ')
                                                                if reps.strip() == '':
                                                                    print('Invalid')
                                                                else:
                                                                    # Adds the description of final_reps to string
                                                                    final_reps = f'The number of reps you have for {update} is: {reps}'
                                                                    description_info += final_reps + '\n'
                                                                    add_description = False
                                                                    select_option = False

                                                        elif option == '3':

                                                            add_description = True
                                                            while add_description:
                                                                weight = input(f'Enter the amount of weight you would like for {update}: ')
                                                                if weight.strip() == '':
                                                                    print('Invalid')
                                                                else:
                                                                    # Adds the description of final_weight to string
                                                                    final_weight = f'The amount of weight you\'re using for {update} is: {weight}'
                                                                    description_info += final_weight + '\n'
                                                                    add_description = False
                                                                    select_option = False

                                                        elif option == '4':

                                                            add_description = True
                                                            while add_description:
                                                                time = input(f'Enter the amount of time you would like to spend on {update}: ')
                                                                if time.strip() == '':
                                                                    print('Invalid')
                                                                else:
                                                                    # Adds the description of final_time to string
                                                                    final_time = f'The total time you are spending on {update} is: {time}'
                                                                    description_info += final_time + '\n'
                                                                    add_description = False
                                                                    select_option = False

                                                        elif option == '5':

                                                            add_description = True
                                                            while add_description:
                                                                distance = input(f'Enter the distance you wish to cover for {update}: ')
                                                                if distance.strip() == '':
                                                                    print('Invalid')
                                                                else:
                                                                    # Adds the description of final_distance to string
                                                                    final_distance = f'The total distance you are covering for {update} is: {distance}'
                                                                    description_info += final_distance + '\n'
                                                                    add_description = False
                                                                    select_option = False

                                                        elif option == '6':

                                                            add_description = True
                                                            while add_description:
                                                                time_structure = input(f'Enter the time structure you would like to use for {update}: ')
                                                                if time_structure.strip() == '':
                                                                    print('Invalid')
                                                                else:
                                                                    # Adds the description of final_time_structure to string
                                                                    final_time_structure = f'The time structure that you are using for {update} is: {time_structure}'
                                                                    description_info += final_time_structure + '\n'
                                                                    add_description = False
                                                                    select_option = False

                                                        elif option == '7':

                                                            add_description = True
                                                            while add_description:
                                                                additional_info = input(f'Enter any additional information you would like to add for {update}: ')
                                                                if additional_info.strip() == '':
                                                                    print('Invalid')
                                                                else:
                                                                    # Adds the additional information to string
                                                                    final_info = f'Additional information that was added is: {additional_info}'
                                                                    description_info += final_info + '\n'
                                                                    add_description = False
                                                                    select_option = False
                                                        else:
                                                            print('Invalid')
        
                                                elif select == '2':
                                                    WorkoutRoutine.update_workout_description(description_info, routine_name, update)
                                                    print('\n'+description_info)
                                                    # WorkoutRoutine.update_workout_description()
                                                    advance = False
                                                    exercise_to_update = False
                                                    exercises = False
                                                    workout_routine = False
                                                    category = False
                                                else:
                                                    print('Invalid')
                                    elif change == '3':
                                        WorkoutRoutine.delete_routine_exercise(routine_name, update)
                                        advance = False
                                        exercise_to_update = False
                                        exercises = False
                                        workout_routine = False
                                        category = False
                                    else:
                                        print('Invalid')

    elif option == '11':

        ExerciseCategory.lst_all_categories() # Fetches all the exercise category names from exercise category table
        WorkoutRoutine.all_routines()       # Appends all workout routines to routines_all_lst
        unique_routine_list = []
        if category_lst == []:
            print('You have no exercise categories')
        elif routine_lst_all == []:    
            print('You have no workout routines')
        else:
            delete_condition = True
            while delete_condition:
                delete_input = input('Which category does the workout routine you want to delete belong to: ')
                if not delete_input in category_lst:
                    print('Exercise category does not exist')
                else:   
                    delete_id = ExerciseCategory.retrieve_category_id(delete_input)
                    WorkoutRoutine.lst_of_routines(delete_id)
                    if routine_lst == []:
                        print('Exercise category has no routines')
                    else:
                        routine = True
                        while routine:
                            print('These are the workout routines you have in the ' + delete_input + ' category: ')
                            # Appends unique workout routine names to list only
                            for i in routine_lst:
                                if not i in unique_routine_list:
                                    unique_routine_list.append(i)
                            print(*unique_routine_list, sep='\n')
                            delete = input('Which of the following workout routines do you wish to delete: ')
                            if not delete in unique_routine_list:
                                print('Workout routine does not exist')
                            else:   
                                # Deletes chosen routine
                                WorkoutRoutine.delete_workout_routine(delete)
                                print('Workout routine successfully deleted')
                                category_lst.clear()
                                routine_lst.clear()
                                routine = False
                                delete_condition = False

    elif option == '12':   

        FitnessGoal.create_table()
        ExerciseCategory.lst_all_categories() # Fetches all the exercise category names from exercise category table

        if category_lst == []:
            print('You have no exercise categories. Cannot proceed')
        else:
            category_condition = True
            while category_condition:
                fitness_goal_exercise_category = input('Which exercise category will this fitness goal belong to: ')
                if not fitness_goal_exercise_category in category_lst:
                    print('Exercise category does not exist')
                else:
                    fitness_condition = True
                    while fitness_condition:
                        exercise_category_id_num = ExerciseCategory.retrieve_category_id(fitness_goal_exercise_category)
                        FitnessGoal.view_fitness_goal_category()
                        if exercise_category_id_num in category_ids:
                            print('Exercise category already has a fitness goal. Once goal is completed, you may add another')
                            break
                        else:
                            set_fitness_goal = input('Set a fitness goal for the ' + fitness_goal_exercise_category + ' category: ').strip()
                            if set_fitness_goal.strip() == '':
                                print('Invalid input. Please enter a fitness goal')
                            else:
                                while True:
                                    set_fitness_goal_date = input('Set a date you wish to achieve your fitness goal: ').strip()
                                    if set_fitness_goal_date == '':
                                        print('Invalid input. Please enter a date you wish to achieve your fitness goal')
                                    else:
                                        FitnessGoal.insert_into_goal(set_fitness_goal, set_fitness_goal_date, exercise_category_id_num)
                                        fitness_condition = False
                                        category_condition = False
                                        break

    elif option == '13': 

        # Fetches all the exercise category names from table and stores it in category_lst
        ExerciseCategory.lst_all_categories()
        # Stores all exercise category's id's that have a fitness goal in list
        FitnessGoal.view_fitness_goal_category()

        if category_lst == []:
            print('You have no exercise categories. Cannot proceed')
        elif category_ids == []:
            print('You have not set a fitness goal. Cannot proceed')
        else:
            while True:
                fitness_goal_input = input('Enter the Exercise Category that this fitness goal belongs to: ')
                if not fitness_goal_input in category_lst:
                    print('Exercise category does not exist')
                elif fitness_goal_input.strip() == '':
                    print('Invalid input. Enter a valid response')
                else:
                    a = ExerciseCategory.retrieve_category_id(fitness_goal_input)
                    FitnessGoal.view_fitness_goal_category()
                    if not a in category_ids:
                        print('Exercise category does not have a fitness goal')
                    else:
                        while True: 
                            print('This is the fitness goal you chose for the ' + fitness_goal_input + ' category:')
                            FitnessGoal.print_fitness_goal(a)
                            fitness_goal_progress = input('Enter your fitness goal progress in the ' + fitness_goal_input + ' exercise category: ').strip()
                            if fitness_goal_progress.strip() == '':
                                print('Invalid input. Enter a valid response')
                            else:
                                while True:
                                    fitness_goal_date_input = input('Enter the current date: ').strip() 
                                    if fitness_goal_date_input.strip() == '':
                                        print('Invalid input. Enter a valid response')
                                    else:
                                        # Inserts user progress towards goal into fitness goal table 
                                        FitnessGoal.insert_into_goal_progress(fitness_goal_progress, fitness_goal_date_input, a)
                                        category_ids.clear()
                                        break
                                break
                        break

    elif option == '14': 

        # Fetches all the exercise category names from table
        ExerciseCategory.lst_all_categories()       
        # Stores all exercise category's id's that have a fitness goal in list
        FitnessGoal.view_fitness_goal_category()

        if category_lst == []:
            print('You have no exercise categories. Cannot proceed')
        elif category_ids == []:
            print('You have not set a fitness goal. Cannot proceed')
        else:
            while True:
                fitness_goal_input = input('Enter the Exercise Category that this fitness goal belongs to: ')
                if not fitness_goal_input in category_lst:
                    print('Exercise category does not exist')
                elif fitness_goal_input.strip() == '':
                    print('Invalid input. Enter a valid response')
                else:
                    a = ExerciseCategory.retrieve_category_id(fitness_goal_input)
                    FitnessGoal.view_fitness_goal_category()
                    if not a in category_ids:
                        print('Exercise category does not have a fitness goal')
                    if a in category_ids:
                        print()
                        # Prints out the exercise category's fitness goal
                        FitnessGoal.view_fitness_goal(a)
                        break

    elif option == '15':    

        # Fetches all the exercise category names from table
        ExerciseCategory.lst_all_categories()       
        # Stores all exercise category's id's that have a fitness goal in list
        FitnessGoal.view_fitness_goal_category()

        if category_lst == []:
            print('You have no exercise categories. Cannot proceed')
        elif category_ids == []:
            print('You have not set a fitness goal. Cannot proceed')
        else:
            fitness_goal = True
            while fitness_goal:
                fitness_goal_input = input('Enter the Exercise Category that this fitness goal belongs to: ')
                if not fitness_goal_input in category_lst:
                    print('Exercise category does not exist')
                elif fitness_goal_input.strip() == '':
                    print('Invalid input. Enter a valid response')
                else:
                    a = ExerciseCategory.retrieve_category_id(fitness_goal_input)
                    FitnessGoal.view_fitness_goal_category()
                    if not a in category_ids:
                        print('Exercise category does not have a fitness goal')
                    else:
                        update = True
                        while update:
                            option = input('''
Enter 1 to change both the fitness goal's description and its achieve date
Enter 2 to only change the fitness goal's description
Enter 3 to only change the fitness goal's achieve date
''')
                            if option == '1':
                                while True:
                                    fitness_goal_update = input('Update your fitness goal in the ' + fitness_goal_input + ' category: ').strip()
                                    if fitness_goal_update.strip() == '':
                                        print('Invalid input. Enter a valid response')
                                    else:
                                        break
                                while True:
                                    new_date = input('Enter the fitness goal\'s new date: ')
                                    if new_date.strip() == '':
                                        print('Invalid input. Enter a valid response')
                                    else:
                                        # Updates exercise category's fitness goal and achieve date
                                        FitnessGoal.update_goal_progress_all(fitness_goal_update, new_date, a)
                                        update = False
                                        fitness_goal = False
                                        break
                            elif option == '2':
                                while True:
                                    fitness_goal_update = input('Update your fitness goal in the ' + fitness_goal_input + ' category: ').strip()
                                    if fitness_goal_update.strip() == '':
                                        print('Invalid input. Enter a valid response')
                                    else:
                                        # Updates the exercise category's fitness goal
                                        FitnessGoal.update_goal(fitness_goal_update, a)
                                        update = False
                                        fitness_goal = False
                                        break
                            elif option == '3':
                                while True:
                                    new_date = input('Enter the fitness goal\'s new date: ')
                                    if new_date.strip() == '':
                                        print('Invalid input. Enter a valid response')
                                    else:
                                        # Updates the fitness goal's achieve date
                                        FitnessGoal.update_goal_date(new_date, a)
                                        update = False
                                        fitness_goal = False
                                        break
                            else:
                                print('Invalid response')
                            

    elif option == '16': 

        # Fetches all the exercise category names from table
        ExerciseCategory.lst_all_categories()       
        # Stores all exercise category's id's that have a fitness goal in list
        FitnessGoal.view_fitness_goal_category()

        if category_lst == []:
            print('You have no exercise categories. Cannot proceed')
        elif category_ids == []:
            print('You have not set a fitness goal. Cannot proceed')
        else:
            while True:
                fitness_goal_input = input('Enter the Exercise Category that this fitness goal belongs to: ')
                if not fitness_goal_input in category_lst:
                    print('Exercise category does not exist')
                elif fitness_goal_input.strip() == '':
                    print('Invalid input. Enter a valid response')
                else:
                    a = ExerciseCategory.retrieve_category_id(fitness_goal_input)
                    FitnessGoal.view_fitness_goal_category()
                    if not a in category_ids:
                        print('Exercise category does not have a fitness goal')
                    if a in category_ids:
                        # Deletes the exercise category's fitness goal
                        FitnessGoal.delete_fitness_goal(a)
                        break

    elif option == '17':

        print('Bye')
        break
    
    else:
        print('Invalid.')


'''
References:

I used the following article as a guideline to help me structure my various classes:
https://codereview.stackexchange.com/questions/182700/python-class-to-manage-a-table-in-sqlite

The following article helped me update multiple columns:
https://stackoverflow.com/questions/808418/how-to-update-two-columns-in-one-statement

I used the following article to convert a tuple to an integer:
https://www.geeksforgeeks.org/python-convert-tuple-to-integer/

I Used the following article to elegantly print out the items in a list without using a loop 
https://stackoverflow.com/questions/37084246/printing-using-list-comprehension
'''
