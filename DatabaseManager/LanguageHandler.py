# chekcs if language is french or english
def get_language_scheme(xl):
    df = xl.parse("Cover", header=6)# Gets the cover sheet
    language = df["Unnamed: 3"][0].lower()# Get the language of the exel file

    return language