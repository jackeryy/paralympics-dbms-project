import psycopg2 as db_connect

#Establish Connection to server
def connect(host_name, db_user, db_password, db_name):

    try:
        connection = db_connect.connect(
            host=host_name, 
            user=db_user, 
            password=db_password, 
            dbname=db_name
        )
        return connection
    
    except Exception as e:
        print("An error occurred while connecting to the database:", e)
        return None

#Query functions for manage athletes menu
def add_athlete(connection):
    try:
        with connection.cursor() as cursor:
            #get user input for athlete's information
            name = input("Enter the athlete's name: ")
            country = input("Enter the athlete's country: ")
            country_code = input("Enter the athlete's country code: ")
            sport = input("Enter the athlete's sport: ")
            sport_code = input("Enter the athlete's sport code: ")
            dob = input("Enter the athlete's date of birth (MM-DD-YYYY): ")
            gender = input("Enter the athlete's gender: ")


            print(name, country, country_code, sport, sport_code, dob, gender)

            #check for existing country code and sport exist in the database
            cursor.execute('''SELECT 1 FROM NPCs WHERE CountryCode = %s AND Country = %s''', (country_code, country))
            if not cursor.fetchone():
                print ("No entry found in the NPCs table with matching country and country code.")
                return

            cursor.execute('''SELECT 1 FROM Discipline WHERE Sport = %s''', (sport,))
            if not cursor.fetchone():
                print ("No entry found in the Discipline table with matching sport.")
                return

            #write and execute query
            query = """INSERT INTO Athletes (NameAthlete, Country, CountryCode, Sport, SportCode, DateOfBirth, Gender)
                    VALUES  (%s, %s, %s, %s, %s, %s, %s)"""

            cursor.execute(query, (name, country, country_code, sport, sport_code, dob, gender))
            connection.commit()
            print(f'\nAthlete added ---- \n{name}({gender}) from {country} ({country_code}), partcipates in {sport} ({sport_code}), born on {dob}')

    except Exception as e:
        print("Failed to add athlete: ", e)
        connection.rollback()

def update_athlete_details(connection):
    try:
        with connection.cursor() as cursor:
            # Get identifying information
            name_athlete = input("Enter the athlete's name: ")
            country_code = input("Enter the athlete's country code: ")

            #Find the athlete 
            cursor.execute("SELECT * FROM Athletes WHERE NameAthlete = %s AND CountryCode = %s", (name_athlete, country_code))
            result = cursor.fetchone()
            if result:
                print("Current details:", result)
            else:
                print("No athlete found with the given name and country code.")
                return

            # Update sport details only if needed
            if input("Update sport details? (y/n): ") == 'y':
                new_sport = input("Enter the new sport: ")
                new_sport_code = input("Enter the new sport code: ")
                
                query = "UPDATE Athletes SET Sport = %s, SportCode = %s WHERE NameAthlete = %s AND CountryCode = %s"
                cursor.execute (query, (new_sport, new_sport_code, name_athlete, country_code))
            
            # Update personal details only if needed
            if input("Update personal details? (y/n): ") == 'y':
                new_dob = input("Enter the new date of birth (YYYY-MM-DD): ")
                new_gender = input("Enter the new gender: ")

                query = "UPDATE Athletes SET DateOfBirth = %s, Gender = %s WHERE NameAthlete = %s AND CountryCode = %s"
                cursor.execute (query, (new_dob, new_gender, name_athlete, country_code))

            print("Athlete Details updated successfully. ")
            cursor.execute("SELECT * FROM Athletes WHERE NameAthlete = %s AND CountryCode = %s", (name_athlete, country_code))
            athlete = cursor.fetchone()
            print(f"New Details: \nAthlete - {athlete[0]} ({athlete[6]}) from {athlete[1]} ({athlete[2]}) participates in {athlete[3]} ({athlete[4]}), born on {athlete[5]}")

    except Exception as e:
        print("Failed to update athlete details: ", e)
        connection.rollback()

