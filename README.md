Simple script to process `NavRoute` events from EDDN and store data about routes and systems from it.
The script should be fed by entering jsonl events from EDDN to stdin (it makes Bravada's archives very easy to use.
Thank you, Bravada), then script will fill with new data sqlite database `navroutes.sqlite`. 
This DB contains three tables:
1. `systems` - contains main information about systems.
2. `systems_history` - contains history of `systems` changes.
3. `routes` - contain routes.

For more information you can examine `doc.txt` file, database itself or source code of the script.

This repo contains `example.jsonl` - it is example of input data, to use it type `cat example.jsonl | python3 main.py`
and check DB for results.