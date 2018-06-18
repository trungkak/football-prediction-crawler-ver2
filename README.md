# football-prediction-crawler

###  Installation

1. Install Selenium
    ```
    $ pip install selenium
    ```

2. Install pyvirtual display

    ```
    $ apt-get install xvfb
    $ pip install pyvirtualdisplay

    ```

### Crawl data

Bet odds from 188

    $ python 188bet.py

Match score and time from google

    $ python winner.py

    
### Index database

To update match score and time, run

    python neo4j_import.py --source matchscore --method update
    
To update betodds prediction, run

    python neo4j_import.py --source 188bet --method update
