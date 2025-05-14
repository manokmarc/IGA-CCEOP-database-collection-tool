import regex as re
from threading import Thread

class Language:# class to determine what language system to use
    def __init__(self, language):
        # frecnh naming scheme
        if language == "français":
            self.head_supply_levels = "Niveaux d'approvisionnement"
            self.head_operational_status = "Statut Opérationnel"
            self.head_pq_status = "PQ_status"
            self.head_source_of_energy = "Source d'énergie"
            self.head_cce_is_available = "ECF disponible (+5°C)"
            self.head_live_births = "Naissances vivantes"
            self.head_distance_to_supply = "Distance d'approvisionnement"
            self.head_maintenance = "Maintenance"
            self.head_energy = "énergie"
            self.head_type_of_equipment = "Type équipement"
            self.head_store = "Dépôt"
            self.head_supply_interval = "interval d'approv., mois"
            self.head_capacity_required = "Capacité requise à +5°C, litres"

        # english naming scheme
        elif language == "english":
            self.head_supply_levels = "Supply Levels"
            self.head_operational_status = "Operational status"
            self.head_pq_status = "PQ_status"
            self.head_source_of_energy = "Source of energy"
            self.head_cce_is_available = "CCE is available (+5°C)"
            self.head_live_births = "Live births"
            self.head_distance_to_supply = "Distance to supply"
            self.head_maintenance = "Maintenance"
            self.head_energy = "energy"
            self.head_type_of_equipment = "Type of equipment"
            self.head_store = "Store"
            self.head_supply_interval = "supply interval, months" #supply intervalle, months
            self.head_capacity_required = "Capacity required at +5°C, litres"

class Tags:# class to determine what tags are used
    def __init__(self, xl, head_store):
            # Get facility level tag
            df = xl.parse("Prog", header=25)
            self.sp_tag = re.sub(r'[0-9]+', '', str(df[head_store][0]))# Remove all possible numbers from the level name
            self.ld_tag = re.sub(r'[0-9]+', '', str(df[head_store][1]))
            self.sn_tag = re.sub(r'[0-9]+', '', str(df[head_store][2]))
            self.pr_tag = re.sub(r'[0-9]+', '', str(df[head_store][4]))

            self.snx_tag = re.sub(r'[0-9]+', '', str(df[head_store][3])) # for the SN2 level tags if there is
            if self.snx_tag == "" or self.snx_tag == " " or self.snx_tag == "nan":# if tag is blank make it unidenifiable
                self.snx_tag = "qdijdqwiondqnqkwnwejnqwel"# random words

            # Get refrigerator tag
            df = xl.parse("Prog", header=6)
            self.refrigerator_tag = df["Unnamed: 5"][0]

            # Get functionality tag
            self.functional_tag = df["Unnamed: 8"][0]
            self.reapair_tag = df["Unnamed: 8"][1]
            self.non_functional_tag = df["Unnamed: 8"][2]

            # Get frezer tag
            df = xl.parse("Prog", header=7)
            self.frezer_tag = df[self.refrigerator_tag][0]

            # Get power type tag
            df = xl.parse("Prog", header=13)
            self.electricity_tag = df["Unnamed: 5"][0]
            self.solar_tag = df["Unnamed: 5"][1]
            self.gas_tag  = df["Unnamed: 5"][2]
            self.kerosene_tag  = df["Unnamed: 5"][3]

class Keys:# class to determine the keys in the xl doc
     def __init__(self, xl, start_head_structure, start_head_inventory, language, tags):
        self.ld_structure_keys = []
        self.sp_structure_keys = []
        def get_structure_keys():# gets the index of the facility level in the structure sheet
            df = xl.parse("Structures", header=start_head_structure)

            for i, value in enumerate(df[language.head_supply_levels]):
                modified_value = re.sub(r'[0-9]+', '', str(value))# Remove all possible numbers from the level name
                
                if modified_value == tags.ld_tag:# LD
                    self.ld_structure_keys.append(i)
                if modified_value == tags.sp_tag:# SP
                    self.sp_structure_keys.append(i)
        get_structure_keys()

        self.ld_inventory_keys = []
        self.sp_inventory_keys = []
        def get_inventory_keys():# gets the index of the facility level in the inventory sheet
            df = xl.parse("Inventory", header=start_head_inventory)
            
            for i, value in enumerate(df[language.head_supply_levels]):
                modified_value = re.sub(r'[0-9]+', '', str(value))# Remove all possible numbers from the level name

                if modified_value == tags.ld_tag:# LD
                    self.ld_inventory_keys.append(i)
                elif modified_value == tags.sp_tag:# SP
                    self.sp_inventory_keys.append(i)
        get_inventory_keys()

        self.cce_keys = []
        def get_cce_keys():# gets the index for the ref and frezer CCE type
            df = xl.parse("Inventory", header=start_head_inventory)

            for i, value in enumerate(df[language.head_type_of_equipment]):
                if value == tags.refrigerator_tag or value == tags.frezer_tag:
                    self.cce_keys.append(i)
        get_cce_keys()

        self.ld_supply_interval_keys = []
        self.sp_supply_interval_keys = []
        def get_supply_interval_keys():# gets the index for supply intervals
            df = xl.parse("Structures", header=start_head_structure)

            for x in self.ld_structure_keys:# LD
                if str(df[language.head_supply_interval][x]) != "nan":# ignore blank values
                    self.ld_supply_interval_keys.append(x)

            for x in self.sp_structure_keys:# SP
                if str(df[language.head_supply_interval][x]) != "nan":# ignore blank values
                    self.sp_supply_interval_keys.append(x)
        get_supply_interval_keys()

        self.ld_cce_keys = list(set(self.cce_keys) & set(self.ld_inventory_keys))
        self.sp_cce_keys = list(set(self.cce_keys) & set(self.sp_inventory_keys))

        self.ld_f_cce_keys = []
        self.sp_f_cce_keys = []
        def get_cce_functionality():
            df = xl.parse("Inventory", header=start_head_inventory)

            for x in self.ld_cce_keys:# LD
                if df[language.head_operational_status][x] == tags.functional_tag:
                    self.ld_f_cce_keys.append(x)# get all functional indexes

            for x in self.sp_cce_keys:# SP
                if df[language.head_operational_status][x] == tags.functional_tag:
                    self.sp_f_cce_keys.append(x)# get all functional indexes
        get_cce_functionality()

        # Set total amounts
        self.sp_total_structure_keys = len(self.sp_structure_keys)
        self.ld_total_structure_keys = len(self.ld_structure_keys)
        self.ld_total_cce_keys =len(self.ld_cce_keys)
        self.sp_total_cce_keys = len(self.sp_cce_keys)
        self.ld_total_f_cce_keys = len(self.ld_f_cce_keys)
        self.sp_total_f_cce_keys = len(self.sp_f_cce_keys)


class CustomThread(Thread): # Thread class that return the values of a function when finished running
    def __init__(self, group= None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._retrun = None
    
    # Override
    def run(self): # set return value to the given function return value
        if self._target is not None:
            self._retrun = self._target(*self._args, **self._kwargs)
    
    # Override
    def join(self): # return the value when thread is finished
        Thread.join(self)
        return self._retrun