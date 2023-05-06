# MixtureModelScript
Scripts for estimating and testing amino acid models

This guide runs on Linux OS

TO ESTIMATE MODELS:

Step 1: unzip the alignments to estimate model in estimate_scripts folder

unzip aln.zip

Step2: run script to estimate

python mix_process.py 4x 29 51 1 0.999 &

Option: 4x means estimate the free_schema rate. To estimate gamma rate you change to 4m.
Option: 29 is the number of alignments in each folders.
Option: 51 is the number of folders.
Here, data is splitted into 51 sub-folders and have 29 alignments in each folder except folder 50 has 21 alignments, totally we have 1471 alignments. 
Option: 1 mean you can continue process at certain loop, 2 or 3 or 4, .etc by replace 1 with 2 or 3 or 4, respectively. Before redo from a loop, you need run this command: "touch un.do".
Option: 0.999 is the stop condition by calculating pearson correlation between current estimated models and previous models.
After running the command at step2, the process will execute undergroundly. And, it will stop after some loops. 
