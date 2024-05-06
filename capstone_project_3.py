import sqlite3
from sqlite3 import IntegrityError


db = sqlite3.connect('fitness_tracker_app')
cur = db.cursor()

exercises_in_routine = []  # This holds all the exercise names the user adds to their workout routine
exercise_count = 0         # Variable that keeps track of how many exercises are left in a user's category

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

class WorkoutRoutine:   

    # Creates a table for the workout routine
    def create_table():     
        cur.execute('''CREATE TABLE IF NOT EXISTS workout_routine
                    (workout_routine_id INTEGER PRIMARY KEY, workout_routine_name TEXT, 
                    workout_routine_exercise TEXT, workout_description TEXT, exercise_category_id)''')

    def insert_workout_routine(routine_name, exercise, exercise_routine_id):
        cur.execute('''INSERT INTO workout_routine(workout_routine_name, workout_routine_exercise,
                    exercise_category_id) VALUES(?,?,?)''',
                    (routine_name, exercise, exercise_routine_id))
        db.commit()

    # Prints out the exercises and its descriptions from a particular workout routine
    def view(exercise_name):    
        cur.execute('''SELECT workout_routine_exercise, workout_description FROM workout_routine
                    WHERE workout_routine_name=?''', (exercise_name,))
        for j in cur:
            print(j[0], '-', j[1])
        
    # Updates exercises workout description of a particular workout routine
    def update_workout_description(new_description, routine, exercise):
        cur.execute('''UPDATE workout_routine SET workout_description=?
                    WHERE workout_routine_name=? AND workout_routine_exercise=?''', 
                    (new_description, routine, exercise))
        db.commit()

    # Deletes workout routine 
    def delete_workout_routine(delete_routine, exercise_category_id):
        cur.execute('''DELETE FROM workout_routine WHERE workout_routine_name=?
                    AND exercise_category_id=?''', (delete_routine, exercise_category_id))
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

class CreateWorkout:      # ADD ADDITIONAL FUNCTIONALITIES TO CLASS TO ALLOW IT TO ALLOW IT TO UPDATE WORKOUT ROUTINES (SEE OPTION 10)

    # The following method allows users to select their own parameters for the workout routines they make
    def choose_own_param(exercise):      # List of all exercises the user aims to include in workout routine

        str_of_description_info = ''    # String to hold each exercises descriptions
        start = True        
        while start:

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
            
                elif select == '2':     # SEE IF YOU CAN HAVE AN IDENTIFIER, IF YOU'RE COMING FROM OPTION 7 (CREATING A WORKOUT ROUTINE, USE ID 1 FOR INSTANCE), IF YOU'RE COMING FROM UPDATING A WORKOUT ROUTINE (ADDING OR CHANGING) USE ANOTHER IDENTIFIER. THESE IDENTIFIERS WILL ALTER THE LOGIC THAT IS APPLIED TO THIS CLASS
                    if str_of_description_info.strip() != '':
                        # From here on out, just execute an update cur call, regardless of whether user is updating a an existent exercise or not.
                        WorkoutRoutine.update_workout_description(str_of_description_info, routine_name, exercise)
                        str_of_description_info = ''    # Emptying the string for next exercise
                        advance = False
                        start = False
                    else:
                        print('You need to insert parameters for the exercises you choose')
                else:
                    print('Invalid')

class FitnessGoal:  

    # Creates a table for the fitness goal
    def create_table():
        cur.execute('''CREATE TABLE IF NOT EXISTS fitness_goal
                    (fitness_goal_id INTEGER PRIMARY KEY, fitness_goal_exercise, 
                    fitness_goal_input TEXT UNIQUE, fitness_goal_achieve_date TEXT, 
                    fitness_goal_progress TEXT, fitness_goal_progress_date TEXT, 
                    fitness_goal_exercise_category INTEGER)''')
        
    # Inserts user's fitness goals into table
    def insert_into_goal(fitness_goal_exercise, fitness_goal_insert, fitness_goal_date, fitness_goal_category_id):
        cur.execute('''INSERT INTO fitness_goal(fitness_goal_exercise, fitness_goal_input, 
                    fitness_goal_achieve_date, fitness_goal_exercise_category) VALUES (?,?,?,?)''', 
                    (fitness_goal_exercise, fitness_goal_insert, fitness_goal_date, fitness_goal_category_id))
        db.commit()
        
    # Inserts user's progress towards fitness goal
    def insert_into_goal_progress(fitness_goal_progress_input, fitness_goal_progress_date_input, fitness_goal_id):
        cur.execute('''UPDATE fitness_goal 
                    SET fitness_goal_progress=?,
                    fitness_goal_progress_date=?
                    WHERE fitness_goal_exercise_category=?''',
                    (fitness_goal_progress_input, fitness_goal_progress_date_input, fitness_goal_id))
        db.commit()
        
    # Updates the fitness goal that the user has set
    def update_goal(update_goal, category_id):
        cur.execute('''UPDATE fitness_goal 
                    SET fitness_goal_input=?
                    WHERE fitness_goal_exercise_category=?''',
                    (update_goal, category_id))
        db.commit()

    def update_and_overwrite(updated_health_goal, fitness_goal_id, updated_goal_progress=None, updated_progress_date=None):
        cur.execute('''UPDATE fitness_goal_health
                    SET fitness_goal_input=?,
                    fitness_goal_progress=?,
                    fitness_goal_progress_date=?
                    WHERE fitness_goal_id=?''',
                    (updated_health_goal, updated_goal_progress, updated_progress_date, fitness_goal_id))
        db.commit()

    # Deletes exercise category's fitness goal
    def delete_fitness_goal(fitness_id):
        cur.execute('''DELETE FROM fitness_goal WHERE fitness_goal_exercise_category=?''',
                    (fitness_id,))
        db.commit()

    def delete(fitness_id):
        cur.execute('''DELETE FROM fitness_goal WHERE fitness_goal_id=?''',
                    (fitness_id,))
        db.commit()

    def print_out_selection():
        cur.execute('''SELECT fitness_goal_id, fitness_goal_exercise, fitness_goal_input
                    FROM fitness_goal''')
        for row in cur:
            print(row[0], '-', row[1], '-', row[2])

