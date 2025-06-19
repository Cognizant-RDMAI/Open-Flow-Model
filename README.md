# Open Flow Model

## Motivation and purpose
Understanding river flow is essential for effective water resource management. River flow data, typically measured in cubic meters per second (m³/s), describes the volume of water moving through a waterbody at a given time. This information is critical for:

- **Predicting floods**
- **Identifying and tracing pollution sources**
- **Managing ecosystems and water quality**

However, gauged flow data are often sparse or entirely missing, especially in smaller or remote rivers. This is largely due to the high cost of installing and maintaining monitoring stations, leaving many catchments without direct observations. With a changing climate, understanding changes in flow is becoming increasingly important.

To address these data gaps, hydrologists often rely on surrogate data from comparable catchments, deterministic hydrology models, or conduct expensive field campaigns. These approaches, while useful, are limited in scalability and timeliness.

### Objective
The Open Flow Model aims to estimate daily mean river flow $(m^3/s)$ in ungauged catchments using a machine learning approach that leverages both static and dynamic data sources. 

Estimating daily mean flow $(m^3/s)$ is the main objective of our work; however, this metric can be used to infer other key flow metrics, such as mean flow and Q95 (flow exceeded or equaled 95% of the time; usually taken as a metric of low flow). During phase 3, we aim to evaluate the model’s usefulness for estimating these metrics as well. 

The model, and its associated performance metrics, presented in this report, represents the first iteration of our ML-model addressing the challenges mentioned above. As River Deep Mountain AI proceeds into phase 3, these models will be developed further and refined. The results presented here are therefore preliminary and should be considered as such.

### Project details

