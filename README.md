# ASU Group Forming Tool

[![codecov](https://codecov.io/gh/zredinger/team-58/branch/main/graph/badge.svg?token=UEEKNFR2WG)](https://codecov.io/gh/zredinger/team-58)

This application allows a user to provide student surveys and generate groups based on specific criteria. It uses 2 algorithms to group the students as best it can. It also provides reporting capabilities to identify grouping statistics

## Setup

There are compiled binaries available for both windows and linux. They can be found under Github Releases. Download a release and it can be called directly from the command line.

## Usage

When the application has been downloaded, it is ready for use. The file can now be run from the CLI.

Note: For windows users, you may be prompted to allow the program to be executed.

Note: Input values (the data that is coming in from the survey file) will automatically be scrubbed for extraneous white spaces where appropriate.

Example command:

```
./grouper-windows-amd64.exe group
```

There are four different functions that this application can perform:

1. Generation: This function generates test survey data
2. Grouping: This function performs grouping on survey data
3. Reporting [Deprecated]: This function creates a report of the grouping results 
4. Updating a report: This will take a report from a grouping run that has already completed, and the user has made manual changes to, and it will re-evaluate all the metrics in the report and make sure all the formatting is normalized.

Each of these functions are accessible from the CLI (Command Line Interface)

Starting the program will display general help for using the applications, including the three commands for the three functions this application can perform,
along with a short description of what each command does.
Additionally, using any of these commands followed by --help will provide usage information for that command.

These are the commands and their usage:

## gen

gen [-f,--filename PATH_TO_OUTPUT_FILE] [-c,--count NUMBER_OF_RECORDS]

The gen file generates random survey data. The gen command will output the generated survey data as a CSV file and takes two optional parameters. They are as follows:

1. **-f, --filename** : the output file name where the generated data will be stored. The default is dataset.csv
2. **-c, --count** : the number of records to generate. The default is 20

## group

group SURVEYFILE [-o,--outputfile PATH_TO_OUTPUT_FILE] [-c,--configfile PATH_TO_CONFIG_FILE] [--report|--no-report] [-r,--reportfile PATH_TO_REPORT_FILE][-a, --allstudentsfile PATH_TO_ROSTER_OF_ALL_STUDENTS]

The group command performs grouping on survey data. The survey data is expected to be in CSV format with the first record being a header for the column names.
The group command takes one required parameter and four optional parameters.
The group command should make sure that algorithm correctly determines availability based on time slots, and that students are assigned with at least 1-2 preferred students instead of as many as possible.

1. **surveyfile** : the first required parameter after the group command should be the path to the survey data.
2. **-c, --configfile** : this is a JSON-formatted configuration file. The default name for this file is config.json with the file being in the same location as the program.
    More details on the structure of the configuration file are included later in this README.
3. **-r, --reportfile** : this is the path for the output file for the report generated from the grouping results. Note that this option is ignored if the --verify option is 
    not used. If --verify is used and this option is not set, the file name will be report-{outputfile}.xlsx, where {outputfile} is the file name used for the grouping
    data. Also note that the file is of type xlsx, an Excel file, and will have multiple sheets.
4. **-a, --allstudentsfile** : this is the path for a CSV file whose first column contains a list of all of the student IDs in the class. If this option is provided, the "roster" file will be used to add students that did not fill out the survey. This ensures that all students in the class will be grouped. The student IDs in the file must be the same format as the student IDs in the survey file.

NOTE: Any student who does not indicate any availability in the survey will be assigned full availability for all time slots for the purpose of grouping. This also means any student added automatically from the list of all students (the allstudentsfile option) will also be assigned full availability for the purpose of grouping.
## Report

report GROUPFILE SURVEYFILE [-c,--configfile PATH_TO_CONFIG_FILE] [-r,--reportfile PATH_TO_REPORT_FILE]

The report command creates a report from the grouping results. The report command takes 2 additional optional parameters. Ensure that the **surveyfile** is the data used as
the source for the **groupfile** and that the same configuration file is used that was used when generating **groupfile**.

NOTE: Now that the group command makes only the report file by default, there is no longer an output file to pass as a parameter.  For now this command is being kept.

1. **groupfile** : the second required parameter after the verify command. This should be the grouping CSV file generated by a group command (or manually edited) whose
2. **surveyfile** : the first required parameter after the verify command. This should be the same file that was used to generate the **groupfile**.
   source survey data was the **surveyfile** provided to the first parameter.
3. -c, --configfile : this should be the path to the configuration file used when creating the **groupfile**. Its default value is config.json
4. -r, --reportfile: this is the path for the output file for the report generated from the grouping results. Its default value is grouping_results_report.xlsx. Note that this is an Excel file and will contain multiple sheets

update-report REPORTFILE

The update-report command properly updates the individual report, group report, overall report, config and survey data inside of the report based on the given **reportfile** and outputs the
same report with new result info based on the manual group changes made to it. The **reportfile** is the excel file generated from when you run the group or report command shown above and
includes the config and survey data in separate worksheet tabs.

1. **reportfile**: the first required parameter for the update-report command. This should be a valid report file in excel generated by the group or report command.

## Configuration File

The configuration file controls how the application operates and identifies the fields used to generate grouping and verification data. The configuration file should be in
JSON format. The following is the structure and explication of the configuration file:

```jsonc
{
  /*string, name of the class the grouping is for*/
  "class_name": "SER401",
  /*number, target size of each group */
  "target_group_size": 5,
  /*boolean, allow groups to have one more member than the target group size*/
  "target_plus_one_allowed": true,
  /*boolean, allow groups to have one less member than the target group size*/
  "target_minus_one_allowed": true,
  /* number (0, 1, or 2), Select a method for grouping students who did NOT fill out the survey:
        0 = Standard grouping -- no special treatment of these students.
        1 = Distribute evenly -- these students are distributed as evenly as possible among all groups,
            with larger groups (if applicable) receiving these students "first".
        2 = Group together -- these students are grouped together to the extent possible */
  "no_survey_group_method": 0,
  /*number, the number of passes that will happen to generate the group*/
  "grouping_passes": 2,
  /*used to denote what the availability is separated on, if multiple characters, simply type them all with no spaces or separators, every character typed will be considered a delimiter.  As written below, it will separate on either a colon or a semicolon*/
  "availability_values_delimiter": ";:",
  /*structure, matches the names of the fields found in the survey data to the fields required for grouping*/
  "field_mappings": {
    /*string, name of the field that contains the student's asurite ID*/
    "student_id_field_name": "Please select your ASURITE ID",
    /*string, name of the field that contains the timezone information*/
    "timezone_field_name": "In what time zone do you live or will you be during the session? Please use UTC so we can match it easier.",
    /*array of strings, names of the fields that contain an ID for a preferred student teammate*/
    "preferred_students_field_names": [
      "Preferred team member 1",
      "Preferred team member 2",
      "Preferred team member 3",
      "Preferred team member 4",
      "Preferred team member 5"
    ],
    /*array of strings, names of the fields that contain an ID for a student who is not preferred to be on the same team*/
    "disliked_students_field_names": [
      "Non-preferred student 1",
      "Non-preferred student 2",
      "Non-preferred student 3"
    ],
    /*array of strings, names of the fields that contain date/time availability*/
    "availability_field_names": [
      "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]",
      "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]",
      "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]",
      "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]",
      "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]",
      "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]",
      "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]",
      "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]"
    ]
  },
  /*structure, settings for what information is included in the verification report */
  "report_fields": {
    /*boolean, include the mappings of each student's preferred teammates*/
    "show_preferred_students": false,
    /*boolean, include the mappings of each student's preference to not be on a team with another student*/
    "show_disliked_students": false,
    /*boolean, include a list of the date/time slices that overlap for all students in each group*/
    "show_availability_overlap": false,
    /*boolean, include the scoring results for each group*/
    "show_scores": true
  },
  /*boolean, include the student's full name in the grouping output*/
  "output_student_name": false,
  /*boolean, include the student's email address in the grouping output*/
  "output_student_email": true,
  /*boolean, include the student's login name in the grouping output*/
  "output_student_login": true
}
```

---

## Developer Setup

This application is a python CLI app. For development purposes it should be executed using the python interpreter directly. Pipenv should be used for managing python packages and ensuring dependencies are up-to-date. This allows developers to maintain consistent environments.

### Local Setup

Run these commands in the root context of the repository

1. Install python 3.10.\* [Download here](https://www.python.org/downloads/)
2. Install pipenv

```
pip install pipenv
```

3. Install pipenv to manage dependencies and virtual envs

```
pipenv install
```

4. Start the virtual environment

```
pipenv shell
```

5. Run the code. This will run the cli.

```
python grouper.py
```

## CI Configuration

A Github action has been configured in this repository for managing the Continuous Integration flow after opening a PR. The action currently runs a couple of things against the source code and requires that they pass before merging pull requests:

- unit tests - pytest is used to run unit tests
- linter - pylint is our linter of choice

## Creating Releases

Releases should be created when a new version is ready. Releases can be created in github.

### How To Create a release in Github

1. Ensure all feature branches are merged into main branch.
2. Open the releases tab on the right in the github repository home
3. Click "Draft Release"
4. Add a release with a new tag
5. Use the autogenerate option for release notes.
6. Upon completion, click "Publish Release". This will create the release and run a github action that compiles the linux and windows binaries. These will be uploaded to the release assets.

### Compiling locally

The application can be compiled locally via pyinstaller to test the functionality using it as an executable file. This uses the same build script as the release workflow found in `/build-scripts/build.py`

To build this locally, run the following:

```
python ./build-scripts/build.py
```

This will generate the file as grouper(.exe) in the root of your repository
