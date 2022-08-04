### Mini Docker Based System
___
This is a a mini docker based system containing 3 modules:

1. The first module will search inside a folder (theHarvester) containing multiple files and folders and, extract a password contained in one of them (we will search for the word password to find it).
2. The second module will analyze the files as so:
   1. Find the number of files from each type (e.g. .py, .txt, etc...)
   2. List the top 10 files by size sorted.
3. The third module will be a controller whose job is to execute the other modules and output the results (from both modules) to a json file.

The communication between the controller and the module conducted through a message broker container (RabbitMQ).

Each module run in a docker container of its own, and all containers runs using docker compose file.

NOTE:
* There is no communication between the analyze and password modules. They are in different networks.
* The folders to analyze available in the containers by volumes.
