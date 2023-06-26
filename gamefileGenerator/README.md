# Create gamefiles

Run with 4 arguments
- filename - location of a csv file with questions
- number of gamefiles to generate
- number of distinct subjects in each gamefile
- number of questions per subject in each gamefile

Eg. to create eight different gamefiles each game with 5 subjects with 6 questions

```
python create-gamefiles.py masterdocument.csv outputfile.xlsx 8 5 6
```


Prerequsites
- There must be enough questions in each subject to fill at least one gamefile
