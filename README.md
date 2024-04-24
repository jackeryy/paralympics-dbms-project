# Paralympics Database Management System

This project is a CLI-based database management system for the 2020 Tokyo Paralympics, built using PostgreSQL. It provides functionalities to manage athletes, disciplines, medals, and more through an interactive command-line interface.

## Getting Started

To get started, ensure you have Python and PostgreSQL installed. Clone this repository and follow these steps:

1. Set up the PostgreSQL database using the provided SQL scripts.
2. Import the CSV files to populate the database with initial data (see "CSV File Import Instructions").
3. Run the CLI script to interact with the database system.

## CSV File Import Instructions

To populate the database, you need to import several CSV files. Follow these steps:

1. Ensure PostgreSQL is running and accessible.
2. Open pgAdmin4 and navigate to the Tables section on the left sidebar
3. Right click on the table you would like to fill
4. Select "Import/Export Data...." and then select on the matching CSV file for the table

## Usage Instructions

After setting up the project, run the CLI script to access the menu. You can manage athletes, view medal records, and gain insights into various disciplines. Below is a brief explanation of the CLI menu options:

- **Manage Athletes**: Add, update, remove, or view athletes.
- **Medal Records**: View medal counts by type, top athletes, and medal records for individual athletes.
- **Discipline Insights**: View aggregate statistics, medalling athletes for a discipline, and discipline performance.
- **View Participating NPCS**: Displays all NPCs participating in the 2020 Tokyo Paralympics.

## Folder Structure

- `sql_scripts/`: Contains the SQL script to set up the PostgreSQL database.
- `cli_functions/`: Contains the Python script for CLI-based functionalities.
- `docs/`: Contains the project documentation, including detailed instructions and examples.
- `csv_files/`: Contains CSV files used to fill the tables

## Additional Notes

- **Software Requirements**: Ensure you have Python and PostgreSQL installed on your system.
- **Troubleshooting**: If you encounter issues, check your PostgreSQL configuration and database connection settings.
