# Import Uvicorn & the necessary modules from FastAPI
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
# Import other necessary packages
from dotenv import load_dotenv
import os
import json
from mlplatformutils.core.pandascoreutils import read_from_delta_as_pandas
# Load the environment variables from the .env file into the application
load_dotenv() 
# Initialize the FastAPI application
app = FastAPI()
SOURCE_STORAGE_ACCOUNT_VALUE = os.environ.get("SOURCE_STORAGE_ACCOUNT_VALUE")
SOURCE_READ_SPN_VALUE = os.environ.get("SOURCE_READ_SPN_VALUE")
SOURCE_READ_SPNKEY_VALUE = os.environ.get("SOURCE_READ_SPNKEY_VALUE")
tenant_id = os.environ.get("tenant_id")
AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH = os.environ.get("AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH")

df = read_from_delta_as_pandas(
                                SOURCE_STORAGE_ACCOUNT_VALUE,\
                                SOURCE_READ_SPN_VALUE,\
                                SOURCE_READ_SPNKEY_VALUE,\
                                tenant_id,\
                                AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH)
class DataLakeReader:
    def __init__(self, RowId):
        self.RowId = RowId

    def readQuery(self, df):
        df_filtered = df.loc[df['RowId'] == self.RowId]
        jsondf = df_filtered.to_json(orient='records')
        return jsondf

# Create the POST endpoint with path '/readQuery'
@app.post("/readQuery")
async def datalake(RowId: int):
    readerObj = DataLakeReader(RowId)
    jsondf = readerObj.readQuery(df)
    return jsondf

if __name__ == '__main__':
    app.run(debug=True)
