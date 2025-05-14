from Common import start_head_structure, start_head_inventory, start_head_analysis
def get_sp_cce_status(xl, language, keys):
    type_map = {"no_cce": 0, "with_cce": 0,}
    df = xl.parse("Structures", header=start_head_structure)

    # Check if an SP facility has a CCE and how many there are in that facility
    for i, value in enumerate(df[language.head_cce_is_available]):
        if i in keys.sp_structure_keys and int(value) >= 0:# makes sure that amount is not equals to 0
            type_map["with_cce"] += value

    type_map["no_cce"] = keys.sp_total_structure_keys - type_map["with_cce"]# gets total with no CCE

    return [*type_map.values()]
 
def get_service_point_density(xl, language, keys):
    total_live_births = 0
    df = xl.parse("Analysis_SP",header=start_head_analysis)

    # Get total live births over total SP
    for value in df[language.head_live_births].dropna()[1:]:# Skip the first index to skip the letter
        total_live_births += int(value)
    
    service_point_density = round(total_live_births / keys.sp_total_structure_keys, 2)# Calculate the service point density

    return service_point_density

def get_average_distance(xl, language, keys_to_loop):
    total_distance = 0
    total_facilities = 0
    df = xl.parse("Structures", header=start_head_structure)

    # Get distance to health facility in SP level
    for x in keys_to_loop:
        if str(df[language.head_distance_to_supply][x]) != "nan":# Skip blank cells to not brake the total distance calculation
            clean_num = str(df[language.head_distance_to_supply][x]).replace('\xa0', '')# Remove all non braking space
            if clean_num:
                total_distance += float(clean_num)
                total_facilities += 1

    if total_facilities != 0:# check if not zero to not do 0 division
        average_distance = round(total_distance / total_facilities, 2)# Calculate average distance
    else:
        average_distance = 0
        
    return average_distance

def get_costs(xl, language):
    total_maintenance_cost = 0
    total_energy_cost = 0
    df = xl.parse("Inventory",header=start_head_inventory)

    # Get maintenance cost and energy cost
    for value in df[language.head_maintenance].dropna()[1:]:
        total_maintenance_cost += value
    for value in df[language.head_energy].dropna()[1:]:
        total_energy_cost+= value

    total_cost = round(total_maintenance_cost + total_energy_cost, 2)# Calculate the total cost

    return [round(total_maintenance_cost, 2), round(total_energy_cost, 2), total_cost]

def get_co2_consumption(xl, language, tags):
    functional_keys = []
    kerosene_keys = []
    gas_keys = []
    df = xl.parse("Inventory", header=start_head_inventory)

    # get all functional equipments
    for i, value in enumerate(df[language.head_operational_status]):
        if value == tags.functional_tag:
            functional_keys.append(i)
            
    # get gas and kerosine keys
    for i, value in enumerate(df[language.head_source_of_energy]):
        if tags.kerosene_tag in str(value):
            kerosene_keys.append(i)
        elif tags.gas_tag in str(value):
            gas_keys.append(i)

    # merge keys
    kerosene_f_keys = list(set(functional_keys) & set(kerosene_keys))
    gas_f_keys = list(set(functional_keys) & set(gas_keys))
    total_kerosene_co2 = 0
    total_gas_co2 = 0

    # get a vales of the co2 production of each functioning equipment
    for x in kerosene_f_keys:
        total_kerosene_co2 += float(df["Unnamed: 61"][x])
    for x in gas_f_keys:
        total_gas_co2 += float(df["Unnamed: 61"][x])

    total_co2_produced = total_kerosene_co2 + total_gas_co2

    return [round(total_kerosene_co2, 2), round(total_gas_co2, 2), round(total_co2_produced, 2)]  