
import json
from neo4jrestclient.client import GraphDatabase
import argparse
import sys
import os


class PredictionDataImport(object):

    def __init__(self, uri, username, password):
        self.gdb = GraphDatabase(uri, username=username, password=password)

    def convert_to_dict(self, arr):
        D = {}
        for d in arr:
            key, val = list(d.items())[0]
            D[key] = val
        return D

    def import_188(self, data, method):

        for row in data:

            team1 = row['MATCHNAME']['team1']
            team2 = row['MATCHNAME']['team2']

            create_script = """CREATE (bet_odds_prediction:BET_ODDS_PREDICTION 
                            {
                                team1: '%s', 
                                team2: '%s', 
                                matchtime: '%s',
                                chance: '%s', 
                                dice: '%s', 
                                onextwo: '%s',
                                firsthalf_chance: '%s',
                                firsthalf_dice: '%s',
                                firsthalf_onextwo: '%s'
                            })
                    """ % (team1.title(),
                           team2.title(),
                           row['DATETIME'],
                           json.dumps(row['CATRAN-handicap']),
                           json.dumps(row['CATRAN-underover']),
                           json.dumps(row['CATRAN-onextwo']),
                           json.dumps(row['HIEP1-handicap']),
                           json.dumps(row['HIEP1-underover']),
                           json.dumps(row['HIEP1-onextwo']),
                           )

            update_script = """MATCH (bet_odds_prediction:BET_ODDS_PREDICTION)
                                        WHERE bet_odds_prediction.team1 = '%s' AND bet_odds_prediction.team2 = '%s' 
                                        SET
                                            bet_odds_prediction.chance = '%s',
                                            bet_odds_prediction.chance = '%s',
                                            bet_odds_prediction.dice = '%s',
                                            bet_odds_prediction.onextwo = '%s',
                                            bet_odds_prediction.firsthalf_chance = '%s',
                                            bet_odds_prediction.firsthalf_dice = '%s',
                                            bet_odds_prediction.firsthalf_onextwo = '%s'
                                """ % (team1.title(),
                                       team2.title(),
                                       row['DATETIME'],
                                       json.dumps(row['CATRAN-handicap']),
                                       json.dumps(row['CATRAN-underover']),
                                       json.dumps(row['CATRAN-onextwo']),
                                       json.dumps(row['HIEP1-handicap']),
                                       json.dumps(row['HIEP1-underover']),
                                       json.dumps(row['HIEP1-onextwo']),
                                       )

            try:
                if method == 'create':
                    create_result = self.gdb.query(create_script, data_contents=True)
                    print(create_result)
                    print('SUCCESSFULLY CREATE ON MATCH (%s - %s)' % (team1, team2))

                    merge_script = """
                                            MATCH (match:MATCH)-[:BELONG_TO]->(tournament:TOURNAMENT), 
                                                    (bet_odds_prediction:BET_ODDS_PREDICTION) 
                                                WHERE   match.team1 = bet_odds_prediction.team1 
                                                    AND match.team2 = bet_odds_prediction.team2 
                                                    AND tournament.name =~ ".*2018.*" 
                                                CREATE (bet_odds_prediction)-[:PREDICT]->(match) 
                                                RETURN bet_odds_prediction, match
                                        """
                    merge_results = self.gdb.query(merge_script, data_contents=True)
                    print(merge_results)
                    print("SUCCESSFULLY MERGE BET_ODDS_PREDICTION TO MATCH")

                if method == 'update':
                    update_result = self.gdb.query(update_script, data_contents=True)
                    print(update_result)
                    print('SUCCESSFULLY UPDATE ON MATCH (%s - %s)' % (team1, team2))
            except Exception as e:
                print(e)

    def import_matchscore(self, data, method):
        match_data = data

        for row in match_data:

            team1 = row['first_team'].strip().title()
            team2 = row['second_team'].strip().title()

            try:
                match_time = row['match_time']

                match_score = row['match_score']
                score1, score2 = match_score.split()

                result_fulltime = {}
                result_fulltime['team1'] = team1.title()
                result_fulltime['team2'] = team2.title()
                result_fulltime['score1'] = int(score1)
                result_fulltime['score2'] = int(score2)
            except:
                print('TRAN DAU CHUA BAT DAU')
                continue

            update_script = """MATCH (match:MATCH)
                            WHERE match.team1 = '%s' AND match.team2 = '%s' 
                            SET
                                match.result_fulltime = '%s',
                                match.time = '%s' 
                    """ % (team1.title(),
                           team2.title(),
                           json.dumps(result_fulltime),
                           match_time
                           )

            try:
                if method == 'create':
                    print('THIS METHOD DOES NOT ALLOW CREATING')
                    return None

                if method == 'update':
                    print(update_script)
                    update_result = self.gdb.query(update_script, data_contents=True)
                    print(update_result)
                    print('SUCCESSFULLY UPDATE ON MATCH (%s - %s)' % (team1, team2))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    pi = PredictionDataImport("http://10.199.220.179:7474/", "neo4j", "123456")

    parser = argparse.ArgumentParser(description='Index data to neo4j')
    parser.add_argument('-s', '--source', dest='source', default='188bet')

    parser.add_argument('-m', '--method', dest='method', default='update')

    args = parser.parse_args()

    if args.method not in ['update', 'create']:
        print('Only allow method from [update, create]')
        sys.exit(1)
    else:
        method = args.method

    if args.source == '188bet':
        with open(os.path.abspath('188.json'), 'r') as f:
            data = json.loads(f.read())
            pi.import_188(data, method)

    elif args.source == 'matchscore':
        with open(os.path.abspath('winner.json'), 'r') as f:
            data = json.loads(f.read())
            pi.import_matchscore(data, method)

    else:
        print('Only allow source from [188bet, matchscore]')
        sys.exit(1)