[River Deep Mountain AI](https://www.cognizant.com/us/en/industries/ocean/rdmai) is an innovation project funded by the Ofwat Innovation Fund working collaboratively to develop open-source AI/ML models that can inform effective actions to tackle waterbody pollution.

The project consists of 6 core partners: Northumbrian Water, Cognizant Ocean, Xylem Inc, Water Research Centre Limited, The Rivers Trust and ADAS. The project is further supported by 6 water companies across the United Kingdom and Ireland. 

## Repo structure
To enhance understandability of the way the project has been structured, there are different directories implicitly explaining the logic to arrange files related to data, notebooks, configurations, and so on. However, after running the first notebooks, developers can find some `.pkl` files in this main directory as they store information that need (or it is more convenient) to be shared among the different steps of the analysis.

### `datasets`
Here the list of the datasets used within the project, with a brief description:
 - **[CAMELS-GB](https://catalogue.ceh.ac.uk/documents/8344e4f3-d2ea-44f5-8afa-86d2987543a9)**: A comprehensive dataset of catchment attributes across Great Britain
 - **[Hydrology Data Explorer API](https://environment.data.gov.uk/hydrology/landing)**: Provides flow flags and other hydrological indicators
 - **[Chalk Streams List](https://naturalengland-defra.opendata.arcgis.com/datasets/Defra::chalk-rivers-england/about)**: Identifies unique geological catchments with presence of chalk. Dataset from Natural England. 

In terms of availability of the data please note that for:
 - **CAMELS-GB**, developers can refer to the [Installation Guide](INSTALL.md) for all the details and reference to the documentation provided by the provider
 - **Hydrology Data Explorer API**: data queries via API are made at runtime, so there is no need to provide these information before running the notebooks
 - **Chalk Streams List**: developers can refer to the [Installation Guide](INSTALL.md) for all the details

### `notebooks`
Notebooks drive the development of the project.

Currently, all the code is nested in the notebooks, and there are no functions defined in any `.py` files or customized packages, except for the file `util_IO.py`, containing utility functions used throughout the notebooks.

The flow of the analysis is straightforward to follow, as the notebooks are numbered (i.e., every 
notebook starts with the name of the step: `01`, `02`, etc..).

The below description details what developers should expect:

#### Step 1 - Aggregation of data files
The first step, as the notebook name suggests, is all about aggregating the raw, original data into different files.

There are two main sets of variables which are considered:
- **Attributes**: these are static variables or variables that change over relative long periods of time describing the location where the sensor is located, such as soil, topography, land cover, etc.
- **Time series**: these are continuous dynamic variables, such as climate variables, as well as 
the ***label*** (variable to simulate), which for this model is `discharge_vol`.

Briefly, the notebook performs the following:
- For each set of variables (attributes or time series), the aggregation process consists of:
   1. Definition of the fields/rows of interest.
   2. Aggregation of files.
   3. Storing of the aggregated file, as well as further metadata, if required.
- The metadata used during the data aggregation is defined and stored as `.pkl` files (in the main project directory).

However, given the structure of the data files, the aggregation process has some nuances:
 - **Attributes**, the aggregation process consists of a stream of tables joined by the table index . Therefore, direction of expansion is  **horizontal**.
 
    Regarding field selection, there are currently only two aggregation lists, leading to the creation of: 
      - `full_list_of_fields`: containing the full set of available fields in the original dataset.
      - `fundamental`: excluding fields which are calculated/derived from the other fields already present in the CAMELS-GB.
   
   Although not initially included into CAMELS-GB, **Chalk Streams List** is easily integrated into the overall attributes dataset by adding the correspondent data frame to the dictionary. 
   
   In addition, developers can easily add further aggregation logics by creating a new dictionary with the list of fields to include for each table; they also may want to create a function doing that, to avoid code repetition, as the dictionary would be the only differing input.
 
 - **Time series**, the aggregation process consists of a stream of table concatenation. Therefore, the direction of expansion is **vertical**. While all fields are retained in this step, the data aggregated into rows are subject to some manipulation. Below is a description of the main stages of processing for each data file:
   - The **catchment ID** is extracted from the file name.
   - Values of the time series are ingested from each file. However, the model simulated flow is then flanked by the corresponding extracted observed flow via the **Hydrology Data API** only in the presence of flags `Good` and `Complete`. This means that, for flow only, the procedure aims to substitute values from CAMELS-GB with values obtained from the Hydrology Data API. A consequence of the intrinsic check of simulated flow quality is a **discontinuous time series**. However, since several catchments have `null` values for flow, even within the CAMELS-GB dataset, there is no avoiding the need to deal with discontinuous time series.
   - **Catchment ID** is replicated to the whole time series as new column.
   - Data is attached to the block.

   The block is finally saved, as well as a dictionary containing the time ranges for each catchment ID, and logs from the aggregation.
 
 
 #### Step 2 - Exploratory Data Analysis
The second step is the exploratory data analysis. This step consists of several notebooks, each one focused on a specific purpose:

  - **02a-EDA-Attributes-Geo.ipynb**: visualisation of gauge station locations, and catchments areas in the entire dataset.
 
    This notebook also contains a section in which developers can specify a set of catchments for visualisation. This functionality serves diverse purposes: developers can return to this point and assess locations, without disrupting the code workflow. 
    
    Finally, there is a section that facilitates a cross check between `area` calculated using the polygons and the area attribute available within the CAMELS-GB. 

 - **02a-EDA-Attributes.ipynb**: analysis regarding attributes.
    
    Please note: most of the visualisation here has been performed using `ProfileReport` from package `ydata_profiling`. Unfortunately, due to conflicts with the other packages, this package has not been included in the libraries requirement list ([Libraries requirements](INSTALL.md#libraries-requirements)) as it is not production-ready. For this reason `import ydata_profiling` does not occur at the beginning of the notebook, or anywhere else, except in that specific chunk of code. Nevertheless, to replicate what done, developers can create a specific Python environment in which the package `ydata_profiling`is installed, or use another package, while ensuring that the `attributes_html_report_flag` flag is enabled.

    Analyses possible in the notebook include: 
     - Missing values analysis.
     - Linear correlation matrix analysis.

 - **02b-EDA-Timeseries.ipynb**: analysis of time series.
    
    First chunks of code creates chart for each continuous time series among all the catchments, stored as `.png` in `resources\EDA\timeseries`.

    Further analyses include:
      - The distribution of the time series length.
      - Linear correlation matrix among time series values.
      - An investigation of the max number of consecutive rainy days.
      - Missing values analysis.
      - Generation of a table of percentiles of flow (label), grouped-by catchment.
      - Investigation of the quantity of zeros (0s); this has driven development toward the utilisation of the Hydrology Data API's `Good` and `Complete` flags.
      - A comparison of zero values between flow data from CAMELS-GB and the Hydrology Data API.
      - Generation of a histogram of flow distribution.

 - **02c-EDA-Timeseries&Attributes.ipynb**: aggregation of attributes and time series.

    After merging the two datasets, the analyses performed in the notebook include:
     - A scatter plot of `flows` vs. `area`, while considering average precipitation of the previous 5, 15, and 30 days.
     - An analysis of `area` in catchments with a significant percentage of 0 flows.

 - **02d-EDA-DataTrim.ipynb**: performs columns/feature and row selection, mainly based on availability of data (i.e., missing values).

    More specifically, the notebook:
    - Removes attributes columns with too many `null` values.
    - Removes time series columns considered not relevant for the model.
    - Removes rows where at least one attribute is `null`.
    - Corrects miss-alignment between catchment attributes and time series due to the Hydrology Data API operation. 
  
    Please note: this is the only notebook, within step 2, that modifies the datasets by reducing/trimming data.

#### Step 3 - Feature Engineering
This step performs all processes needed to obtain a dataset which can be directly fed into the machine learning models.

 - **03a-FE_AdditionalFeatures.ipynb**: following the schema adopted across the entire project, performs feature engineering, including differentiation between **attributes** and **timeseries** datasets, more specifically: 
    - **Attributes**:
      - Non-numerical information describing gauge locations are extracted and stored in a specific data frame within the aggregated attributes data directory.
      - the *gauge_name* field has been split into two fields, namely *river* and *location*, detached, and saved as separated table.
    - **Timeseries**: A few additional fields have been added to timeseries datasets to provide a time reference during the model training phase, including:
      - `sin_year` and `cos_year`, calculated by setting the 21st of March as 0 $\pi$, and transforming the dates information via a trigonometric function (*sin* and *cos*) with 2 $\pi$ representing one year.
      - `time_ref`, integer calculated as the difference in days from the timeseries dates and the oldest date available in the whole dataset.
 
    In addition, a logarithmic transformation has been added as potential label to use.

    Please note: a section at the end of this notebook performs cluster analysis. Only attribute fields have been considered, since the use of `t-SNE`. However, developers may want to enhance the cluster analysis in this section as this notebook generates the final data frames that are fed into the model. Developers may want to use the cluster analysis to:
    - Implement an alternative approach to delineating catchments, which can be useful for the definition of alternative train/test datasets.
    - Add/substitute dimensions to the model.

 - **03b-FE_ModelFeed.ipynb**: implements the second sub-step to produce data that directly feeds into the machine learning models. Here, continuous **time series** data coming from different sensors are broken up into time windows, while maintaining a coherent **attributes** dataset:
    - **Timeseries**:
      - After grouping by `catchmentID` and `group`, time windows of continuous timeseries are broken up into windows of a certain length.
      - Windows of the different sensor data are aggregated.
      - Explanatory variables are scaled.
      - Explanatory variables and labels for the training set only are shuffled (test set is excluded as the shuffle would be irrelevant).
    - **Attributes**:
      - A registry data frame originating directly from the timeseries windowing function is merged  with the original data frame, with attributes. This produces a new dataset of static variables that are coherent with observations coming from windowing.
      - Static variables are scaled.

    While this notebook has a considerable set of parameters, they can all be found in the first chunks of code. When `example_input` flag is set to `True`, a dummy example is created which is useful for assessing what the routine is doing by looking at a very small sample of (random) data.

#### Step 4 - Model training
During model training, all metrics are collected and there us an in-depth analysis of model error. Due to the need to store a vast quantity of artifacts, **04-BaseModel.ipynb** uses MLflow experiments tracking capabilities.

Overall, the notebook:
 - Loads the data coherently with the parameters chosen in the first chunks. 
 - Defines layers of the neural network as well as the loss function (developers may need to interact with this set of parameters too). 
 - Compiles the model. 
 - Creates TensorFlow datasets, to speed up the training. 
 - Trains the model.
 - Evaluates the model on the test set. 
 - Performs error analysis. 

  Since the model can simulate flow or its logarithmic transformation, error analysis automatically calculates metrics based on "level" predictions , which may vary from the default metrics stored by MLflow, as these metrics are related to the pure training process. Error analyses available after the training include:
   - Scatter plots of differences (all variables and zoom-in on MAE and MAPE), errors vs. actual. 
   - Error concentration at catchment-level. 
   - $R^2$/NSE at catchment level. 
   - Identification of the most problematic catchments. 
   - Maps showing good and bad catchments. 
   - Graphs of actual and predicted time series, both for training and test datasets. 
   - Generation of flow duration curves (*FDCs*) considering the distribution of actual and predicted time series, both for training and test datasets. 

### `resources`
The `resources` directory stores mainly artifacts that are not used in the training process, but still might provide value by being archived. The `resources` directory contains the  subdirectory `EDA`, which stores anything coming from step 2, as well as the subdirectory `chart`, which currently is only used in step 3.

### `temp`
A temporary directory used solely by MLflow while storing artifacts like `.json` or `.csv` files.

### Inherent time varying
Due to the inherent time varying of the challenges addressed in this project, it is important to continuously re-train and fine-tune the model to make sure it is up to date with the latest trends and variances of our climate and environment. The model was trained on publicly available data up to 2015. In the future, the model may not reflect updated scientific understandings, environmental conditions, or regulatory standards.

## Disclaimer
River Deep Mountain AI (“RDMAI”) consists of 10 parties. The parties currently participating in RDMAI are listed at the end of this section and they are collectively referred to in these terms as the “consortium”.

This section provides additional context and usage guidance specific to the artificial intelligence models and / or software (the “**Software**”) distributed under the MIT License. It does not modify or override the terms of the MIT License.  In the event of any conflict between this section and the terms of the MIT licence, the terms of the MIT licence shall take precedence.

#### 1. Research and Development Status
The Software has been created as part of a research and development project and reflects a point-in-time snapshot of an evolving project. It is provided without any warranty, representation or commitment of any kind including with regards to title, non-infringement, accuracy, completeness, or performance. The Software is for information purposes only and it is not: (1) intended for production use unless the user accepts full liability for its use of the Software and independently validates that the Software is appropriate for its required use; and / or (2) intended to be the basis of making any decision without independent validation. No party, including any member of the development consortium, is obligated to provide updates, maintenance, or support in relation to the Software and / or any associated documentation.
#### 2. Software Knowledge Cutoff
The Software was trained on publicly available data up to September 2015. It may not reflect current scientific understanding, environmental conditions, or regulatory standards. Users are solely responsible for verifying the accuracy, timeliness, and applicability of any outputs.
#### 3. Experimental and Generative Nature
The Software may exhibit limitations, including but not limited to:
 - Inaccurate, incomplete, or misleading outputs; 
 - Embedded biases and / or assumptions in training data;
 - Non-deterministic and / or unexpected behaviour;
 - Limited transparency in model logic or decision-making
 
Users must critically evaluate and independently validate all outputs and exercise independent scientific, legal, and technical judgment when using the Software and / or any outputs. The Software is not a substitute for professional expertise and / or regulatory compliance.

#### 4. Usage Considerations
 
 - Bias and Fairness: The Software may reflect biases present in its training data. Users are responsible for identifying and mitigating such biases in their applications.
 - Ethical and Lawful Use: The Software is intended solely for lawful, ethical, and development purposes. It must not be used in any way that could result in harm to individuals, communities, and / or the environment, or in any way that violates applicable laws and / or regulations.
 - Data Privacy: The Software was trained on publicly available datasets. Users must ensure compliance with all applicable data privacy laws and licensing terms when using the Software in any way.
 - Environmental and Regulatory Risk: Users are not permitted to use the Software for environmental monitoring, regulatory reporting, or decision making in relation to public health, public policy and / or commercial matters. Any such use is in violation of these terms and at the user’s sole risk and discretion.
 
#### 5. No Liability
 
This section is intended to clarify, and not to limit or modify, the disclaimer of warranties and limitation of liability already provided under the MIT License.
 
To the extent permitted by applicable law, users acknowledge and agree that:
 - The Software is not permitted for use in environmental monitoring, regulatory compliance, or decision making in relation to public health, public policy and / or commercial matters.
 - Any use of the Software in such contexts is in violation of these terms and undertaken entirely at the user’s own risk.
 - The development consortium and all consortium members, contributors and their affiliates expressly disclaim any responsibility or liability for any use of the Software including (but not limited to):
   - Environmental, ecological, public health, public policy or commercial outcomes
   - Regulatory and / or legal compliance failures
   - Misinterpretation, misuse, or reliance on the Software’s outputs
   - Any direct, indirect, incidental, or consequential damages arising from use of the Software including (but not limited to) any (1) loss of profit, (2) loss of use, (3) loss of income, (4) loss of production or accruals, (5) loss of anticipated savings, (6) loss of business or contracts, (7) loss or depletion of goodwill, (8) loss of goods, (9) loss or corruption of data, information, or software, (10) pure economic loss, or (11) wasted expenditure resulting from use of the Software —whether arising in contract, tort, or otherwise, even if foreseeable . 
 
Users assume full responsibility for their use of the Software, validating the Software’s outputs and for any decisions and / or actions taken based on their use of the Software and / or its outputs.

#### 6. Consortium Members  
 
1. Northumbrian Water Limited
2. Cognizant Worldwide Limited
3. Xylem
4. Water Research Centre Limited
5. RSK ADAS Limited
6. The Rivers Trust
7. Wessex Water Limited
8. Northern Ireland Water
9. Southwest Water Limited
10. Anglian Water Services Limited




## References
Useful papers on river flow estimation:
 - Arsenault, R., et al. (2022). LSTM models significantly outperform traditional hydrological models in regionalization tasks across 148 catchments in northeast North America. [Study on deep learning for streamflow prediction].

 - Ghaneei, H., et al. (2024). A nonlinear knowledge-based framework combining UMAP and Growing Neural Gas clustering with LSTM models for streamflow prediction in ungauged basins. [Demonstration of regionalized deep learning guided by unsupervised learning].

 - Mangukiya, R., & Sharma, A. (2024). Deep learning-based daily streamflow prediction from monthly aggregated and intermittent observations using LSTM models. [Application in near-natural and human-influenced watersheds].

 - Sun, Q., et al. (2021). Graph Neural Networks for streamflow forecasting across large-sample hydrology datasets. [Benchmarking GNN architectures using CAMELS].

 - Sun, Q., et al. (2022). Basin-scale river network learning with physics-based connectivity and data fusion using GNNs. [Integration with the National Water Model].

 - Wilbrand, S., et al. (2023). Global LSTM models for streamflow prediction using ERA5 and HydroMT datasets. [Evaluation across 500+ US catchments].

 - Zhang, Y., et al. (2022). Encoder-decoder LSTM model for flood prediction in 35 mountainous catchments in China. [Assessment of generalization and regional model performance].