class FitnessGoalHealth:

    def create_table():
        cur.execute('''CREATE TABLE IF NOT EXISTS fitness_goal_health
                    (fitness_goal_id INTEGER PRIMARY KEY, 
                    fitness_goal_input TEXT, fitness_goal_progress TEXT, fitness_goal_end_date TEXT, 
                    fitness_goal_progress_date TEXT)''')
        
    def insert_into_goal(fitness_goal_input, fitness_goal_progress_date):
        cur.execute('''INSERT INTO fitness_goal_health 
                    (fitness_goal_input, fitness_goal_end_date) VALUES (?,?)''', 
                    (fitness_goal_input, fitness_goal_progress_date))
        db.commit()

    def insert_into_goal_progress(fitness_goal_progress, fitness_goal_progress_date, fitness_goal_id):
        cur.execute('''UPDATE fitness_goal_health 
                    SET fitness_goal_progress=?,
                    fitness_goal_progress_date=?
                    WHERE fitness_goal_id=?''',
                    (fitness_goal_progress, fitness_goal_progress_date, fitness_goal_id))
        db.commit()

    def update_health_goal(updated_health_goal, fitness_goal_id):
        cur.execute('''UPDATE fitness_goal_health
                    SET fitness_goal_input=?
                    WHERE fitness_goal_id=?''',
                    (updated_health_goal, fitness_goal_id))
        
    def update_and_overwrite(updated_health_goal, fitness_goal_id, updated_goal_progress=None, updated_progress_date=None):
        cur.execute('''UPDATE fitness_goal_health
                    SET fitness_goal_input=?,
                    fitness_goal_progress=?,
                    fitness_goal_progress_date=?
                    WHERE fitness_goal_id=?''',
                    (updated_health_goal, updated_goal_progress, updated_progress_date, fitness_goal_id))
        db.commit()

    def update_target_date(updated_target_date, fitness_goal_id):
        cur.execute('''UPDATE fitness_goal_health
                    SET fitness_goal_end_date=?
                    WHERE fitness_goal_id=?''',
                    (updated_target_date, fitness_goal_id))
        db.commit()
        
    def print_out_selection():
        cur.execute('''SELECT * FROM fitness_goal_health''')
        for row in cur:
            print(row[1], '-', row[2], '-', row[3], '-', row[4])

    def delete_goal(goal_id):
        cur.execute('''DELETE FROM fitness_goal_health
                    WHERE fitness_goal_id=?''', (goal_id,))
        db.commit()

# Section for user input

# MAYBE BEFORE YOU START WORKING ON THE APP, RUN ALL THE create_table() functions

ExerciseCategory.create_table()
Exercise.create_table()
WorkoutRoutine.create_table()
FitnessGoal.create_table()
FitnessGoalHealth.create_table()


