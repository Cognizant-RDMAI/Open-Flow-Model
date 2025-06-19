# Installation Guide
Please refer to this guide to set up your system properly.


## Libraries requirements
 - Python 3.10.16
 - Required packages listed in `requirements.txt`


## Data import
As per best practice, datasets are not stored in the repository. Below instructions to retrieve and locate the data into the preexisting (empty) directories within the repo.

### CAMELS-GB
CAMELS-GB dataset has to be downloaded and ingest in specific `datasets\camels-gb` directory. Developers:
 - can easily unzip content of directory `data` from zipped file, available at https://catalogue.ceh.ac.uk/documents/8344e4f3-d2ea-44f5-8afa-86d2987543a9, into `\datasets\camels-gb-data\data`
 - may want to remove `__README.html` and unzip `CAMELS_GB_catchment_boundaries.zip`

Once done, file hierarchy should look like:
```bash
OpenFlowModel\datasets\camels-gb-data\data:
¦   .gitkeep
¦   CAMELS_GB_climatic_attributes.csv
¦   CAMELS_GB_humaninfluence_attributes.csv
¦   CAMELS_GB_hydrogeology_attributes.csv
¦   CAMELS_GB_hydrologic_attributes.csv
¦   CAMELS_GB_hydrometry_attributes.csv
¦   CAMELS_GB_landcover_attributes.csv
¦   CAMELS_GB_soil_attributes.csv
¦   CAMELS_GB_topographic_attributes.csv
¦   
+---CAMELS_GB_catchment_boundaries
¦       CAMELS_GB_catchment_boundaries.cpg
¦       CAMELS_GB_catchment_boundaries.dbf
¦       CAMELS_GB_catchment_boundaries.prj
¦       CAMELS_GB_catchment_boundaries.sbn
¦       CAMELS_GB_catchment_boundaries.sbx
¦       CAMELS_GB_catchment_boundaries.shp
¦       CAMELS_GB_catchment_boundaries.shp.xml
¦       CAMELS_GB_catchment_boundaries.shx
¦       
+---timeseries
        CAMELS_GB_hydromet_timeseries_10002_19701001-20150930.csv
        CAMELS_GB_hydromet_timeseries_10003_19701001-20150930.csv
        CAMELS_GB_hydromet_timeseries_1001_19701001-20150930.csv
        CAMELS_GB_hydromet_timeseries_101002_19701001-20150930.csv
        ...
```

Please note that, since containing documentation, directory `dataset\camels-gb-data\supporting-documents`, which mirrors the homologous one within the mentioned zip file, has been kept in the repository.

### Chalk Streams List
Chalk Streams List dataset has to be created in `datasets` directory. Developers:
 - can download **Chalk Rivers (England)** at https://naturalengland-defra.opendata.arcgis.com/datasets/Defra::chalk-rivers-england/about
 - leverage GIS (or any other compatible mapping software) to identify monitoring points falling on the rivers identified as chalk streams

 Resulting file has to be a `.csv` with two columns, `gauge_id` and `chalk_stream_flag`, with the former being the gauge identifier (according to CAMELS-GB denomination), and the latter a Boolean (`FALSE` or `TRUE`), whether the catchments lies on a chalk streams.


## Environment variables settings
To be able to run the rode you need to set an `.env` file, in the main root of the repository, stating two environment variables:
 - **STADIA_MAPS_API_KEY**: the API key for Stadia. In case developers want to use another provider to render maps, they may want to have a look at function `get_stadiamaps_provider_api_key_in_env` in `util_IO.py`
 - **MLFLOW_TRACKING_URI**: the URI for MLflow tracking. Please refer to MLflow documentation regarding [setting tracking URI](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html?highlight=set_tracking_uri#mlflow.set_tracking_uri)