def remove_athlete(connection):
    try:
        with connection.cursor() as cursor:
            # Start the transaction
            cursor.execute("BEGIN;")

            # Get identifying information
            name_athlete = input("Enter the athlete's name: ")
            country_code = input("Enter the athlete's country code: ")
            cursor.execute("SELECT * FROM Athletes WHERE NameAthlete = %s AND CountryCode = %s", (name_athlete, country_code))
            result = cursor.fetchone()
            print("Result -", result)
            if result:
                sport = result[3]
                gender = result[6]
                #Delete from Athletes table
                cursor.execute("DELETE FROM Athletes WHERE NameAthlete = %s AND CountryCode = %s", (name_athlete, country_code))
                print("Deleted from Athletes")
                
                #Delete from Medals Tally
                cursor.execute("DELETE FROM Medals WHERE NameAthlete = %s AND CountryCode = %s", (name_athlete, country_code))
                print("Deleted from Medals")

                #Update discipline table to account for the gender count
                if gender.lower() == 'male':
                    print("before update male")
                    cursor.execute("UPDATE Discipline SET Males = Males - 1, Total = Total - 1 WHERE Sport = %s", (sport,))
                else:
                    print("before update female")
                    #query = "UPDATE Discipline SET Females = Females - 1, Total = Total - 1 WHERE Sport = %s"
                    cursor.execute("UPDATE Discipline SET Females = Females - 1, Total = Total - 1 WHERE Sport = %s", (sport,))
                print("Updated gender count in Disciplines")

                connection.commit()
                print(f"Athlete {name_athlete} from {country_code} has been removed successfully.")
            else:
                cursor.execute("ROLLBACK;")
                print("No athlete found with the given name 1and country.")
    except Exception as e:
        print("Failed to remove athlete: ", e)
        connection.rollback()


def view_athlete(connection):
    try:
        # Prompt user for search criteria
        search_criteria = input("Search by Country Code (C) or Sport Code (S): ").upper()
        if search_criteria not in ('C', 'S'):
            print("Invalid selection. Please enter 'C' for Country Code or 'S' for Sport Code.")
            return

        if search_criteria == 'C':
            country_code = input("Enter the athlete's country code: ").upper()
            query = "SELECT * FROM Athletes WHERE CountryCode = %s"
            params = (country_code,)
        elif search_criteria == 'S':
            sport_code = input("Enter the athlete's sport code: ").upper()
            query = "SELECT * FROM Athletes WHERE SportCode = %s"
            params = (sport_code,)

        # Execute the query to fetch athlete details
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            athletes = cursor.fetchall()

            if athletes:
                print("Athlete Details:")
                x = 1
                for athlete in athletes:
                    print(f"[{x}] - Athlete - {athlete[0]} ({athlete[6]}) from {athlete[1]} ({athlete[2]}) participates in {athlete[3]} ({athlete[4]}), born on {athlete[5]}")
                    x += 1
            else:
                print("No athletes found with the given criteria.")

    except Exception as e:
        print("Failed to remove athlete: ", e)
        connection.rollback()


#CLI for Manage Athletes Menu
def manage_athletes(connection):
    while True:
        print("\nManaging Athletes:")
        print("1. Add Athlete")
        print("2. Update Athlete Details")
        print("3. Remove Athlete")
        print("4. View Athlete by Detail")
        print("5. Return to Main Menu")

        answer = input("Enter your choice: ")

        if answer == '1':
            add_athlete(connection)
        elif answer == '2':
            update_athlete_details(connection)
        elif answer == '3':
            remove_athlete(connection)
        elif answer == '4':
            view_athlete(connection)
        elif answer == '5':
            break
        else:
            print("Invalid choice. Please choose again.")

#Query functions for Manage_medals
def most_medals_athlete(connection):
    try:
        with connection.cursor() as cursor:
            #Find the 10 athletes who earned the most medals
            query = """SELECT NameAthlete, COUNT(*) AS TotalMedals FROM Medals
            GROUP BY NameAthlete ORDER BY TotalMedals DESC LIMIT 10;"""
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("Top 10 Athletes with the Most Individual Medals:")
                x = 1
                for result in results:
                    print(f"[{x}] - {result[0]}, Total Medals: {result[1]}")
                    x += 1
            else:
                print("No medal records found.")

    except Exception as e:
        print("Failed to retrieve top athletes with most medals:", e)