while True:

    option = input('''
Select an option:
1.  Add Exercise Category
2.  View all Exercise Categories
3.  Delete Exercise Category
4.  Add Exercise by Category
5.  View Exercise by Category
6.  Delete Exercise by Category
7.  Create Workout Routine 
8.  View Workout Routine
9.  View Exercise Progress
10. Update Workout Routine
11. Delete Workout Routine 
12. Set Fitness Goal
13. Insert Progress towards Fitness Goal    
14. View Fitness Goal
15. Update Fitness Goal 
16. Delete Fitness Goal
17. Quit
''')    


    if option == '1':

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

        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        # Fetches the result
        results = cur.fetchone()
        if results[0] > 0:
            print('You have the following exercise categories:')
            ExerciseCategory.view_all_categories()  
        else:
            print('You have no exercise categories')

    elif option == '3':

        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            print('You have the following exercise categories:')
            ExerciseCategory.view_all_categories()
            while True:
                delete_category = input('Which exercise category would you like to delete: ')
                cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                            (delete_category,))
                category_result = cur.fetchone()
                if category_result[0] > 0:
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
                    break
                else:
                    print('Exercise category does not exist')
        else:
            print('You have no exercise categories')

    elif option == '4':

        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            while True:
                which_category = input('Which exercise will this category belong to: ')
                cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                            (which_category,))
                category_result = cur.fetchone()
                if category_result[0] > 0:  # Checks to see if exercise category exists
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
                                print('Exercise successfully saved')
                                break
                        except IntegrityError:  # Prevents identical exercises from being saved to database
                            print('Exercise already exists')
                    break
                else:
                    print('Exercise category does not exist')
        else:
            print('You have no exercise categories!') 
            print('You need to create exercise categories before adding exercises')

    elif option == '5':    

        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            # Counts all the exercises from exercises table
            cur.execute('''SELECT COUNT(*) FROM exercises''')
            # Fetches the results
            exercises_results = cur.fetchone()
            if exercises_results[0] > 0:
                while True:
                    which_input = input('Which exercise category would you like to display?: ')
                    cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                                (which_input,))
                    category_result = cur.fetchone()
                    if category_result[0] > 0:
                        # Retrieves the exercise category's id
                        cat_id = ExerciseCategory.retrieve_category_id(which_input)
                        cur.execute('''SELECT COUNT(*) FROM exercises WHERE exercise_category_id=?''',
                                    (cat_id,))
                        id_result = cur.fetchone()
                        if id_result[0] > 0:
                            cur.execute('''SELECT exercise_name FROM exercises WHERE exercise_category_id=?''',
                                        (cat_id,))
                            print(f'You have the following exercises in the {which_input} category:')
                            for row in cur:
                                print(row[0])
                            break
                        else:
                            print('Exercise category does not have any exercises')
                    else:
                        print('Exercise category does not exist')
            else:
                print('You have not created any exercises')
        else:
            print('You have not created any exercise categories')

    elif option == '6':     # Add more while loops so that the program doesn't restart the while loop after each invalid input

        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            # Counts all the exercises from exercises table
            cur.execute('''SELECT COUNT(*) FROM exercises''')
            exercises_results = cur.fetchone()
            if exercises_results[0] > 0:
                while True:
                    exercise_category = input('Which exercise category would you want to delete from?: ')
                    # Checks to see if exercise category exists in table
                    cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                                (exercise_category,))
                    # Fetches the result
                    category_result = cur.fetchone()
                    if category_result[0] > 0:
                        # Retrieves the exercise category's id
                        exercise_category_id = ExerciseCategory.retrieve_category_id(exercise_category)
                        # Counts all exercises from table with matching category id's
                        cur.execute('''SELECT COUNT(*) FROM exercises WHERE exercise_category_id=?''',
                                    (exercise_category_id,))
                        # Fetches the result
                        category_results_count = cur.fetchone()
                        if category_results_count[0] > 0:
                            while True:
                                exercise = input('Which exercise would you like to delete: ')
                                # Checks to see if exercise exists in table
                                cur.execute('''SELECT COUNT(*) FROM exercises WHERE exercise_name=?''',
                                            (exercise,))
                                # Fetches result
                                exercise_result = cur.fetchone()
                                if exercise_result[0] > 0:
                                    # Deletes exercise if does exist
                                    Exercise.delete(exercise)
                                    print(f'{exercise} was deleted from database')
                                    break
                                else:
                                    print(f'The exercise {exercise} does not exist in the {exercise_category} category')
                            break
                        else:
                            print(f'There are no exercises in the {exercise_category} category')
                    else:
                        print('Exercise category does not exist')
            else:
                print('You have not created any exercises')
        else:
            print('You have not created any exercise categories')

    elif option == '7':     # THINK ABOUT DELETING THE count VARIABLE, AND INSTEAD USE THE enumerate FUNCTION TO GET THE TOTAL NUMBER OF EXERCISES IN THE WORKOUT ROUTINE. THIS MAY REDUCE THE AMOUNT OF CODE YOU WRITE

        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            # Counts all the exercises from exercises table
            cur.execute('''SELECT COUNT(*) FROM exercises''')
            exercises_results = cur.fetchone()
            if exercises_results[0] > 0:
                while True:

                    workout_routine_category = input('Which category will this workout routine belong to: ')
                    # Checks to see if workout routine exists
                    cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                                (workout_routine_category,))
                    category_results = cur.fetchone()
                    if category_results[0] > 0:
                        category_id = ExerciseCategory.retrieve_category_id(workout_routine_category)
                        # Checks to see if there are exercises in exercise category
                        cur.execute('''SELECT COUNT(*) FROM exercises WHERE exercise_category_id=?''',
                                    (category_id,))
                        # Fetches the result
                        is_exercises = cur.fetchone()
                        if is_exercises[0] > 0:
                            while True:

                                routine_name = input('''Give this workout routine a name: ''')
                                if routine_name.strip() != '' or routine_name.isalpha():
                                    cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE workout_routine_name=?
                                                AND exercise_category_id=?''', (routine_name, category_id))
                                    routine_result = cur.fetchone()
                                    if routine_result[0] == 0:
                                        while True:

                                            add = input('''
