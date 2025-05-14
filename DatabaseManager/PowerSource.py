from Common import start_head_inventory, turn_to_persent

def get_power_source(xl, language, tags, keys_to_loop, total_keys):
    type_map_ld = {tags.electricity_tag: 0, tags.solar_tag: 0, tags.kerosene_tag: 0, tags.gas_tag : 0}
    df = xl.parse("Inventory", header=start_head_inventory)

    # This method takes into acount the hybrid power sources
    # Get power source type
    for x in keys_to_loop: 
        if tags.kerosene_tag in str(df[language.head_source_of_energy][x]):
            type_map_ld[tags.kerosene_tag] += 1
        elif tags.gas_tag in str(df[language.head_source_of_energy][x]):
            type_map_ld[tags.gas_tag] += 1
        elif tags.electricity_tag in str(df[language.head_source_of_energy][x]):
            type_map_ld[tags.electricity_tag] += 1
        elif tags.solar_tag in str(df[language.head_source_of_energy][x]):
            type_map_ld[tags.solar_tag] += 1

    # Turn to persentage
    type_map_ld = turn_to_persent(type_map_ld, total_keys)
        
    return [*type_map_ld.values()]
