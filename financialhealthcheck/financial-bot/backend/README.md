# Backend

Python backend where the conversation orchestration happens.

# Setup

1 - create a venv and activate (optional)

```bash
python -m venv bot-backend-env
```

```bash
# unix bash
source bot-backend-env/bin/activate
```

```bash
# windows powershell
.\bot-backend-env\Scripts\Activate.ps1 
```

```bash
# windows cmd
.\bot-backend-env\Scripts\activate.bat
```

2 - install requirements

```bash
pip install -r requirements.txt
```

3 - Setup your environment variables. You can use a .env file as follows:

```bash
GRAPH_DB_SERVER="bolt://localhost:7687"
GRAPH_DB_USER="neo4j"
GRAPH_DB_PASSWORD="12345678"
FLASK_HOST="127.0.0.1"
FLASK_PORT="8000"
```

This example is also available in ```example.env```.

# Running

```bash
python app.py
```

The system probably would not run via ```flask run``` since other integrations are initialised in the ```__main__```. Can be changed later on.

# Testing
It is possible to test prompts by effectively engaging LLMs with each other, thus eliminating human interaction (manual answering). To do this, generate answers first, then, use the answers to compare LLMs, and finally, analyse results.
## Generating answers 
To generate answers for characters (profiles) from characters.py, access the following route
```
/conversations/mcd/init
```
Once you get a 200 code response, check ```/logs/chat/``` folder. It should contain ```i_answers.json``` where ```i``` indicates character(profile) id from character.py.
## Compare LLMs
Once answers are generated, they can be used to run automatic LLM conversations.
Accessing the following route
```
/conversations/mcd/compare-llms
````
would start a number of conversations for each of the profiles. The number of conversations would equal to number of unique answers for each of the questions(defined by ```Defaults.answers_to_generate_count```) multiplied by number of characters(see ```character.py```).

Once you get 200 code response, check ```logs/chat/{today's data}/```. It should contain ```compare_char_i_conv_j_model_k_{date and time}-{session_id}.log``` files, where  ```i``` indicates character(profile) id, ```j``` conversation number, ```k``` model id (see ```GptModelNames``` in ```defaults.py```).

These files represent interaction between LLM representing human (based on profile) and LLM representing NLP (extracting data and saving to graph db).
### Limitations
**Currently, the application expects the  ```logs/chat/{today's data}/``` folder to only contain files relevant to a single run. That is, it has not been tested to support multiple sessions and removing or renaming of the ```{today's data}``` folder is recommended before accessing the route.**
## Analyse results
Once logs are generated, they can be used for analysis and comparison of the models.
Accessing the following route would return a json result with comparison analysis.
```
/conversations/mcd/comparison-results
```