1.  Enter new exercise into workout routine
2.  Quit, once you\'ve added at least one exercise to workout routine
''')
                                    
                                            if add == '1':
                                                while True:
                                                    exercise = input('Which exercise would you like to add to this workout routine: ')
                                                    cur.execute('''SELECT COUNT(*) FROM exercises WHERE exercise_name=?
                                                                AND exercise_category_id=?''',
                                                                (exercise, category_id))
                                                    exercise_exists = cur.fetchone()
                                                    if exercise_exists[0] > 0:
                                                        if exercise not in exercises_in_routine:
                                                            WorkoutRoutine.insert_workout_routine(routine_name, exercise, category_id)
                                                            CreateWorkout.choose_own_param(exercise)
                                                            exercises_in_routine.append(exercise)
                                                            break
                                                        else:
                                                            print('Exercise already exists in workout routine')
                                                            break
                                                    else:
                                                        print(f'Exercise doesn\'t exist in {workout_routine_category} category')
                                                
                                            elif add == '2':
                                                cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE workout_routine_name=?
                                                            AND exercise_category_id=?''', (routine_name, category_id))
                                                exists = cur.fetchone()
                                                if exists[0] > 0:
                                                    break
                                                else:
                                                    print('You have to select at least one exercise for your workout routine')
                                            else:
                                                print('Invalid option')
                                        break
                                    else:
                                        print(f'Workout routine name already exists in the {workout_routine_category} category. Choose another name')
                                else:
                                    print('Invalid input')
                            break
                        else:
                            print('Exercise category does not contain any exercise. Add exercises before creating a workout routine.')
                    else:
                        print('Exercise category does not exist')
            else:
                print('You have not created any exercises')
        else:
            print('You have not created any exercise categories')

    elif option == '8': 

        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            # Counts all the exercises from exercises table
            cur.execute('''SELECT COUNT(*) FROM exercises''')
            exercises_results = cur.fetchone()
            if exercises_results[0] > 0:
                # Counts all the workout routines from the workout routine's table
                cur.execute('''SELECT COUNT(*) FROM workout_routine''')
                # Fetches the result
                all_routines = cur.fetchone()
                if all_routines[0] > 0:
                    while True:

                        category = input('Which exercise category does the workout routine belong to: ')
                        # Checks to see if the exercise category exists
                        cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                                    (category,))
                        category_result = cur.fetchone()
                        if category_result[0] > 0:
                            exercise_category_id_result = ExerciseCategory.retrieve_category_id(category)
                            print(exercise_category_id_result)
                            # Checks to see if the exercise category has workout routines 
                            cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE exercise_category_id=?''',
                                        (exercise_category_id_result,))
                            has_routines = cur.fetchone()
                            if has_routines[0] > 0:
                            
                                while True:

                                    print(f'You have the following workout routines in the {category} category: ')
                                    cur.execute('''SELECT workout_routine_name FROM workout_routine
                                                WHERE exercise_category_id=?''', (exercise_category_id_result,))
                                    for row in cur:
                                        print(row[0])
                                    view_workout_routine = input('Which workout routine do you wish to view: ')
                                    cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE workout_routine_name=?
                                                AND exercise_category_id=?''', (view_workout_routine, exercise_category_id_result))
                                    workout_routine_result = cur.fetchone()
                                    if workout_routine_result[0] > 0:
                                        WorkoutRoutine.view(view_workout_routine)
                                        break
                                    else:
                                        print('Invalid. Workout routine does not exist')
                                break
                            else:
                                print(f'{category} category has no workout routines')
                        else:
                            print('Exercise category does not exist')
                else:
                    print('You have not created a workout routine yet')
            else:
                print('You have not created any exercises')
        else:
            print('You have not created any exercise categories')

    elif option == '9':

         # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            # Counts all the exercises from exercises table
            cur.execute('''SELECT COUNT(*) FROM exercises''')
            exercises_results = cur.fetchone()
            if exercises_results[0] > 0:
                # Counts all the workout routines from the workout routine's table
                cur.execute('''SELECT COUNT(*) FROM workout_routine''')
                all_routines = cur.fetchone()
                if all_routines[0] > 0:
                    while True:
                        category = input('Which exercise category does the workout routine belong to: ')
                        # Checks to see if the exercise category exists
                        cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                                    (category,))
                        category_result = cur.fetchone()
                        if category_result[0] > 0:
                            exercise_category_id_result = ExerciseCategory.retrieve_category_id(category)
                            print(exercise_category_id_result)
                            # Checks to see if the exercise category has workout routines 
                            cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE exercise_category_id=?''',
                                        (exercise_category_id_result,))
                            has_routines = cur.fetchone()
                            if has_routines[0] > 0:
                                while True:

                                    print(f'You have the following workout routines in the {category} exercise category: ')
                                    # Prints out all the workout routines that the user has in exercise category
                                    cur.execute('''SELECT workout_routine_name FROM workout_routine
                                                WHERE exercise_category_id=?''', (exercise_category_id_result,))
                                    for row in cur:
                                        print(row[0])
                                    routine = input('Which routine are you currently busy with: ')
                                    # Checks to see if workout routine exists in the specified exercise category
                                    cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE workout_routine_name=?
                                                AND exercise_category_id=?''', (routine, exercise_category_id_result))
                                    routine_result = cur.fetchone()
                                    if routine_result[0] > 0:
                                        while True:

                                            print(f'You have the following exercises in the {routine} workout routine:')
                                            cur.execute('''SELECT workout_routine_exercise FROM workout_routine
                                                        WHERE workout_routine_name=? AND exercise_category_id=?''',
                                                        (routine, exercise_category_id_result))
                                            for index, exercises in enumerate(cur, start=1):
                                                print(index, exercises[0])

                                            completed = input(f'''
1.  Enter 1 to add exercise you\'ve completed from {routine} workout routine
2.  Enter 2 once you\'ve added all completed exercises from {routine} workout routine
''')
                                            if completed == '1':    # Make sure user can't add duplicate exercises!!!       ALSO ANOTHER IDEA COULD BE TO USE NUMBERS AS INDEXES FOR EXERCISE SO THAT USERS DON'T HAVE TO TYPE IN THE EXERCISE IN FULL ONCE THEY'VE COMPLETED IT, THEY ONLY NEED TO TYPE IN THE NUMBER ASSOCIATED WITH THE EXERCISE
                                                while True:
                                                    completed_exercise = input('Which exercise have you completed: ')
                                                    cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE
                                                                workout_routine_name=? AND workout_routine_exercise=?
                                                                AND exercise_category_id=?''', (routine, completed_exercise, exercise_category_id_result))
                                                    exercise_result = cur.fetchone()
                                                    if exercise_result[0] > 0:
                                                        if not completed_exercise in exercises_in_routine:
                                                            exercises_in_routine.append(completed_exercise)
                                                            print(f'{completed_exercise} marked off as complete')
                                                            # Increment count variable by one
                                                            exercise_count += 1
                                                            break
                                                        else:
                                                            print('Exercise already marked off as complete')
                                                            break
                                                    else:
                                                        print('Exercise does not exist')
                                            elif completed == '2':
                                                cur.execute('''SELECT workout_routine_exercise, workout_description
                                                            FROM workout_routine WHERE workout_routine_name=?
                                                            AND exercise_category_id=?''', (routine, exercise_category_id_result))
                                                for exercise in cur:
                                                    if not exercise[0] in exercises_in_routine:
                                                        print(exercise[0], '-', exercise[1])
                                                exercises_in_routine.clear()
                                                exercise_count = 0
                                                break
                                            if exercise_count == index:
                                                print('You have completed your workout. Well done')
                                                exercise_count = 0
                                                break
                                        break
                                    else:
                                        print('Workout routine does not exist')
                                break
                            else:
                                print(f'{category} category has no workout routines')
                        else:
                            print('Exercise category does not exist')
                else:
                    print('You have not created a workout routine yet')
            else:
                print('You have not created any exercises')
        else:
            print('You have not created any exercise categories')

    elif option == '10':
        
        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            # Counts all the exercises from exercises table
            cur.execute('''SELECT COUNT(*) FROM exercises''')
            exercises_results = cur.fetchone()
            if exercises_results[0] > 0:
                # Counts all the workout routines from the workout routine's table
                cur.execute('''SELECT COUNT(*) FROM workout_routine''')
                all_routines = cur.fetchone()
                if all_routines[0] > 0:
                    while True:
                        category = input('Which exercise category does the workout routine belong to: ')
                        # Checks to see if the exercise category exists
                        cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                                    (category,))
                        category_result = cur.fetchone()
                        if category_result[0] > 0:
                            exercise_category_id_result = ExerciseCategory.retrieve_category_id(category)
                            print(exercise_category_id_result)
                            # Checks to see if the exercise category has workout routines 
                            cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE exercise_category_id=?''',
                                        (exercise_category_id_result,))
                            has_routines = cur.fetchone()
                            if has_routines[0] > 0:
                                while True:

                                    print(f'You have the following workout routines in the {category} exercise category: ')
                                    # Prints out all the workout routines that the user has in exercise category
                                    cur.execute('''SELECT workout_routine_name FROM workout_routine
                                                WHERE exercise_category_id=?''', (exercise_category_id_result,))
                                    for row in cur:
                                        print(row[0])
                                    routine_name = input('Which routine do you want to update: ')
                                    # Checks to see if workout routine exists in the specified exercise category
                                    cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE workout_routine_name=?
                                                AND exercise_category_id=?''', (routine_name, exercise_category_id_result))
                                    routine_result = cur.fetchone()
                                    if routine_result[0] > 0:
                                        change_routine = True
                                        while change_routine:


                                            change = input('''
