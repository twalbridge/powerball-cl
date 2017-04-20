import os
import random
import operator
import re
from fuzzywuzzy import fuzz 

only_letters = re.compile(r'^[a-z A-Z \']{2,}$')
all_entry_names_and_their_nums = {}
list_of_ball_nums = {}
list_of_powerball_nums = {}
initial_instructions_list = []


def initial_instructions(name):
	"""
	Initial instructions for first time participants.
	"""
	if name not in initial_instructions_list:
		initial_instructions_list.append(name)
		return "\n{:^75}\n{:^75}\n{:^75}\n{:^75}\n{:^75}\n\n{:^75}\n".format(
			"* " + name.split()[0] + \
			" please fill out the survey by entring your favorite *",
			"* lottery numbers! The most popular entries will be considered *",
			"* lucky and will therefore be used to purchase one very lucky *",
			"* lottery ticket! The final PowerBall number must be between 1 *",
			"* and 26. All other number selections must be between 1 and 69. *", 
			"** Multiple entries are encouraged! **"
		)
	return ""


def sort_nums(unsort_d_list):
	"""
    Handles reverse sorting.
    """
	return sorted(
		unsort_d_list.items(), 
		key=operator.itemgetter(1), 
		reverse=True
	)


def pick_random_balls(fav_list):
	"""
    Used in the event of less than 5 duplicate ball selection.
    """
	exempt_nums = []
	for num in fav_list:
		exempt_nums.append(num)
	while len(fav_list) < 5:
		random_num = random.choice(range(1, 70))
		if str(random_num) not in exempt_nums:
			fav_list.append(str(random_num))
	return fav_list


def most_popular_balls(balls):
	"""
    Sorts and possibly randomly selects highest ranking duplicate balls.
    """
	luckiest_balls = []
	temp_list_of_equals = []
	for num in balls:
		if num[1] > 1:
			if len(luckiest_balls) < 5:
				if len(temp_list_of_equals) == 0:
					temp_list_of_equals.append(num)
				elif num[1] == temp_list_of_equals[0][1]:
					temp_list_of_equals.append(num)
				else:
					if len(luckiest_balls) + len(temp_list_of_equals) > 5:
						while len(luckiest_balls) < 5:
							pick = random.choice(temp_list_of_equals)
							luckiest_balls.append(pick[0])
							temp_list_of_equals.remove(pick)
						temp_list_of_equals.clear()
						break
					else:
						for x in temp_list_of_equals:
							luckiest_balls.append(x[0])
							temp_list_of_equals = []
							temp_list_of_equals.append(num)
		else:
			if len(temp_list_of_equals) > 0:
				if len(luckiest_balls) + len(temp_list_of_equals) > 5:
					while len(luckiest_balls) < 5:
						pick = random.choice(temp_list_of_equals)
						luckiest_balls.append(pick[0])
						temp_list_of_equals.remove(pick)
				else:
					for x in temp_list_of_equals:
						luckiest_balls.append(x[0])
			if len(luckiest_balls) < 5:
				luckiest_balls = pick_random_balls(luckiest_balls)
				break
	for num in temp_list_of_equals:
		luckiest_balls.append(num[0])
	return luckiest_balls


def most_popular_powerball(powerballs):
	"""
    Sorts and possibly randomly selects the highest ranking duplicate 
    powerball.
    """
	popular_powerballs = []
	for num in powerballs:
		if num[1] > 1:
			if len(popular_powerballs) == 0:
				popular_powerballs.append(num[0])
			else:
				if num[1] in popular_powerballs:
					popular_powerballs.append(num[0])
	if len(popular_powerballs) > 0:
		luckiest_powerball = random.choice(popular_powerballs)
	elif len(popular_powerballs) == 1:
		luckiest_powerball = popular_powerballs
	else:
		luckiest_powerball = random.choice(range(1, 27))
	return luckiest_powerball


def select_most_popular(balls, powerballs):
	"""
    String formats final selection.
    """
	selection = "* Current most popular selection! {d[0]} {d[1]} {d[2]} {d[3]} {d[4]} and Powerball {p} *".format(
		d=most_popular_balls(balls),
		p=most_popular_powerball(powerballs)
		)
	return "{:^75}".format(selection)


def create_ball_choices_str(entries_for_name):
	"""
    String formats entry(ies) per player.
    """
	numbers = ""
	for ball_list in entries_for_name:
		all_nums = "\n\t\t{d[0]:>2} {d[1]:>2} {d[2]:>2} {d[3]:>2} {d[4]:>2} and Powerball {d[5]:>2}".format(
			d=ball_list)
		numbers += all_nums
	return numbers


def find_all_entries_for_name(full_name):
	"""
    String formats instance player's selection(s).
    """
	initial_response = " Please try again!"
	entries_for_name = all_entry_names_and_their_nums[full_name]
	again = ""
	entry = "entry is"
	if len(entries_for_name) > 1:
		again = " again"
		entry = "entries are"
	numbers = create_ball_choices_str(entries_for_name)
	return "Successfully submitted{}.\n\tYour {}:{}\n".format(
		again,	
		entry,
		numbers
	)


