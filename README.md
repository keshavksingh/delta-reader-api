# Delta Storage Format Reader API

A Containerized Delta Formatted Table Reader. The data source is Azure Data Lake Gen2 Storage in Delta Format. 
## main.py
* The solution leverages Python Delta Reader to enable an API for the data.
* In the example, we leverage FastAPI to build the API.
* Build a lightweight Docker Container and host it on either Azure Kubernetes Service (AKS) or Azure Container Instance (ACI)
* Tested on 2 Million Records with response times of 2 seconds when the container is hosted on Azure Container Instance with 4 Cores.
* For larger datasets, consider Z-Order indexing and efficient partitioning with appropriate considerations to query access patterns.

## main-v2.py
* In this solution, we load the data from Delta Lake into IN MEMORY Dataframe
* Serve it through memory. It reduces the latency to milli seconds with the tradeoff of the need to scheduler-based init refreshes.

## main-v3.py
* Ultimately we leverage https://pypi.org/project/fastapi-utils/ and https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/ to be able to refresh "in-memory" dataframe from DeltaLake every 60 seconds without disrupting reads.
* Helps reflect changes of data from Lake and refresh the in memory dataframe (helps with lightening fast data serving for the API reads) by triggering a background refresh preodically without hurting realtime reads of data.
