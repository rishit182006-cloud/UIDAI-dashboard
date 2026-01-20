import pandas as pd
try:
    bio = pd.read_csv("data/biometric.csv")
    print("Biometric Columns FULL LIST:", ", ".join(bio.columns.tolist()))
    
    demo = pd.read_csv("data/demographic.csv")
    print("Demographic Columns FULL LIST:", ", ".join(demo.columns.tolist()))
except Exception as e:
    print(e)

