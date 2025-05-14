from Common import start_head_structure, start_head_inventory, turn_to_persent

def get_cce_functionality(xl, language, tags, keys_to_loop, total_keys):
    type_map = {tags.functional_tag : 0, tags.non_functional_tag: 0}
    df = xl.parse("Inventory", header=start_head_inventory)

    # Get if CCE is functional or not
    for x in keys_to_loop:
        if df[language.head_operational_status][x] == tags.functional_tag:
            type_map[tags.functional_tag] += 1
        elif df[language.head_operational_status][x] == tags.non_functional_tag or df[language.head_operational_status][x] == tags.reapair_tag:# Needs reapair is also non fuctional
            type_map[tags.non_functional_tag] += 1

    # Turn to persentage
    type_map = turn_to_persent(type_map, total_keys)

    return [*type_map.values()]

def get_storage_capasity(xl, langauge, keys_to_loop):
    head_index = 0 # Index of available cold storage
    tag_available_cold_storage = "Unnamed: "# Set unamed header

    type_map = {"ld_sufficent": 0, "ld_insufficent": 0}
    df = xl.parse("Structures", header=start_head_structure)

    # Gets the head number for the first instance of available cold storage (we do this because there is 2 headers with the name of avaiable cold storage)
    for i, head in enumerate(df):
        if head == langauge.head_cce_is_available:
            head_index = i + 1
    tag_available_cold_storage += str(head_index)# add the index number to the unamed header

    # Check is storage capasity is sufficent
    for x in keys_to_loop:
        if df[tag_available_cold_storage][x] > df[langauge.head_capacity_required][x]:
            type_map["ld_sufficent"] += 1
        else:
            type_map["ld_insufficent"] += 1

    # Turn values to persentage
    turn_to_persent(type_map, sum(type_map.values()))

    return[*type_map.values()]

def get_pq_status(xl, language, keys_to_loop):
    type_map = {"pqs_refr" : 0, "pis_refr": 0, "non_pq": 0}
    df = xl.parse("Inventory", header=start_head_inventory)

    # Checks if ref and frezer CCE has a status of PQ, PI OR non
    # Get status
    for x in keys_to_loop:
        if "non" in str(df[language.head_pq_status][x]).lower():
            type_map["non_pq"] += 1
        elif "pq" in str(df[language.head_pq_status][x]).lower():
            type_map["pqs_refr"] += 1
        elif "pi" in str(df[language.head_pq_status][x]).lower():
            type_map["pis_refr"] += 1
 
    # Turn to persentage
    type_map = turn_to_persent(type_map, sum(type_map.values()))

    return [*type_map.values()]
