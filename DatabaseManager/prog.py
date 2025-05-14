import pandas as pd
from collections import defaultdict

exel_file = 'DatabaseManager/CCE_InventoryGapAnalysis_Afghanistan_01022023_Review.xlsx'
xl = pd.ExcelFile(exel_file)

sp_keys = []
ld_keys = []
sp_keys_struc = []

# Get keys from inventory Sheet
def get_keys():
    type_map = ["LD","SP"]
    df = xl.parse("Inventory", header=[8], index_col=[])

    for i, value in enumerate(df["Supply Levels"].values.tolist()):
        if str(value).upper() in type_map:
            if value.upper() == "LD":
                ld_keys.append(i)
            if value.upper() == "SP":
                sp_keys.append(i)

# Get amount of facility type
def get_facility():
    type_map = {"LD": 0, "PR": 0, "SN": 0, "SP": 0}
    df = xl.parse("Structures", header=[7], index_col=[])

    for i, value in enumerate(df["Supply Levels"].values.tolist()):
        if str(value).upper() in type_map:
            if value.upper() == "SP":
                sp_keys_struc.append(i)
            type_map[value.upper()] += 1

    print("facility type", type_map)
    return type_map

# Get functional facilities with CCE
def get_functionality():
    type_map_ld = defaultdict(int)
    type_map_sp = defaultdict(int)

    df = xl.parse("Inventory", header=[8], index_col=[])

    for i in ld_keys:
        type_map_ld[df["Operational status"][i]] += 1
    for i in sp_keys:
        type_map_sp[df["Operational status"][i]] += 1

    print("SP functionality", type_map_sp)
    print("LD functionality", type_map_ld)
    return [type_map_ld, type_map_sp]

# Get amount of power source
def get_power_source():
    type_map_ld = defaultdict(int)
    type_map_sp = defaultdict(int)
    df = xl.parse("Inventory", header=[8], index_col=[])

    for i in ld_keys:
        type_map_ld[df["Source of energy"][i]] += 1
    for i in sp_keys:
        type_map_sp[df["Source of energy"][i]] += 1

    print("SP power source", type_map_sp)
    print("LD power source", type_map_ld)
    return [type_map_ld, type_map_sp]

# Get amount of CCE type
def get_cce_status():
    type_map = {"with_cce": 0, "no_cce": 0}

    df = xl.parse("Structures", header=[7], index_col=[])

    for i, value in enumerate(df["CCE is available (+5°C)"].values.tolist()):
        if i in sp_keys_struc:
            type_map["with_cce"] += value

    type_map["no_cce"] = len(sp_keys_struc) - type_map["with_cce"]

    print(type_map)
    return type_map

# Get service pointdensity
def get_service_pointdensity():
    provinces = set()
    total_live_births = 0
    service_point_dencity = {"service point dencity": 0}

    df = xl.parse("Structures",header=[7], index_col=[])

    for i in sp_keys_struc:
        provinces.add(df["Province"][i].lower())
    
    df = xl.parse("Analysis_SP",header=[6], index_col=[])

    for value in df["Live births"].dropna().values.tolist()[1:]:
        if value != 0:
            total_live_births += value
            
    service_point_dencity["service point dencity"] = round(total_live_births,2) / len(sp_keys_struc)

    print(service_point_dencity)
    return service_point_dencity

# Get average helth facility supply distance
def get_distance():
    total_count = 0
    total_sum = 0
    avarage_distance = {"average distance": 0}

    df = xl.parse("Structures", header=[7], index_col=[])

    for i, value in enumerate(df["Distance to supply"].values.tolist()):
        if i in sp_keys_struc and value:
            total_count += 1
            total_sum += int(value)

    avarage_distance["avarage distance"] = total_sum / total_count

    print(avarage_distance)
    return avarage_distance

get_keys()
get_facility()


country_data = {**get_facility(),
                **get_functionality(),
                **get_power_source(),
                **get_cce_status(),
                **get_functionality(),
                **get_power_source(),
                **get_service_pointdensity(),
                **get_distance()}

df = pd.DataFrame(country_data, index=["Afganistan"])
with pd.ExcelWriter('C:\\Users\\marcm\\Downloads\\Database.xlsx') as writer:
    df.to_excel(writer, sheet_name="Sheet_1")