def athlete_medal_records(connection):
    name_athlete = input("Enter the athlete's name to view their medal records: ")
    try:
        with connection.cursor() as cursor:

            # Join Athletes with Medals on NameAthlete and CountryCode
            query = """SELECT A.NameAthlete, A.Country, M.Medal, M.Event FROM Athletes A
            INNER JOIN Medals M ON A.NameAthlete = M.NameAthlete AND A.CountryCode = M.CountryCode
            WHERE A.NameAthlete = %s;"""
            cursor.execute(query, (name_athlete,))
            results = cursor.fetchall()
            if results:
                print(f"Medal Records for {name_athlete}:")
                for result in results:
                    print(f"Country: {result[1]}, Medal: {result[2]}, Event: {result[3]}")
            else:
                print("No medal records found for this athlete or athlete does not exist.")

    except Exception as e:
        print("Failed to fetch athlete's medal records:", e)

def athletes_one_medal(connection):
    try:
        with connection.cursor() as cursor:
            #find athletes who have won at least one medal
            query = """SELECT A.NameAthlete, A.Country, A.Sport FROM Athletes A
            WHERE A.NameAthlete IN (SELECT M.NameAthlete FROM Medals M);"""
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("Athletes Who Have Won At Least One Medal:")
                for result in results:
                    print(f"Athlete Name: {result[0]}, Country: {result[1]}, Sport: {result[2]}")
            else:
                print("No athletes have won any medals.")
    except Exception as e:
        print("Failed to retrieve athletes with medals:", e)

    
def display_medal_counts(connection):
    try:
        with connection.cursor() as cursor:
            while True:
                print("Select the type of medal to display counts for:")
                print("1. Gold")
                print("2. Silver")
                print("3. Bronze")
                medal_choice = input("Enter your choice (1-3): ")

                # Mapping user input to the medal type in the SQL query
                medal_types = {
                    '1': 'Gold',
                    '2': 'Silver',
                    '3': 'Bronze'
                }
                medal_selected = medal_types.get(medal_choice, None)

                if medal_selected is None:
                    print("Invalid choice. Please select a valid option (1, 2, or 3).")
                    return

                # SQL query to fetch and display the selected medal counts
                query = f"SELECT Country, SUM({medal_selected}) AS {medal_selected} FROM ParalympicTally GROUP BY Country ORDER BY {medal_selected} DESC;"
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    print(f"{medal_selected} Medal Counts by Country:")
                    for result in results:
                        print(f"Country: {result[0]}, {medal_selected}: {result[1]}")
                else:
                    print(f"No {medal_selected.lower()} medals found.")

    except Exception as e:
        print(f"Failed to display {medal_selected.lower()} medal counts: ", e)

#CLI for managing medals
def manage_medals(connection):
    while True:
        print("\nMedal Records:")
        print("1. View Athletes With Most Medals.")
        print("2. Athletes Medal Records")
        print("3. Athletes Who Earned At Least One Medal")
        print("4. Display Medals Counts By Medal Count")
        print("5. Return to Main Menu")

        choice = input("Enter your choice: ")
        if choice == '1':
            most_medals_athlete(connection)
        elif choice == '2':
            athlete_medal_records(connection)
        elif choice == '3':
            athletes_one_medal(connection)
        elif choice == '4':
            display_medal_counts(connection)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please choose again.")


