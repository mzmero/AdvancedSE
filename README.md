"# Advance Software Engineering- Seminar" 
in this project we calculated the correlation between quality and reuse in a given dataset.
the dataset that's being analyzed , are a set of projects from github thats have the same domain.

To start using the code , you need to fulfill the following tasks:

1 - use CLAN or other tools thats calculate the similarity score between projects (single dataset that have all projects with the same domain) , 
   the result of the tools is a csv file thats look like a matrix where each cell i,j present the similiraity score between project i and project j.
   
2 - place the csv file in folder " data ".

3 - download the metadata on each project and organize it in csv file ( example for metadata such as forks ,startgazing ..etc).

4 - place the csv file in folder " repository ".

5 - download all commits in projects and arrange them in a csv file.

6 - place the csv in folder " commit ".

7 - the name of csv files should be the same for each dataset ,example: os dataset in data , repository and commit folder have the same name such as os.csv 

Notes : 

- By doing step 7 u can use more than 1 dataset and the code will calculate for each dataset the correlation between reuse and quality.

- Look at the data in each folder to understand the tasks , most header names in csv are critical for the code to work such as repo_id, fork..etc

- To test how the code works, runs it using the datasets that exists in the project (there are 3 datasets os , db and tetris) .

- The CLAN version thats we used in the project to measure similarity score is included in CLAN

- The CLAN verison was modiefid so it can create the similarity matrix between each project in the dataset. 
