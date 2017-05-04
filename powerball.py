import operator
import random
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

#####
def sort_nums(unsort_d_list):
    """
    Handles reverse sorting.

    >>> sort_nums({1: 4, 2: 1, 3: 3, 4: 7, 5: 2})
    [(4, 7), (1, 4), (3, 3), (5, 2), (2, 1)]

    >>> sort_nums({17: 48, 27: 11, 35: 3, 41: 7, 65: 8})
    [(17, 48), (27, 11), (65, 8), (41, 7), (35, 3)]
    """
    return sorted(
        unsort_d_list.items(), 
        key=operator.itemgetter(1), 
        reverse=True
    )


def pick_random_balls(fav_list):
    """
    Used in the event of less than 5 duplicate ball selection.

    >>> pick_random_balls([4, 1, 3, 5, 2])
    [4, 1, 3, 5, 2]

    >>> pick_random_balls([4, 55, 32, 5, 56])
    [4, 55, 32, 5, 56]
    """
    exempt_nums = [num for num in fav_list]
    while len(fav_list) < 5:
        random_num = random.choice(range(1, 70))
        if random_num not in exempt_nums:
            fav_list.append(random_num)
            exempt_nums.append(random_num)
    return fav_list

##
def most_popular_balls(balls):
    """
    Sorts and possibly randomly selects highest ranking duplicate balls.

    >>> most_popular_balls([(1, 5), (3, 5), (5, 2), (23, 2), (4, 2), (7, 1), (9, 1)])
    [1, 3, 4, 5, 23]

    >>> most_popular_balls([(1, 5), (3, 4), (5, 4), (23, 2), (4, 2), (7, 1), (9, 1)])
    [1, 3, 4, 5, 23]

    >>> most_popular_balls([(1, 5), (3, 5), (5, 5), (23, 5), (4, 5), (7, 1), (9, 1)])
    [1, 3, 4, 5, 23]

    most_popular_balls([(1, 5), (3, 5), (5, 2), (23, 2), (4, 1), (7, 1), (9, 1)])
    [1, 3, 4, 5, random 1-69 except 1, 3, 4, 5] *needs to be tested with unittest

    most_popular_balls([(1, 5), (3, 5), (5, 5), (23, 5), (4, 5), (7, 5), (9, 5)])
    [1, 3, 4, 5, 7, 9, 23](possiblities) *needs to be tested with unittest
    """

    luckiest_list = []
    temp_list_of_equals = []
    for num in balls:
        if num[1] > 1 and len(luckiest_list) < 5:
            if len(temp_list_of_equals) == 0 or temp_list_of_equals[0][1] == num[1]:
                temp_list_of_equals.append(num)
            else:
                if len(temp_list_of_equals) + len(luckiest_list) <= 5:
                    luckiest_list += [ball[0] for ball in temp_list_of_equals]
                    temp_list_of_equals.clear()
                    temp_list_of_equals.append(num)
    if len(temp_list_of_equals) > 0:
        temp_list_of_balls = [ball[0] for ball in temp_list_of_equals]
        while len(luckiest_list) < 5:
            if temp_list_of_balls:
                random_pick = random.choice(temp_list_of_balls)
                luckiest_list.append(random_pick)
                temp_list_of_balls.remove(random_pick)
            else:
                return sorted(pick_random_balls(luckiest_list))
        return sorted(luckiest_list)
    else:
        return sorted(pick_random_balls(luckiest_list))		


def most_popular_powerball(powerballs, occurences=None):
    """
    Sorts and possibly randomly selects the highest ranking duplicate 
    powerball.

    >>> most_popular_powerball([(1, 5), (3, 2), (5, 2), (23, 2), (4, 2), (7, 1), (9, 1)], occurences=None)
    1

    >>> most_popular_powerball([(5, 15), (3, 4), (5, 4), (23, 2), (4, 2), (7, 1), (9, 1)], occurences=None)
    5

    >>> most_popular_powerball([(23, 7), (3, 5), (5, 5), (23, 5), (4, 5), (7, 1), (9, 1)], occurences=None)
    23

    most_popular_powerball([(23, 7), (3, 7), (5, 7), (23, 7), (4, 7), (7, 1), (9, 1)], occurences=None)
    23, 3, 5, 23, 4 (possiblities) *needs to be tested with unittest
    """
    popular_powerballs = []
    for ball in powerballs:
        if ball[1] > 1:
            if occurences == None or ball[1] == occurences:
                popular_powerballs.append(ball[0])
                occurences = ball[1]
    if len(popular_powerballs) > 0:
        return random.choice(popular_powerballs)
    return random.choice(range(1, 27))


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
    return ''.join([
        "\n\t\t{d[0]:>2} {d[1]:>2} {d[2]:>2} {d[3]:>2} {d[4]:>2} and Powerball {p[0]:>2}".format(
            d=sorted(ball_list[:5]),
            p=ball_list[5:]
        )
        for ball_list in entries_for_name
        ]
    )

 
def find_all_entries_for_name(full_name, again="", entry="entry is"):
    """
    String formats instance player's selection(s).
    """
    entries_for_name = all_entry_names_and_their_nums[full_name]
    if len(entries_for_name) > 1:
        again = " again"
        entry = "entries are"
    numbers = create_ball_choices_str(entries_for_name)
    return "Successfully submitted{}.\n\tYour {}:{}\n".format(
        again,	
        entry,
        numbers
    )


def list_all_entries_and_participants(instance_participant, entries_str=""):
    """
    String formats alphabetically all players with their corresponding
    entries.
    """	
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
            if 70 <= ratio < 100:
                similar_names.append((name, ratio))
        sorted_similar_names = sorted(
            similar_names, 
            key=operator.itemgetter(1), 
            reverse=True
        )
        for similar in similar_names:
            consider = input("\tDid you mean {}? ('y' to AGREE otherwise press 'Enter'): ".format(
                similar[0]))
            if "y" in consider.casefold():
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
    import doctest
    doctest.testmod()
    controller()
