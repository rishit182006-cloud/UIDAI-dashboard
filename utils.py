import pandas as pd

def load_data():
    enrol = pd.read_csv("data/enrolment_merged_cleaned.csv")
    bio = pd.read_csv("data/biometric.csv")
    demo = pd.read_csv("data/demographic.csv")

    enrol['date'] = pd.to_datetime(enrol['date'], format="%d-%m-%Y", errors='coerce')
    return enrol, bio, demo

def load_birth_data():
    # Keep the existing birth data logic but also add a way to load population data
    data = {
        "state": [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
            "Chhattisgarh", "Goa", "Gujarat", "Haryana",
            "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
            "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
            "Mizoram", "Nagaland", "Odisha", "Punjab",
            "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
            "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
            "Andaman and Nicobar Islands", "Chandigarh",
            "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
            "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
        ],
        "total_births": [
            750000, 45000, 1000000, 3070000, 800000, 35000, 1180000, 600000,
            90000, 970000, 1040000, 440000, 1990000, 1920000, 50000, 70000,
            40000, 35000, 730000, 400000, 1800000, 12000, 940000, 700000,
            120000, 5440000, 180000, 1390000, 8000, 25000, 60000, 500000,
            300000, 18000, 2000, 28000
        ]
    }
    return pd.DataFrame(data)

def load_population_data():
    """Loads the state-wise population data"""
    df = pd.read_csv("data/state_population.csv")
    return df


def normalize_state_names(df):
    """
    Ensures state names are leading/trailing whitespace free and 
    consistent with the govt birth data mapping.
    """
    # Standardize column name to lowercase 'state'
    if 'State' in df.columns:
        df.rename(columns={'State': 'state'}, inplace=True)

    mapping = {
        "Andaman & Nicobar Islands": "Andaman and Nicobar Islands",
        "Pondicherry": "Puducherry",
        "Nct Delhi": "Delhi",
        "NCT Delhi": "Delhi"
    }

    if 'state' in df.columns:
        df['state'] = df['state'].str.strip()
        df['state'] = df['state'].replace(mapping)
        # Handle title case but keep specific UT names correct
        df['state'] = df['state'].str.title()
        
        # Consistent mapping back to the standard names used in the birth/pop data
        final_mapping = {
            "Andaman And Nicobar Islands": "Andaman and Nicobar Islands",
            "Dadra And Nagar Haveli And Daman And Diu": "Dadra and Nagar Haveli and Daman and Diu"
        }
        df['state'] = df['state'].replace(final_mapping)
    return df