Enter 1 if you wish to add an exercise to an existing workout routine
Enter 2 if you wish to change an exercise's description 
Enter 3 if you wish to delete an exercise from an existing workout routine
''')
                                            if change == '1':
                                                # Counting all the exercise in exercise category id
                                                cur.execute('''SELECT COUNT(*) FROM exercises WHERE
                                                            exercise_category_id=?''', 
                                                            (exercise_category_id_result,))
                                                all_exercises = cur.fetchone()
                                                # Counting all the exercises user has in workout routine
                                                cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE
                                                            workout_routine_name=?''', (routine_name,))
                                                routine_exercises = cur.fetchone()
                                                # Proceeds if user has exercise remaining to add to workout routine
                                                if all_exercises[0] != routine_exercises[0]:
                                                    while True:

                                                        exercise = input('Which exercise would you like to add to this workout routine: ')
                                                        cur.execute('''SELECT COUNT(*) FROM exercises WHERE exercise_name=?
                                                                    AND exercise_category_id=?''',
                                                                    (exercise, exercise_category_id_result))
                                                        exercise_exists = cur.fetchone()
                                                        if exercise_exists[0] > 0:
                                                            cur.execute('''SELECT COUNT(*) FROM workout_routine 
                                                                        WHERE workout_routine_name=? AND workout_routine_exercise=?''',
                                                                        (routine_name, exercise))
                                                            new_exercise = cur.fetchone()
                                                            if new_exercise[0] == 0:
                                                                WorkoutRoutine.insert_workout_routine(routine_name, exercise, exercise_category_id_result)
                                                                CreateWorkout.choose_own_param(exercise)
                                                                # Breaks out of outer loop
                                                                change_routine = False
                                                                break
                                                            else:
                                                                print(f'{exercise} already exist in the {routine_name} workout routine')
                                                        else:
                                                            print(f'Exercise doesn\'t exist in the {category} category') 
                                                else:
                                                    print(f'You have no exercises left to add to {routine_name} workout routine')
                                                    break
                                            elif change == '2':
                                                while True:
                                                
                                                    exercise = input('Which exercise would you like to update in this workout routine: ')
                                                    cur.execute('''SELECT COUNT(*) FROM workout_routine 
                                                                    WHERE workout_routine_name=? AND workout_routine_exercise=?''',
                                                                    (routine_name, exercise))
                                                    exercise_exists = cur.fetchone()
                                                    if exercise_exists[0] > 0:
                                                        CreateWorkout.choose_own_param(exercise)
                                                        # Breaks out of outer loop
                                                        change_routine = False
                                                        break
                                                    else:
                                                        print(f'Exercise doesn\'t exist in the {routine_name} workout routine')
                                            elif change == '3':
                                                while True:
                                                
                                                    exercise = input('Which exercise would you like to delete from this workout routine: ')
                                                    cur.execute('''SELECT COUNT(*) FROM workout_routine 
                                                                    WHERE workout_routine_name=? AND workout_routine_exercise=?''',
                                                                    (routine_name, exercise))
                                                    exercise_exists = cur.fetchone()
                                                    if exercise_exists[0] > 0:
                                                        WorkoutRoutine.delete_routine_exercise(routine_name, exercise)
                                                        # Breaks out of outer loop
                                                        change_routine = False
                                                        break
                                                    else:
                                                        print(f'Exercise doesn\'t exist in the {routine_name} workout routine')
                                            else:
                                                print('Invalid input')
                                        break
                                    else:
                                        print('Workout routine does not exist')
                                break    
                            else:
                                print(f'{category} category has no workout routines')
                        else:
                            print('Exercise category does not exist')
                else:
                    print('You have not created a workout routine yet')
            else:
                print('You have not created any exercises')
        else:
            print('You have not created any exercise categories')

    elif option == '11':

        # Counts all the exercise categories from exercise_category table
        cur.execute('''SELECT COUNT(*) FROM exercise_category''')
        results = cur.fetchone()
        if results[0] > 0:
            # Counts all the exercises from exercises table
            cur.execute('''SELECT COUNT(*) FROM exercises''')
            exercises_results = cur.fetchone()
            if exercises_results[0] > 0:
                # Counts all the workout routines from the workout routine's table
                cur.execute('''SELECT COUNT(*) FROM workout_routine''')
                all_routines = cur.fetchone()
                if all_routines[0] > 0:
                    while True:
                        category = input('Which exercise category does the workout routine belong to: ')
                        # Checks to see if the exercise category exists
                        cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                                    (category,))
                        category_result = cur.fetchone()
                        if category_result[0] > 0:
                            exercise_category_id_result = ExerciseCategory.retrieve_category_id(category)
                            print(exercise_category_id_result)
                            # Checks to see if the exercise category has workout routines 
                            cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE exercise_category_id=?''',
                                        (exercise_category_id_result,))
                            has_routines = cur.fetchone()
                            if has_routines[0] > 0:
                                while True:

                                    print(f'You have the following workout routines in the {category} exercise category: ')
                                    # Prints out all the workout routines that the user has in exercise category
                                    cur.execute('''SELECT workout_routine_name FROM workout_routine
                                                WHERE exercise_category_id=?''', (exercise_category_id_result,))
                                    for row in cur:
                                        print(row[0])
                                    routine = input('Which routine do you wish to remove: ')
                                    # Checks to see if workout routine exists in the specified exercise category
                                    cur.execute('''SELECT COUNT(*) FROM workout_routine WHERE workout_routine_name=?
                                                AND exercise_category_id=?''', (routine, exercise_category_id_result))
                                    routine_result = cur.fetchone()
                                    if routine_result[0] > 0:
                                        WorkoutRoutine.delete_workout_routine(routine, exercise_category_id_result)
                                        print(f'{routine} routine successfully deleted')
                                        break
                                    else:
                                        print('Workout routine does not exist')
                                break
                            else:
                                print(f'{category} category has no workout routines')
                        else:
                            print('Exercise category does not exist')
                else:
                    print('You have not created a workout routine yet')
            else:
                print('You have not created any exercises')
        else:
            print('You have not created any exercise categories')

    elif option == '12':   

        fitness_goal = True
        while fitness_goal:

            health_goal = input('''
