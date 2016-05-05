from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random


ACCEPTABLE_MONTH_TIMEFRAME = 3


def add_team_vote(*args, **kwargs):
    today = kwargs.pop('today', datetime.now().strftime('%x'))
    entry = today

    with open('LunchSpotData.txt', 'a') as lunch_data_fp:
        for restaurant in args:
            entry += (',' + restaurant)
        entry += '\n'
        lunch_data_fp.write(entry)


def seed_data(number_of_teammates):
    lunch_spot_pool = []
    lunch_spot_features = defaultdict(list)

    # get default pool for restaurants
    with open('LunchSpotFeatures.csv', 'r') as lunch_feature_fp:
        for line in lunch_feature_fp:
            restaurant_info = line.split(',')
            lunch_spot_pool.append(restaurant_info[0])
            for index in range(1, len(restaurant_info)):
                lunch_spot_features[restaurant_info[0]].append(restaurant_info[index])

    start_timestamp = datetime.now() - relativedelta(months=ACCEPTABLE_MONTH_TIMEFRAME)
    for relative_days in range(30 * ACCEPTABLE_MONTH_TIMEFRAME):
        entry_date = start_timestamp + relativedelta(days=relative_days)
        random_team_votes = []
        for team_vote in range(number_of_teammates):
            random_team_votes.append(random.choice(lunch_spot_pool))
        # TODO: don't open and close file for every seed
        add_team_vote(*random_team_votes, today=entry_date.strftime('%x'))


def aggregate_choices(lunch_spot_pool, lunch_spot_features):
    # add tally for each restaurant
    with open('LunchSpotFeatures.csv', 'r') as lunch_feature_fp:
        for line in lunch_feature_fp:
            restaurant_info = line.replace('\n', '').split(',')
            lunch_spot_pool.append(restaurant_info[0])
            for index in range(1, len(restaurant_info)):
                lunch_spot_features[restaurant_info[0]].append(restaurant_info[index])

    # skew restaurant decision toward resturants with more votes
    with open('LunchSpotData.txt', 'r') as lunch_data_fp:
        for line in lunch_data_fp:
            daily_restaurant_decisions = line.replace('\n', '').split(',')
            if datetime.strptime(daily_restaurant_decisions[0], '%x') - relativedelta(months=ACCEPTABLE_MONTH_TIMEFRAME) < datetime.now():
                for index in range(1, len(daily_restaurant_decisions)):
                    lunch_spot_pool.append(daily_restaurant_decisions[index])

    random.shuffle(lunch_spot_pool)

def get_two_choices():
    # select first choice, get set of attributes
    first_choice = random.choice(lunch_spot_pool)
    first_choice_attributes = set(lunch_spot_features[first_choice])

    # get second choice where no attributes overlap
    second_choice = random.choice(lunch_spot_pool)
    second_choice_attributes = set(lunch_spot_features[second_choice])

    while (first_choice_attributes.intersection(second_choice_attributes)):
        second_choice = random.choice(lunch_spot_pool)
        second_choice_attributes = set(lunch_spot_features[second_choice])

    print first_choice
    print second_choice


lunch_spot_pool = []
lunch_spot_features = defaultdict(list)

aggregate_choices(lunch_spot_pool, lunch_spot_features)
get_two_choices()
