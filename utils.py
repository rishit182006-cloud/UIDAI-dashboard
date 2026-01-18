import pandas as pd

def load_data():
    enrol = pd.read_csv("data/enrolment.csv")
    bio = pd.read_csv("data/biometric.csv")
    demo = pd.read_csv("data/demographic.csv")

    enrol['date'] = pd.to_datetime(enrol['date'], errors='coerce')
    return enrol, bio, demo