def list_all_entries_and_participants(instance_participant):
	"""
    String formats alphabetically all players with their corresponding 
    entries.
    """
	entries_str = ""
	if len(all_entry_names_and_their_nums) > 1:
		alphabetical_entries = sorted(
			sorted(
				all_entry_names_and_their_nums
				), 
				key=lambda n: n.split()[1]
			)
		entries_str = "All other entries:"
		for entry in alphabetical_entries:
			if entry != instance_participant:			
				numbers = create_ball_choices_str(all_entry_names_and_their_nums[entry])
				entries_str += "\n\t{}:{}".format(
					entry,
					numbers
				) 
	return entries_str



def controller(play=""):
	"""
    Handles general flow.
    """
	while play != "q":
		entry = Entry()
		first_name = entry.clean_name(
			"Enter your first name: "
		)
		entry.full_name = entry.clean_last_name(
			"Enter your last name: ", first_name
		)
		similar_names = []
		for name in all_entry_names_and_their_nums:
			ratio = fuzz.ratio(name, entry.full_name)
			if 85 <= ratio < 100:
				similar_names.append((name, ratio))
		sorted_similar_names = sorted(
			similar_names, 
			key=operator.itemgetter(1), 
			reverse=True
		)
		for similar in similar_names:
			consider = input("\tDid you mean {}? ('y' to AGREE otherwise press 'Enter'): ".format(
				similar[0]))
			if "y" in consider or "Y" in consider:
				entry.full_name = similar[0]
		print(initial_instructions(entry.full_name))
		entry.first_favorite = entry.clean_number(
			"Select 1st: "
		)
		entry.second_favorite = entry.clean_number(
			"Select 2nd: "
		)
		entry.third_favorite = entry.clean_number(
			"Select 3rd: "
		)
		entry.fourth_favorite = entry.clean_number(
			"Select 4th: "
		)
		entry.fifth_favorite = entry.clean_number(
			"Select 5th: "
		)
		entry.power_ball_number = entry.clean_power_ball_number(
			"Select Power Ball: "
		)
		for num in entry.picks:
			if num in list_of_ball_nums:
				list_of_ball_nums[num] += 1
			else:
				list_of_ball_nums.update({num: 1})
		if entry.power_ball_number in list_of_powerball_nums:
			list_of_powerball_nums[entry.power_ball_number] += 1
		else:
			list_of_powerball_nums.update({entry.power_ball_number: 1})
		balls, powerballs = sort_nums(list_of_ball_nums), sort_nums(list_of_powerball_nums)
		entries = (
			entry.first_favorite,
			entry.second_favorite,
			entry.third_favorite,
			entry.fourth_favorite,
			entry.fifth_favorite,
			entry.power_ball_number
		)
		if entry.full_name in all_entry_names_and_their_nums:
			all_entry_names_and_their_nums[entry.full_name].append(entries)
		else:
			all_entry_names_and_their_nums.update(
				{entry.full_name: [entries]}
		)
		print(
			"-" * 75,
			"\n\n",
			select_most_popular(balls, powerballs),
			"\n\n",
			find_all_entries_for_name(entry.full_name),
			"\n",
			list_all_entries_and_participants(entry.full_name),
		)
		play = input("\nNew entry? ('q' to quit): ")


class Entry():
	"""
    For each entry instance: Handles ensuring that the exceptable inputs 
    are valid. First name and last name are first letter capitalized only 
    and not unique together duplicated names. Verify the first 5 numbers 
    range from 1-69 without duplicates and the 6th number range from 1-26.
    """

	def __init__(self, *args, **kwargs):
		super(Entry, self).__init__(*args, **kwargs)
		self.picks = []


	def clean_name(self, name):
		"""
		Handles ensuring entry instance uses only letters, is only one name 
		and is capitalized.
		"""
		name_choice = input(name)
		if not only_letters.search(name_choice):
			print (
				'\tEnter a valid name. This value must contain only letters.'
			)
			return self.clean_name(name)
		sep = ' '
		return name_choice.strip().split(sep, 1)[0].capitalize()

	def clean_last_name(self, name, first_name):
		"""
		Handles ensuring entry instance uses only letter and is capitalized 
		and looks for a name match.
		"""
		last_name_choice = self.clean_name(name)
		return "{} {}".format(
			first_name, 
			last_name_choice
		)

	def clean_number(self, fav_selection):
		"""
		Handles checking for duplicated entries instance numbers 1 - 5.
		"""
		fav_number = input(fav_selection)
		if fav_number.isdigit() and 1 <= int(fav_number) <= 69:
			fav_number = int(fav_number)
			if fav_number in self.picks:
				print('\tDuplicates are not allowed. Try a number other \
					than {}'.format(
						fav_number)
				)
				return self.clean_number(fav_selection)
			self.picks.append(fav_number)
			return fav_number
		else:
			print('\tEnter a valid number between 1 through 69.')
			return self.clean_number(fav_selection)

	def clean_power_ball_number(self, fav_selection):
		"""
	    Handles ensuring entry instance is a number and populating the 
	    PowerBall favorites. Then forwards the list to 
	    """
		power_ball = input(fav_selection)
		if power_ball.isdigit() and 1 <= int(power_ball) <= 26:
			return int(power_ball)
		else:
			print('\tEnter a valid number between 1 through 26.')
			return self.clean_power_ball_number(fav_selection)


if __name__ == "__main__":
	controller()
