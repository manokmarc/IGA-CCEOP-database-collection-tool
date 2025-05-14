from InputFile import all_exel_files
from LanguageHandler import get_language_scheme
from Classes import Language, Tags, Keys, CustomThread
from Common import start_head_structure, start_head_inventory
import AllFacilities
import CCEData
import PowerSource
import GeneralData

all_country_names = []
all_country_data = []

def get_country_name(xl):
    # get name of country
    df = xl.parse("Cover", header=8)
    country_name = df["Unnamed: 3"][0]

    return country_name

def calculate_data(xl):
    country_data = []

    # set dataframe
    df = xl.parse("Cover", header=6)

    # set up classes
    language = Language(get_language_scheme(xl))
    tags = Tags(xl, language.head_store)
    keys = Keys(xl, start_head_structure, start_head_inventory, language, tags)

    # Get values
    year = df["Unnamed: 5"][0]
    thread1 = CustomThread(target=AllFacilities.get_facility_type, args=(xl, language, tags))
    thread2 = CustomThread(target=CCEData.get_cce_functionality, args=(xl, language, tags, keys.ld_cce_keys, keys.ld_total_cce_keys))
    thread3 = CustomThread(target=CCEData.get_cce_functionality, args=(xl, language, tags, keys.sp_cce_keys, keys.sp_total_cce_keys))
    thread4 = CustomThread(target=CCEData.get_storage_capasity, args=(xl, language, keys.ld_supply_interval_keys))
    thread5 = CustomThread(target=CCEData.get_storage_capasity, args=(xl, language, keys.sp_supply_interval_keys))
    thread6 = CustomThread(target=CCEData.get_pq_status, args=(xl, language, keys.ld_cce_keys))
    thread7 = CustomThread(target=CCEData.get_pq_status, args=(xl, language, keys.sp_cce_keys))
    thread8 = CustomThread(target=PowerSource.get_power_source, args=(xl, language, tags, keys.ld_f_cce_keys, keys.ld_total_f_cce_keys))
    thread9 = CustomThread(target=PowerSource.get_power_source, args=(xl, language, tags, keys.sp_f_cce_keys, keys.sp_total_f_cce_keys))
    thread10 = CustomThread(target=GeneralData.get_sp_cce_status, args=(xl, language, keys))
    thread11 = CustomThread(target=GeneralData.get_service_point_density, args=(xl, language, keys))
    thread12 = CustomThread(target=GeneralData.get_average_distance, args=(xl, language, keys.sp_structure_keys))
    thread13 = CustomThread(target=GeneralData.get_costs, args=(xl, language))
    thread14 = CustomThread(target=GeneralData.get_co2_consumption, args=(xl, language, tags))
    
    # Start multi threading
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()
    thread11.start()
    thread12.start()
    thread13.start()
    thread14.start()
    
    # Set Collected data
    facility_type_count = thread1.join()
    ld_cce_functionality_persentage = thread2.join()
    sp_cce_functionality_persentage = thread3.join()
    ld_suficient_storage_capasity_persentage = thread4.join()
    sp_suficient_storage_capasity_persentage = thread5.join()
    ld_cce_pq_status_persentage = thread6.join()
    sp_cce_pq_status_persentage = thread7.join()
    ld_power_source_persentage = thread8.join()
    sp_power_source_persentage = thread9.join()
    sp_with_cce_persentage = thread10.join()
    service_point_density = thread11.join()
    average_distance = thread12.join()
    total_costs = thread13.join()
    total_co2_produced = thread14.join()
    
    # facility_type_count = AllFacilities.get_facility_type(xl, language, tags) # [PR, SN, LD, SP]
    # ld_cce_functionality_persentage = CCEData.get_cce_functionality(xl, language, tags, keys_to_loop=keys.ld_cce_keys, total_keys=keys.ld_total_cce_keys)
    # sp_cce_functionality_persentage = CCEData.get_cce_functionality(xl, language, tags, keys_to_loop=keys.sp_cce_keys, total_keys=keys.sp_total_cce_keys)
    # ld_suficient_storage_capasity_persentage = CCEData.get_storage_capasity(xl, language, keys_to_loop=keys.ld_supply_interval_keys)
    # sp_suficient_storage_capasity_persentage = CCEData.get_storage_capasity(xl, language, keys_to_loop=keys.sp_supply_interval_keys)
    # ld_cce_pq_status_persentage = CCEData.get_pq_status(xl, language, keys_to_loop=keys.ld_cce_keys)
    # sp_cce_pq_status_persentage = CCEData.get_pq_status(xl, language, keys_to_loop=keys.sp_cce_keys)
    # ld_power_source_persentage = PowerSource.get_power_source(xl, language, tags, keys_to_loop=keys.ld_f_cce_keys, total_keys=keys.ld_total_f_cce_keys)
    # sp_power_source_persentage = PowerSource.get_power_source(xl, language, tags, keys_to_loop=keys.sp_f_cce_keys, total_keys=keys.sp_total_f_cce_keys)
    # sp_with_cce_persentage = GeneralData.get_sp_cce_status(xl, language, keys)
    # service_point_density = GeneralData.get_service_point_density(xl, language, keys)
    # average_distance = GeneralData.get_average_distance(xl, language, keys_to_loop=keys.sp_structure_keys)
    # total_costs = GeneralData.get_costs(xl, language) 
    # total_co2_produced = GeneralData.get_co2_consumption(xl, language, tags)
    
    # Compile the data gathered
    def import_data():
        country_data.append(year)
        for x in facility_type_count:
            country_data.append(x)
        for x in ld_cce_functionality_persentage:
            country_data.append(x)
        for x in ld_suficient_storage_capasity_persentage:
            country_data.append(x)
        for x in ld_cce_pq_status_persentage:
            country_data.append(x)
        for x in ld_power_source_persentage:
            country_data.append(x)
        for x in sp_with_cce_persentage:
            country_data.append(x)
        for x in sp_cce_functionality_persentage:
            country_data.append(x)
        for x in sp_suficient_storage_capasity_persentage:
            country_data.append(x)
        for x in sp_cce_pq_status_persentage:
            country_data.append(x)
        for x in sp_power_source_persentage :
            country_data.append(x)
        country_data.append(service_point_density)
        country_data.append(average_distance)
        for x in total_costs:
            country_data.append(x)
        for x in total_co2_produced:
            country_data.append(x)
    import_data()

    # output contry names and country data
    return country_data

for xl in all_exel_files:
    all_country_names.append(get_country_name(xl))
    all_country_data.append(calculate_data(xl))
    print(get_country_name(xl))