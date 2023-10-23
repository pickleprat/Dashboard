import pandas as pd 

denormalized = pd.read_csv("streamlit/data/denormalized.csv")
modeldata = pd.read_csv("streamlit/data/modeled_data.csv")

denormalized["amount_predicted"] = modeldata["amount_predicted"]
denormalized.to_csv("streamlit/data/denormalized.csv", index=False)
