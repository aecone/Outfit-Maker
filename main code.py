import json
import random
import itertools
from os import path

"""I wanted to have a program that would formulate simple warm weather outfits for a person every week for a duration of 
a month (5 weeks (I added some days)). User would just have to input data about what clothing pieces they have and which
week's outfits they want. I used json files to store the info so it can be reused for remaining weeks"""


# Since the program can do several operations, I needed just one question to determine which operation the user
# wants, which would be to input their clothing data if they are new or if they want their weekly outfits made (only
# for those who already input their data).
def main():
    acceptable_responses = ["YES", " YES", "YES ", "NO", " NO", "NO "]
    user_answer = raw_input(
        "\nWelcome! This is your BASIC spring/summer outfit maker that will create weekly clothing looks for a "
        "duration of one month. \n \nDo you already have a saved closet here? YES or NO: ").upper()
    while user_answer not in acceptable_responses:
        user_answer = raw_input("Only YES or NO answers. Try again: ").upper()
    make_closet_or_get_outfits(user_answer)


def make_closet_or_get_outfits(user_answer):
    no = ["NO", " NO", "NO "]
    yes = ["YES", " YES", "YES "]
    if user_answer in no:
        get_closet()
    if user_answer in yes:
        name = raw_input(" \nWhat is the EXACT name of the closet you made: ")
        full_file_name = name + ":"
        valid_file_verification(full_file_name)


# Made short and long versions of tops and bottoms to make it easier for the user to categorize their clothes, but
# the length of clothing doesn't matter, so it's really just overall tops and bottoms needed
def get_closet():
    clothing_categories = ["Short-Sleeved Top", "Long-Sleeved Top", "Short Bottom", "Long Bottom"]
    print('\n--------------------------------------------------------------'
          '\nEach outfit only consists of 1 top and 1 bottom. Also, there will be 2 outwear options given per '
          'week. \nList out the clothes you will be wearing during spring/summer season and make sure to specify each '
          'piece so you can recognize it easily. \nI recommend mentioning brand names, colors, or features of the '
          'clothing to help identify the piece. \nYou will have to update your closet data every month, so whenever '
          'you want to change your closet, say "NO" at the beginning of the program or you can say "YES" if '
          '\nyou want to reuse the exact same ordering of the outfits made before.'
          '\n \nPlease be ready to categorize all your clothes with these titles: \n - Short Sleeves Tops '
          '(Tees, Tanks, etc)\n - Long Sleeve Tops (Blouses, Button Downs, Sweaters, etc) '
          '\n - Short Bottoms (Shorts, Skirts, etc) \n - Long Bottoms (Jeans, Trousers, etc) '
          '\n - Outerwear (Jackets, Blazers, Cardigans, Hoodies, Coats) \n \nPress ENTER to move to next category'
          '\n \nYOUR CLOSET:')
    tops = get_grouped_clothing(clothing_categories[0], clothing_categories[1])
    bottoms = get_grouped_clothing(clothing_categories[2], clothing_categories[3])
    outerwears = get_outerwear()
    organize_clothing_file(tops, bottoms, outerwears)


def get_grouped_clothing(clothing1, clothing2):
    grouped_clothes = []
    while True:
        input1 = raw_input("{}: ".format(clothing1))
        if input1 == "":
            break
        grouped_clothes.append(input1)
    print("")
    while True:
        input2 = raw_input("{}: ".format(clothing2))
        if input2 == "":
            break
        grouped_clothes.append(input2)
    print ("Your " + clothing1 + " and " + clothing2 + " closet is: " + "\n" + str(grouped_clothes) + "\n")
    return grouped_clothes


def get_outerwear():
    outer_list = []
    while True:
        outerwear = raw_input("Outerwears (at least 2): ")
        if outerwear == "":
            break
        outer_list.append(outerwear)
    while len(outer_list) < 2:
        if outerwear == "":
            outerwear = raw_input("Please add at least one more outerwear: ")
            outer_list.append(outerwear)
    print ("Your Outerwear closet is: \n" + str(outer_list))
    return outer_list


# Needed to randomize and make all possible combinations for tops + bottoms. Made dict for tops & bottoms and another
# for outerwear and combined it, so you can access it easier when displaying the info separately in the file.
def organize_clothing_file(tops, bottoms, outerwears):
    tops_bottoms_dict = {}
    outer_dict = {}
    combo_list = make_combinations(tops, bottoms)
    random.shuffle(combo_list)
    random.shuffle(outerwears)
    tops_bottoms_dict["tops_bottoms"] = combo_list
    outer_dict["outerwear"] = outerwears
    ult_list = outer_dict.copy()
    ult_list.update(tops_bottoms_dict)
    make_json(ult_list)


