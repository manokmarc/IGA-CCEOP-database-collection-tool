import regex as re
from Common import start_head_structure

def get_facility_type(xl, language, tags):
    type_map = {tags.pr_tag: 0, tags.sn_tag: 0, tags.ld_tag: 0, tags.sp_tag: 0}
    df = xl.parse("Structures", header=start_head_structure)

    # Gets the level of each facility
    for value in df[language.head_supply_levels]:
        modified_value = re.sub(r'[0-9]+', '', str(value))# remove all possible numbers from the string
        if modified_value in type_map:
            type_map[modified_value] += 1
        elif modified_value == tags.snx_tag:# check if value is equal to senx tag
            type_map[tags.sn_tag] += 1

    return [*type_map.values()]