Enter 1 if you want to set a health goal
Enter 2 if you want to set a fitness goal
''')
            if health_goal == '1':
                while True:

                    health_fitness_goal = input('Enter your desired health goal: ')
                    # Checks to see if input is not empty whitespace
                    if health_fitness_goal.strip() != '':
                        while True:

                            health_goal_date = input('Enter the date you would like to achieve this health goal: ')
                            # Checks to see if input is not empty whitespace
                            if health_goal_date.strip() != '':
                                # Adds health goal to the database
                                FitnessGoalHealth.insert_into_goal(health_fitness_goal, health_goal_date)
                                fitness_goal = False
                                break
                            else:
                                print('Invalid input')
                        break
                    else:
                        print('Invalid input')
            elif health_goal == '2':
                # Counts all the exercise categories from exercise_category table
                cur.execute('''SELECT COUNT(*) FROM exercise_category''')
                results = cur.fetchone()
                if results[0] > 0:
                    # Counts all the exercises from exercises table
                    cur.execute('''SELECT COUNT(*) FROM exercises''')
                    exercises_results = cur.fetchone()
                    if exercises_results[0] > 0:
                        while True:

                            exercise_category = input('Which category will this fitness goal belong to: ')
                            # Checks to see if workout routine exists
                            cur.execute('''SELECT COUNT(*) FROM exercise_category WHERE exercise_category_name=?''',
                                        (exercise_category,))
                            # Fetches the result
                            category_results = cur.fetchone()
                            if category_results[0] > 0:
                                category_id = ExerciseCategory.retrieve_category_id(exercise_category)
                                # Checks to see if there are exercises in exercise category
                                cur.execute('''SELECT COUNT(*) FROM exercises WHERE exercise_category_id=?''',
                                            (category_id,))
                                # Fetches the result
                                is_exercises = cur.fetchone()
                                if is_exercises[0] > 0:
                                    while True:
                                        exercise_goal = input(f'Which exercise in the {exercise_category} would you like to create a fitness goal for: ')
                                        # Checks to see if exercise exists
                                        cur.execute('''SELECT COUNT(*) FROM exercises WHERE exercise_name=?
                                                    AND exercise_category_id=?''', (exercise_goal, category_id))
                                        exercise_exists = cur.fetchone()
                                        if exercise_exists[0] > 0:
                                            while True:

                                                fitness_goal_input = input(f'What fitness goal would you like to set for {exercise_goal}: ')
                                                if fitness_goal_input.strip() != '':
                                                    while True:

                                                        fitness_goal_date = input('When would you like to achieve this fitness goal: ')
                                                        if fitness_goal_date.strip() != '':
                                                            # Adds fitness goal to database
                                                            FitnessGoal.insert_into_goal(exercise_goal, fitness_goal_input, fitness_goal_date, category_id)
                                                            print('Fitness goal successfully updated')
                                                            # Breaks out of loops
                                                            fitness_goal = False
                                                            break
                                                        else:
                                                            print('Invalid input')
                                                    break
                                                else:
                                                    print('Invalid input')
                                            break
                                        else:
                                            print(f'Exercise does not exist in the {exercise_category} category')
                                    break
                                else:
                                    print('Exercise category does not contain any exercise. Add exercises before creating a workout routine.')
                            else:
                                print('Exercise category does not exist')
                    else:
                        print('You have not created any exercises')
                else:
                    print('You have not created any exercise categories')
            else:
                print('Invalid input')
            
    elif option == '13': 

        fitness_goal = True
        while fitness_goal:

            health_goal_progress = input('''
