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
# Create a class to load the Model from MLFLOW Registry & use it for prediction
class DataLakeReader:
    def __init__(self,RowId):
        """
        To initalize the model Details
        """
        self.SOURCE_STORAGE_ACCOUNT_VALUE = os.environ.get("SOURCE_STORAGE_ACCOUNT_VALUE")
        self.SOURCE_READ_SPN_VALUE = os.environ.get("SOURCE_READ_SPN_VALUE")
        self.SOURCE_READ_SPNKEY_VALUE = os.environ.get("SOURCE_READ_SPNKEY_VALUE")
        self.tenant_id = os.environ.get("tenant_id")
        self.AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH = os.environ.get("AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH")
        self.RowId = RowId

    def readQuery(self):
        df = read_from_delta_as_pandas(
                                       self.SOURCE_STORAGE_ACCOUNT_VALUE,\
                                       self.SOURCE_READ_SPN_VALUE,\
                                       self.SOURCE_READ_SPNKEY_VALUE,\
                                       self.tenant_id,\
                                       self.AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH)
        df = df.loc[df['RowId'] == self.RowId]
        jsondf = df.to_json(orient = 'records')
        return jsondf

# Create the POST endpoint with path '/readQuery'
@app.post("/readQuery")
async def datalake(RowId: int):
    readerObj =  DataLakeReader(RowId)
    return readerObj.readQuery()

if __name__ == '__main__':
    app.run(debug=True)