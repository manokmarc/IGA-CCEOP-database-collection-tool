# Unique header row for each file
start_head_structure = 7
start_head_inventory = 8
start_head_analysis = 6

def turn_to_persent(dic, total):
    # Turns the total values to a persentage
    for x in dic:
        dic[x] = round((dic[x] / total) * 100, 2)

    return dic