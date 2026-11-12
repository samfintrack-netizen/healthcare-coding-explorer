import pandas as pd

bene = pd.read_csv("data_raw/DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv", nrows=3)
print("BENEFICIARY columns (", len(bene.columns), "):")
print(list(bene.columns))
print()
carrier = pd.read_csv("data_raw/DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.csv", nrows=3)
print("CARRIER columns (", len(carrier.columns), "):")
print(list(carrier.columns))