# Found a code online to make combinations from two lists. I noticed that if the length of the tops list was less than
# the bottoms list, there was an error with the code, so I had to create two different versions of the code to ensure
# that the combinations would be made.
def make_combinations(tops, bottoms):
    proxy_list = []
    combo_list = []
    if len(tops) >= len(bottoms):
        permutation = itertools.permutations(tops, len(bottoms))
        for combination in permutation:
            zipped = zip(combination, bottoms)
            proxy_list.append(list(zipped))
        # Needed to rid brackets
        fixed_list = list(itertools.chain.from_iterable(proxy_list))
    else:
        permutation = itertools.permutations(bottoms, len(tops))
        for combination in permutation:
            zipped = zip(combination, tops)
            proxy_list.append(list(zipped))
        # Needed to rid brackets
        fixed_list = list(itertools.chain.from_iterable(proxy_list))
    # Rid any repeated combos from fixed_list
    [combo_list.append(x) for x in fixed_list if x not in combo_list]
    set_list_length(combo_list)
    return combo_list


# There had to be enough amount of combinations to meet 5 weeks of potential outfits, so the list length had to be 35.
# Additional combinations were added to the main list by creating new lists that each had a different order of the
# combinations. The amount of new lists created depended on how much clothing the user submitted to their "closet."
def set_list_length(combo_list):
    print("")
    shuffled_list_names = ["list1", "list2", "list3", "list4", "list5"]
    num = ((35.0 - float(len(combo_list))) / float(len(combo_list)))
    num += (1 if num - int(num) > 0 else 0)
    for i in range(int(num)):
        shuffled_list_names[i] = list(combo_list)
        random.shuffle(shuffled_list_names[i])
        for combo in shuffled_list_names[i]:
            combo_list.append(combo)
            if len(combo_list) > 35:
                break


# After file is made, user should be able to get outfits (optional)
def make_json(ult_list):
    acceptable_responses = ["YES", " YES", "YES ", "NO", " NO", "NO "]
    name = raw_input("Name your closet (please remember for future reference): ").upper()
    closet_file = name + ":"
    with open("{}:".format(name), 'w') as f:
        json.dump(ult_list, f, indent=4)
    user_answer = raw_input("\nDo you want this week's outfits created now? YES or NO: ").upper()
    while user_answer not in acceptable_responses:
        user_answer = raw_input("Only YES or NO answers. Try again: ").upper()
    stop_or_get_outfits(closet_file, user_answer)


def stop_or_get_outfits(closet_file, user_answer):
    no = ["NO", " NO", "NO "]
    yes = ["YES", " YES", "YES "]
    if user_answer in no:
        print("\nSee you next time! :)")
        exit()
    if user_answer in yes:
        open_json_and_ask_week_num(closet_file)


def valid_file_verification(closet_file):
    while str(path.isfile(closet_file)) == "False":
        name = raw_input("No file was found. Retype the file name: ")
        closet_file = name + ":"
    open_json_and_ask_week_num(closet_file)


def open_json_and_ask_week_num(closet_file):
    week_numbers = ["1", "2", "3", "4", "5"]
    week = raw_input("\n" + "What week are you in? 1-5 only: ")
    with open(closet_file) as f:
        opened_file = json.load(f)
    while week not in week_numbers:
        week = raw_input("You can only write numbers 1-5. Please try again:")
    display_outfits(opened_file, week)


# week 1 = combos 0-6, week 2 = combos 7-13 .... based on given week number each additional week would have
# 7 more days
def display_outfits(opened_file, week_num):
    numbered_outfits = ["Outfit 1: ", "Outfit 2: ", "Outfit 3: ", "Outfit 4: ", "Outfit 5: ", "Outfit 6: ",
                        "Outfit 7: "]
    additional_days = [0, 7, 14, 21, 28]
    print("\n"
          "------------------------------")
    for i in range(7):
        one_outfit = str(numbered_outfits[i]) + str(
            ", ".join(opened_file["tops_bottoms"][i + additional_days[int(week_num) - 1]]))
        print (one_outfit)
    print ("\n" + "2 Outerwears: " + str(", ".join(random.sample(opened_file["outerwear"], 2))) + "\n")


if __name__ == "__main__":
    main()
