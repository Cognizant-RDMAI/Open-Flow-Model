# Open Flow Model

## Motivation and purpose
Understanding river flow is essential for effective water resource management. River flow data, typically measured in cubic meters per second (m³/s), describes the volume of water moving through a waterbody at a given time. This information is critical for:

- **Predicting floods**
- **Identifying and tracing pollution sources**
- **Managing ecosystems and water quality**

However, gauged flow data are often sparse or entirely missing, especially in smaller or remote rivers. This is largely due to the high cost of installing and maintaining monitoring stations, leaving many catchments without direct observations. With a changing climate, understanding changes in flow is becoming increasingly important.

To address these data gaps, hydrologists often rely on surrogate data from comparable catchments, deterministic hydrology models, or conduct expensive field campaigns. These approaches, while useful, are limited in scalability and timeliness.

### Report Download:

Please download the Open Flow Model Report [here](https://github.com/Cognizant-RDMAI/Open-Flow-Model/tree/main/supporting-documents).

### Objective
The Open Flow Model aims to estimate daily mean river flow $(m^3/s)$ in ungauged catchments using a machine learning approach that leverages both static and dynamic data sources. 

Estimating daily mean flow $(m^3/s)$ is the main objective of our work; however, this metric can be used to infer other key flow metrics, such as mean flow and Q95 (flow exceeded or equaled 95% of the time; usually taken as a metric of low flow). During phase 3, we aim to evaluate the model’s usefulness for estimating these metrics as well. 

The model, and its associated performance metrics, presented in this report, represents the first iteration of our ML-model addressing the challenges mentioned above. As River Deep Mountain AI proceeds into phase 3, these models will be developed further and refined. The results presented here are therefore preliminary and should be considered as such.

### Project details

[River Deep Mountain AI](https://www.cognizant.com/us/en/industries/ocean/rdmai) is an innovation project funded by the Ofwat Innovation Fund working collaboratively to develop open-source AI/ML models that can inform effective actions to tackle waterbody pollution.

The project consists of 6 core partners: Northumbrian Water, Cognizant Ocean, Xylem Inc, Water Research Centre Limited, The Rivers Trust and ADAS. The project is further supported by 6 water companies across the United Kingdom and Ireland. 

## Installation and Setup

This guide provides detailed instructions for setting up the project environment and preparing the necessary data.

### 1. Clone the Repository

First, you need to clone this repository to your local machine. If you are new to Git, you can do this by opening a terminal and running the following command:

```bash
git clone https://github.com/Cognizant-RDMAI/Open-Flow-Model.git
cd Open-Flow-Model
```

This will download the project into a new folder named `Open-Flow-Model` and navigate you into it.

### 2. Install Poetry

This project uses Poetry for dependency management. You can install it by following the official instructions [here](https://python-poetry.org/docs/#installation).

### 3. Install Project Dependencies

Navigate to the project's root directory and run the following command to install the required packages:

```bash
poetry install
```

This will create a virtual environment and install all the dependencies listed in the `pyproject.toml` file.

### 4A. Prepare Data and Run Inference (RECOMMENED AS NO MODEL TRAINING REQUIRED)

To prepare the data and run an inference example, you need to execute a sequence of notebooks located in the `notebooks/` directory. This process downloads the required datasets, processes them, and demonstrates how to use the trained model.

1.  **Run `01-DataDownload.ipynb`**: Downloads the CAMELS-GB dataset and extracts it to `datasets/camels-gb/data`. Takes about 5 mins on M1 MAC.
2.  **Run `02-DataAggregation.ipynb`**: Aggregates the raw data into unified files.  Takes about 60 mins on M1 MAC.
3.  **Run `03-DataTrim.ipynb`**: Trims the dataset to remove irrelevant columns and rows with missing values. Takes about 2 mins on M1 MAC.
4.  **Run `04-FeatureEnginnering.ipynb`**: Creates additional features for the model. Takes about 2 mins on M1 MAC.
5.  **Run `05-DataSplit.ipynb`**: Splits the data into training and testing sets.  Ensure the parameter USE_EXISTING_TRAIN_TEST_SPLIT_FOR_LOCAL_MODEL = True. Takes about 180 mins on M1 MAC.
6.  **Run `07-Inference.ipynb`**: Picks up model in the repo and demonstrates how to use the trained model for inference on new data. Takes about 1 mins on M1 MAC.

### 4B. Prepare Data, train new model and Run Inference

To prepare the data, train the model, and run an inference example, you need to execute a sequence of notebooks located in the `notebooks/` directory. This process downloads the required datasets, processes them, and demonstrates how to use the trained model.

1.  **Run `01-DataDownload.ipynb`**: Downloads the CAMELS-GB dataset and extracts it to `datasets/camels-gb/data`.
2.  **Run `02-DataAggregation.ipynb`**: Aggregates the raw data into unified files.
3.  **Run `03-DataTrim.ipynb`**: Trims the dataset to remove irrelevant columns and rows with missing values.
4.  **Run `04-FeatureEnginnering.ipynb`**: Creates additional features for the model.
5.  **Run `05-DataSplit.ipynb`**: Splits the data into training and testing sets. Ensure the parameter USE_EXISTING_TRAIN_TEST_SPLIT_FOR_LOCAL_MODEL = False.
6.  **Run `06-ModelTraining.ipynb`**: Trains the model using the prepared data.
7.  **Run `07-Inference.ipynb`**: Picks up newly trained model and demonstrates how to use the trained model for inference on new data.

### 5. Manually Download Chalk Streams List

The Chalk Streams dataset must be downloaded manually.

1.  Download the **Chalk Rivers (England)** dataset from the [Natural England Open Data Geoportal](https://naturalengland-defra.opendata.arcgis.com/datasets/Defra::chalk-rivers-england/about).
2.  Use a GIS tool to identify monitoring points that fall on chalk streams.
3.  Create a `.csv` file named `chalk_streams.csv` in the `datasets` directory with two columns: `gauge_id` and `chalk_stream_flag`.

## Folder Structure

- **datasets**: Contains raw, intermediate, and processed data used in the project.
- **models**: Contains trained machine learning models.
- **notebooks**: Contains Jupyter notebooks for data exploration, feature engineering, model training, and inference.
- **resources**: Contains supplementary materials such as charts and spreadsheets.
- **src**: Contains Python source code for data preparation and utility functions.
- **tests**: Contains unit tests for the source code.

###
Compute instance used for development
64 vCPUs, 416 GB RAM	NVIDIA T4 x 4

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
3. Xylem Water Solutions UK Limited
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