Enter 1 if you would like to add progress towards a health goal
Enter 2 if you would like to add progress towards a fitness goal
''')
            if health_goal_progress == '1':

                while True:

                    FitnessGoalHealth.print_out_selection()
                    # Used to catch incorrect input types from user
                    try:
                        select_health_goal = int(input('Enter the id of the health goal you would like to add progress for: '))
                        # Checks to see if exercise exists
                        cur.execute('''SELECT COUNT(*) FROM fitness_goal_health WHERE fitness_goal_id=?''',
                                    (select_health_goal,))
                        fitness_goal_exist = cur.fetchone()
                        if fitness_goal_exist[0] > 0:
                            while True:

                                health_goal_progress = input('Enter your progress for your health goal: ')
                                if health_goal_progress.strip() != '':
                                    while True:

                                        health_goal_progress_date = input('Enter the current date to track your progress: ')          
                                        if health_goal_progress_date.strip() != '':
                                            # Adds user's progress to the fitness goal
                                            FitnessGoalHealth.insert_into_goal_progress(health_goal_progress, health_goal_progress_date, select_health_goal)
                                            fitness_goal = False
                                            break
                                        else:
                                            print('Invalid input')
                                    break
                                else:
                                    print('Invalid input')
                            break
                        else:
                            print('Does not exist')
                    except ValueError:
                        print('Invalid input')
                
            elif health_goal_progress == '2':
                # Checks to see if the user has any fitness goals in database
                cur.execute('''SELECT COUNT(*) FROM fitness_goal''')
                has_fitness_goal = cur.fetchone()
                if has_fitness_goal[0] > 0:
                    while True:

                        FitnessGoal.print_out_selection()
                        try:
                            select_fitness_goal = int(input('Enter the number of the fitness goal you want to add progress for: '))
                            # Checks to see if exercise exists
                            cur.execute('''SELECT COUNT(*) FROM fitness_goal WHERE fitness_goal_id=?''',
                                        (select_fitness_goal,))
                            exercise_exists = cur.fetchone()
                            if exercise_exists[0] > 0:
                                while True:

                                    # Retrieving the exercise category id of the exercise
                                    cur.execute('''SELECT fitness_goal_exercise_category FROM fitness_goal
                                                WHERE fitness_goal_id=?''', (select_fitness_goal,))
                                    exercise_category_id = cur.fetchone()
                                    # Fetching the exercise associated with the fitness id
                                    cur.execute('''SELECT fitness_goal_exercise FROM fitness_goal WHERE
                                                fitness_goal_id=?''', (select_fitness_goal,))
                                    exercise = cur.fetchone()

                                    fitness_goal_progress = input(f'Enter the fitness progress you have for {exercise[0]}: ')
                                    if fitness_goal_progress.strip() != '':
                                        while True:

                                            fitness_progress_date = input('Enter the current date to track progress: ')
                                            if fitness_progress_date.strip() != '':
                                                # Adds user's progress towards the fitness goal
                                                FitnessGoal.insert_into_goal_progress(fitness_goal_progress, fitness_progress_date, exercise_category_id[0])
                                                fitness_goal = False
                                                break
                                            else:
                                                print('Invalid input')
                                        break
                                    else:
                                        print('Invalid input')
                                break
                            else:
                                print('Number is not associated with a fitness goal')
                        except ValueError:
                            print('Invalid input')
                    break
                else:
                    print('You have not created any fitness goals')
            else:
                print('Invalid input')

    elif option == '14': 

        while True:

            goal = input('''
Enter 1 if you wish to view a health goal
Enter 2 if you wish to view a fitness goal
''')
            if goal == '1':
                # Checks to see if user has set a health goal
                cur.execute('''SELECT COUNT(*) FROM fitness_goal_health''')
                health_goal_count = cur.fetchone()
                if health_goal_count[0] > 0:
                    # Prints out user's health goals
                    FitnessGoalHealth.print_out_selection()
                else:
                    print('You have not set any health goals')
                break
            elif goal == '2':
                # Checks to see if user has set a fitness goal
                cur.execute('''SELECT COUNT(*) FROM fitness_goal''')
                fitness_goal_count = cur.fetchone()
                if fitness_goal_count[0] > 0:
                    # Prints out user's health goals
                    FitnessGoal.print_out_selection()
                else:
                    print('You have not set any fitness goals')
                break
            else:
                print('Invalid input')

    elif option == '15':    

        # Over here you really can create a function with parameters. The parameter should include whether the goal is a fitness one or a health one. You really can make these two parts into one. Do the thing you see on AlgoExpert, first call the function before creating it. Define it after you call it.

        goal_update = True
        while goal_update:

            goal = input('''
Enter 1 if you wish to update a health goal
Enter 2 if you wish to update a fitness goal
''')
            if goal == '1':
                cur.execute('''SELECT COUNT(*) FROM fitness_goal_health''')
                is_goal = cur.fetchone()
                if is_goal[0] > 0:
                    # Prints out user's health goals
                    FitnessGoalHealth.print_out_selection()
                    num = True
                    while num:
                        try:
                            option = int(input('Enter the ID of the health goal you want to update: '))
                            # Checks to see if health goal exists
                            cur.execute('''SELECT COUNT(*) FROM fitness_goal_health
                                        WHERE fitness_goal_id=?''', (option,))
                            goal_exists = cur.fetchone()
                            if goal_exists[0] > 0:
                                update_option = True
                                while update_option:

                                    update = input('''
Enter 1 if you wish to update the health goal
Enter 2 if you wish to update the achieve date
''')
                                    if update == '1':
                                        while True:
                                            new_health_goal = input('Enter the updated health goal you want to set: ')
                                            if new_health_goal.strip() != '':

                                                '''Checks to see if user has entered progress for their fitness goal, 
                                                if yes allows user the option to overwrite their progress'''

                                                cur.execute('''SELECT fitness_goal_progress FROM fitness_goal_health
                                                            WHERE fitness_goal_id=?''', (option,))
                                                overwrite_option = cur.fetchone()
                                                if str(overwrite_option[0]) != 'None':
                                                    while True:
                                                        # Allows the user to overwrite the progress they have for the fitness goal
                                                        overwrite_progress = input('''
