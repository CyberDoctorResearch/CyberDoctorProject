# Article Preprocessing

## Introduction

This folder contains the source code and resources for the Article Preprocessing phase of the CYBERDOC system. This phase focuses on preparing CTI (Cyber Threat Intelligence) articles for further processing by performing deduplication, sentence classification, and security-related entity retrieval.

## Workflow

1. **Article De-duplication**:
   - Use the `Article De-duplication.ipynb` notebook to identify and filter out duplicate articles based on their key descriptions. This ensures the dataset includes only unique and diverse CTI articles for further processing.

2. **Security-Related Entity Retrieval**:
   - Use the `Security-Related Entity Retrieval.ipynb` notebook to extract security-related entities (e.g., CVEs, malware names) from CTI articles. These entities provide essential context for constructing a knowledge graph.

3. **Tactic Model Training and Improvement**:
   - Use the following combined steps to train and enhance the tactic classification model for identifying sentences that describe attack tactics:
     - **Data Preparation**: Use the `labeled sentence with tactics .xlsx` file to provide labeled sentences for training the tactic model.
     - **Model Training and Inference**: Use the `tactic model training and inference.ipynb` notebook to fine-tune a RoBERTa-based model for accurately identifying tactics in CTI article sentences.
     - **Active Learning (Optional)**: Use the `Optional Active learning.ipynb` notebook to iteratively select and label additional sentences, expanding the dataset and further improving the model's performance if needed.

4. **Tools and Utilities**:
   - The `tools.py` script provides utility functions.



