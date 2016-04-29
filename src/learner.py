from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random


def add_team_vote(*kwargs):
	today = datetime.now().strftime('%x')
	entry = today
	with open('LunchSpotData.txt', 'a') as lunch_data_fp:
		for restaurant in kwargs:
			entry += (',' + restaurant)
		entry += '\n'
		lunch_data_fp.write(entry)

def get_two_choices():
	lunch_spot_pool = []
	lunch_spot_features = defaultdict(list)

	# add tally for each restaurant
	with open('LunchSpotFeatures.csv', 'r') as lunch_feature_fp:
		for line in lunch_feature_fp:
			restaurant_info = line.split(',')
			lunch_spot_pool.append(restaurant_info[0])
			for index in range(1, len(restaurant_info)):
				lunch_spot_features[restaurant_info[0]].append(restaurant_info[index])

	# skew restaurant decision toward resturants with more votes
	with open('LunchSpotData.txt', 'r') as lunch_data_fp:
		for line in lunch_data_fp:
			daily_restaurant_decisions = line.split(',')
			if datetime.strptime(daily_restaurant_decisions[0], '%x') - relativedelta(months=3) < datetime.now():
				for index in range(1, len(daily_restaurant_decisions)):
					lunch_spot_pool.append(daily_restaurant_decisions[index])

	random.shuffle(lunch_spot_pool)

	# select first choice, get set of attributes
	first_choice = random.choice(lunch_spot_pool)
	first_choice_attributes = set(lunch_spot_features[first_choice])
	print first_choice

	# get second choice where no attributes overlap
	second_choice = random.choice(lunch_spot_pool)
	second_choice_attributes = set(lunch_spot_features[second_choice])
	while (first_choice_attributes.intersection(second_choice_attributes)):
		second_choice = random.choice(lunch_spot_pool)
		second_choice_attributes = set(lunch_spot_features[second_choice])

	print second_choice

get_two_choices()