Enter 1 if you wish to overwrite your progress for this fitness goal
Enter 2 if you do not wish to overwrite your progress for this fitness goal
''')
                                                        if overwrite_progress == '1':
                                                            # Updates users health goal and overwrites progress that user has set
                                                            FitnessGoalHealth.update_and_overwrite(new_health_goal, option)
                                                            print('Health goal successfully updated')
                                                            break
                                                        elif overwrite_progress == '2':
                                                            # Updates user's health goal
                                                            FitnessGoalHealth.update_health_goal(new_health_goal, option)
                                                            print('Health goal successfully updated')
                                                            break
                                                        else:
                                                            print('Invalid option')
                                                else:
                                                    # Updates user's health goal
                                                    FitnessGoalHealth.update_health_goal(new_health_goal, option)
                                                    print('Health goal successfully updated')
                                                # Breaks out of all outer loops
                                                goal_update = False
                                                num = False
                                                update_option = False
                                                break  
                                            else:
                                                print('Invalid')
                                    elif update == '2':

                                        while True:

                                            new_achieve_date = input('Please enter the health goal\'s new desired date: ')
                                            if new_achieve_date != '':
                                                # Updates the health goal with the new date
                                                FitnessGoalHealth.update_target_date(new_achieve_date, option)
                                                print('Health goal successfully updated')
                                                goal_update = False
                                                num = False
                                                update_option = False
                                                break
                                            else:
                                                print('Invalid input')
                                    else:
                                        print('Invalid input')
                            else:
                                print('Invalid. Input is not associated with a goal')
                        except ValueError:
                            print('Invalid input')
                else:
                    print('You have not set a health goal yet')
                    goal_update = False
            elif goal == '2':
                # Checks to see if user has created fitness goals
                cur.execute('''SELECT COUNT(*) FROM fitness_goal''')
                goal_count = cur.fetchone()
                if goal_count[0] > 0:
                    num = True
                    while num:
                        # Prints out the users fitness goals for user to choose
                        FitnessGoal.print_out_selection()
                        try:
                            option = int(input('Enter the number of the fitness goal you would like to update: '))
                            # Checks to see if fitness goal exists
                            cur.execute('''SELECT COUNT(*) FROM fitness_goal
                                        WHERE fitness_goal_id=?''', (option,))
                            goal_exists = cur.fetchone()
                            if goal_exists[0] > 0:
                                update_option = True
                                while update_option:

                                    update = input('''
Enter 1 if you wish to update the fitness goal
Enter 2 if you wish to update the achieve date
''')


                                    if update == '1':
                                        while True:
                                            new_fitness_goal = input('Enter the updated fitness goal you want to set: ')
                                            if new_fitness_goal.strip() != '':

                                                '''Checks to see if user has entered progress for their fitness goal, 
                                                if yes allows user the option to overwrite their progress'''

                                                cur.execute('''SELECT fitness_goal_progress FROM fitness_goal
                                                            WHERE fitness_goal_id=?''', (option,))
                                                overwrite_option = cur.fetchone()
                                                if str(overwrite_option[0]) != 'None':
                                                    while True:
                                                        # Allows the user to overwrite the progress they have for the fitness goal
                                                        overwrite_progress = input('''
Enter 1 if you wish to overwrite your progress for this fitness goal
Enter 2 if you do not wish to overwrite your progress for this fitness goal
''')
                                                        if overwrite_progress == '1':
                                                            # Updates and overwrites user's fitness 
                                                            FitnessGoal.update_and_overwrite(new_fitness_goal, option)
                                                            print('Fitness goal successfully updated')
                                                            break
                                                        elif overwrite_progress == '2':
                                                            # Updates the user's fitness goal
                                                            FitnessGoal.update_goal(new_fitness_goal, option)
                                                            print('Fitness goal successfully updated')
                                                        else:
                                                            print('Invalid option')
                                                else:
                                                    # Updates the user's fitness goal
                                                    FitnessGoal.update_goal(new_fitness_goal, option)
                                                    print('Fitness goal successfully updated')
                                                # Breaks out of all outer loops
                                                goal_update = False
                                                num = False
                                                update_option = False
                                                break  
                                            else:
                                                print('Invalid')
                                    elif update == '2':

                                        while True:

                                            new_achieve_date = input('Please enter the revised target date for this goal: ')
                                            if new_achieve_date != '':
                                                # Updated the user's fitness goal
                                                FitnessGoalHealth.update_target_date(new_achieve_date, option)
                                                print('Fitness goal successfully updated')

                                                goal_update = False
                                                num = False
                                                update_option = False
                                                break
                                            else:
                                                print('Invalid input')
                                    else:
                                        print('Invalid input')

                            else:
                                print('ID is not associated with a fitness goal')
                        except ValueError:
                            print('Invalid input')

                else:
                    print('You have not created a fitness goal yet')
                    # Breaks out of main loop
                    goal_update = False
            else:
                print('Invalid input')         

    elif option == '16': 

        delete = True
        while delete:
            fitness_goal = input('''
Enter 1 if you would like to delete a health goal
Enter 2 if you would like to delete a fitness goal
''')

            if fitness_goal == '1':
                
                # Checks to see if user has created a health goal yet
                cur.execute('''SELECT COUNT(*) FROM fitness_goal_health''')
                fitness_goal_health_count = cur.fetchone()
                if fitness_goal_health_count[0] > 0:
                    while True:
                        # Prints out the user's fitness goal for user to choose
                        FitnessGoalHealth.print_out_selection()
                        try:
                            option = int(input('Enter the ID of the health goal you want to delete: '))
                            # Checks to see if health goal exists
                            cur.execute('''SELECT COUNT(*) FROM fitness_goal_health
                                        WHERE fitness_goal_id=?''', (option,))
                            goal_exists = cur.fetchone()
                            if goal_exists[0] > 0:
                                # Deletes the health goal
                                FitnessGoalHealth.delete_goal(option)
                                delete = False
                                break
                            else:
                                print('Error, ID does not exist')
                        except ValueError:
                            print('Invalid input')
                else:
                    print('You have not made a health goal yet.')

            elif fitness_goal == '2':
                # Checks to see if user has created a fitness goal
                cur.execute('''SELECT COUNT(*) FROM fitness_goal''')
                fitness_goal_count = cur.fetchone()
                if fitness_goal_count[0] > 0:
                    # Prints out 
                    FitnessGoal.print_out_selection()
                    while True:
                        try:
                            option = int(input('Enter the number of the fitness goal you want to delete: '))
                            # Checks to see if fitness goal exists
                            cur.execute('''SELECT COUNT(*) FROM fitness_goal
                                        WHERE fitness_goal_id=?''', (option,))
                            goal_exists = cur.fetchone()
                            if goal_exists[0] > 0:
                                # Deletes the fitness goal
                                FitnessGoal.delete(option)
                                delete = False
                                break
                            else:
                                print('Invalid input. ID is not associated with a fitness goal')
                        except ValueError:
                            print('Invalid input')
                else:
                    print('You have not made a fitness goal yet.')
            else:
                print('Invalid input. Enter a valid option')

    elif option == '17':

        print('Bye')
        break
    
    else:
        print('Invalid.')
