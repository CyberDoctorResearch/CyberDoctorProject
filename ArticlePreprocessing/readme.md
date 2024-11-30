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
     - **Data Preparation**: Use the `labeled sentence with tactics.xlsx` file to provide labeled sentences for training the tactic model.
     - **Model Training and Inference**: Use the `tactic model training and inference.ipynb` notebook to fine-tune a RoBERTa-based model for accurately identifying tactics in CTI article sentences.
     - **Active Learning (Optional)**: Use the `Optional Active learning.ipynb` notebook to iteratively select and label additional sentences, expanding the dataset and further improving the model's performance if needed.

4. **Tools and Utilities**:
   - The `tools.py` script provides utility functions.


### Active Learning and Uncertainty Sampling

- Employed active learning to improve model performance, particularly for tactics with fewer labeled samples.
- **Uncertainty Measures**:
  - **Classification Uncertainty**: \( 1 - p_{\text{max}} \)
  - **Classification Margin**: \( p_{\text{max}} - p_{\text{next max}} \)
  - **Classification Entropy**: \( -\sum_{i=1}^{n} p_i \log_2 p_i \)
- **Process**:
  - Select sentences with high uncertainty scores.
  - Manually label these sentences and update the dataset.
  - Retrain the model with the expanded dataset.
 
## Article Deduplication Effectiveness

**Enhanced Diversity and Comprehensiveness**: The deduplication process significantly improved the variety and depth of unique behaviors captured in the generated summaries. This enhancement was especially pronounced for CVEnvd+ (a group of CVEs with insufficient behavior descriptions in the National Vulnerability Database), where diverse articles were crucial for uncovering missing or overlooked details.

- On average, **Summarydedup** (summaries generated from deduplicated articles) demonstrated a 30% increase in unique behaviors compared to **Summarydup** (summaries generated from all articles without deduplication) for CVEnvd+.  
- For CVE2024pop (a group of popular CVEs in 2024), deduplication offered a smaller but consistent improvement by reducing redundant content in summaries while retaining critical details.

**Case Studies**: Deduplication uncovered critical behaviors that were obscured by repetitive content in non-deduplicated summaries. Examples include:  
- **CVE-2024-21336**: The deduplicated summary revealed its association with SSL/TLS impersonation (a type of attack where secure communication channels are faked), a detail hidden in repetitive content from non-deduplicated articles.  
- **CVE-2024-22043**: The deduplicated summary highlighted critical information about an out-of-bounds read vulnerability (a programming error where data outside the intended memory boundaries is accessed) affecting Siemens Parasolid, a CAD software component.  

## Model Performance

- **Improvement Through Active Learning**:
  - The tactic model achieved an average **88% precision** and **90% recall** after active learning.
- **Performance Metrics Before and After Active Learning**:

  | Attack Tactic       | Precision Before | Recall Before | Precision After | Recall After |
  |---------------------|------------------|---------------|-----------------|--------------|
  | Initial Access      | 0.67             | 0.75          | 0.88            | 0.89         |
  | Execution           | 0.17             | 0.11          | 0.90            | 0.92         |
  | Defense Evasion     | 0.50             | 0.14          | 0.85            | 0.86         |
  | Command and Control | 0.05             | 0.06          | 0.84            | 0.87         |
  | Privilege Escalation| 0.35             | 0.39          | 0.89            | 0.90         |
  | Persistence         | 0.00             | 0.00          | 0.91            | 0.93         |
  | Lateral Movement    | 0.00             | 0.00          | 0.90            | 0.91         |
  | Data Leak           | 0.18             | 0.12          | 0.88            | 0.89         |
  | Exfiltration        | 0.00             | 0.00          | 0.84            | 0.89         |
  | Impact              | 0.00             | 0.00          | 0.94            | 0.92         |
  | **Macro Average**   | **0.21**         | **0.17**      | **0.88**        | **0.90**     |