#Query functions for Manage_disciplines
def view_disciplines(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Sport, Females, Males, Total FROM Discipline ORDER BY Sport;")
            results = cursor.fetchall()
            print("List of All Disciplines:")
            for result in results:
                print(f"Sport: {result[0]}, Female Participants: {result[1]}, Male Participants: {result[2]}, Total Participants: {result[3]}")
    except Exception as e:
        print("Error retrieving all disciplines:", e)

def display_medalling_athletes_for_discipline(connection):
    try:
        # User inputs the sport code
        sport_code = input("Enter the sport code to view athletes who have won medals: ")
        with connection.cursor() as cursor:
            #fetch athletes who have won medals in the specified discipline
            query = """SELECT A.NameAthlete, A.Country, M.Medal, M.Event FROM Athletes A
            JOIN Medals M ON A.NameAthlete = M.NameAthlete AND A.CountryCode = M.CountryCode WHERE A.SportCode = %s;"""
            cursor.execute(query, (sport_code,))
            results = cursor.fetchall()

            if results:
                print(f"Athletes who have won medals in the discipline (Code: {sport_code}):")
                for result in results:
                    print(f"Athlete Name: {result[0]}, Country: {result[1]}, Medal: {result[2]}, Event: {result[3]}")
            else:
                print("No medalling athletes found for this sport code or sport code does not exist.")

    except Exception as e:
        print("Failed to display medalling athletes for the discipline: ", e)


def view_discipline_performance(connection):
    try:
        # User inputs the sport code
        sport_name = input("Enter the sport to view its performance: ")
        with connection.cursor() as cursor:
            #find detailed statistics about the selected sport and the average total participants
            query = """SELECT D.Sport, D.Females, D.Males, D.Total, (SELECT AVG(Total) FROM Discipline) AS AvgTotal
            FROM Discipline D WHERE D.Sport = %s;"""
            cursor.execute(query, (sport_name,))
            result = cursor.fetchone()

            if result:
                print(f"Performance Statistics for {result[0]} (Code: {sport_name}):")
                print(f"Female Participants: {result[1]}")
                print(f"Male Participants: {result[2]}")
                print(f"Total Participants: {result[3]}")
                print(f"Average Total Participants Across All Sports: {result[4]:.2f}")  
            else:
                print("Sport code not found. Please ensure it is correct and try again.")

    except Exception as e:
        print("Failed to retrieve discipline performance data: ", e)




#CLI for managing disciplines
def manage_disciplines(connection):
    while True:
        print("\nDiscipline Insights:")
        print("1. View Disciplines")
        print("2. View Medalling Athletes For Discipline")
        print("3. View Discipline Performance")
        print("4. Return to Main Menu")

        answer = input("Enter your choice: ")
        if answer == '1':
            view_disciplines(connection)
        elif answer == '2':
            display_medalling_athletes_for_discipline(connection)
        elif answer == '3':
            view_discipline_performance(connection)
        elif answer == '4':
            break
        else:
            print("Invalid choice. Please choose again.")


def view_participating_npcs(connection):
    try:
        with connection.cursor() as cursor:
            
            cursor.execute("SELECT Country, CountryCode FROM NPCs ORDER BY Country")
            records = cursor.fetchall()  # Fetch all records 
            
            if records:
                print("List of Participating NPCs:")
                x = 1
                for record in records:
                    print(f"[{x}] - {record[0]},  {record[1]}")
                    x += 1
            else:
                print("No participating NPCs found.")
                
    except Exception as error:
        print("Failed to retrieve participating NPCs:", error)
    finally:
        cursor.close()

#CLI to handle user choices
def main():
    
    #connect to PostgreSQL
    connection = connect("localhost", "postgres", "postgres", "postgres")
    if connection is None:
        return  # Stop the program if the connection fails

    while True:
        print("Welcome to CLI userface for the 2020 Tokyo Paralympics\n")
        print("Menu:")
        print("1. Manage Athletes")
        print("2. Medal Records")
        print("3. Discipline Insight")
        print("4. View Participating NPCs")
        print("5. Exit\n")

        #change to other menus
        answer = input("Enter your choice (1-5):  ")
        if answer == '1':
            manage_athletes(connection)
        elif answer == '2':
            manage_medals(connection)
        elif answer == '3':
            manage_disciplines(connection)
        elif answer == '4':
            view_participating_npcs(connection)
        elif answer == '5':
            break
        else:
            print("Invalid choice. Please choose again.")

    connection.close()

main()

