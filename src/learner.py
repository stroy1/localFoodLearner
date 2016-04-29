from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta


lunch_spot_tally = defaultdict(int)
with open('LunchSpotFeatures.csv', 'r') as lunch_feature_fp:
	for line in lunch_feature_fp:
		restaurant_info = line.split(',')
		lunch_spot_tally[restaurant_info[0]] += 1

with open('LunchSpotData.txt', 'r') as lunch_data_fp:
	for line in lunch_data_fp:
		daily_restaurant_decisions = line.split(',')
		if datetime.strptime(daily_restaurant_decisions[0], '%x') - relativedelta(months=3) < datetime.now():
			for index in range(1, len(daily_restaurant_decisions)):
				lunch_spot_tally[daily_restaurant_decisions[index]] += 1

print lunch_spot_tally
