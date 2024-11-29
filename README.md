# CyberDoctor

## Introduction
CYBERDOC is an innovative tool designed to enhance Cyber Threat Intelligence (CTI) by automatically sourcing, deduplicating, and summarizing cyber threat behaviors from diverse CTI articles. In an era where cyber threats are rapidly evolving and becoming increasingly sophisticated, CYBERDOC provides security managers and automated systems with timely and comprehensive insights to better understand and respond to emerging threats.


## Approach
The architecture of CYBERDOC, illustrated in Figure 2, consists of three major phases:

1. **Article Preprocessing**: This phase prepares collected CTI articles for downstream analysis by:
   - **Article Deduplication**: Utilizing a language model to identify and filter redundant articles, ensuring that only unique CTI articles are retained for processing.
   - **Sentence Classification**: Employing a tactics classification model to label sentences with corresponding cyber attack tactics, enabling focused extraction of relevant information.
   - **Security-Related Entity Retrieval**: Using a Large Language Model (LLM) to extract security-focused entities from classified sentences, ensuring relevance and accuracy in the extracted data.

2. **Knowledge Graph Construction**: This phase organizes knowledge extracted from CTI articles into a structured, interconnected format by:
   - **Triple Extraction**: Dividing CTI articles into text segments and extracting knowledge in the form of triples from each segment.
   - **Memory Management**: Implementing a short-term memory to store triples from individual segments and a long-term memory to unify triples across entire articles.
   - **Knowledge Graph Merging**: Utilizing an LLM agent to merge unified triples from multiple CTI articles, forming a comprehensive knowledge graph that represents the interconnected cyber threat information.

3. **Threat Summarization & Community Detection**: This phase leverages the constructed knowledge graph to generate actionable insights and identify relationships between cyber threats by:
   - **Threat Summary Generation**: Deploying an LLM to generate concise, detailed summaries of cyber threats, providing clear overviews of threat behaviors and key findings.
   - **Security-Oriented Community Detection**: Analyzing the knowledge graph to group related entities and interactions, highlighting interconnected threats and enhancing understanding of the overall threat landscape.


## Evaluation

We evaluated **CyberDoctor** on two datasets to assess its ability to enhance cyber threat intelligence analysis:

- **Cyber Threat Dataset**: This dataset includes 1,000 articles covering 100 CVEs randomly selected from 15,079 CVEs reported in the National Vulnerability Database (NVD) between January and June 2024. Articles were retrieved using a search engine and segmented into smaller sections for analysis.

- **De-duplicated Cyber Threat Dataset**: This dataset focuses on two subsets of CVEs requiring additional context beyond NVD descriptions. The first subset includes 17 CVEs where the NVD descriptions were incomplete. Using **CyberDoctor's** de-duplication module, we curated 170 unique articles for these CVEs. The second subset highlights 17 high-profile CVEs identified as significant in 2024 based on security reports. For these CVEs, 170 unique articles were retrieved
### CVE Behavior Description

The results show that **CyberDoctor** outperforms models like **NVD** and **ChatGPT** in identifying behaviors related to CVEs, especially for CVEs not fully described by the NVD (referred to as CVEnvd+). **CyberDoctor** consistently identifies more behaviors across all CVSS levels.

- **All CVEs**: CyberDoctor identifies an average of 3.73 behaviors per CVE, closely aligning with the ground truth (3.77) and outperforming NVD (3.4) and ChatGPT (3.58).
  
- **CVEnvd+**: For CVEs not fully described by NVD, CyberDoctor identifies an average of 4.39 behaviors, significantly surpassing NVD (2.87) and ChatGPT (3.74). This demonstrates CyberDoctor's strength in extracting more comprehensive insights from incomplete datasets.

![image](https://i.imgur.com/t3lnBPp.png)

### Knowledge Graph Construction

In terms of knowledge graph construction, **CyberDoctor** achieves superior performance with higher recall and F1 scores compared to **GPT-4o** and **GraphRAG**, demonstrating its advanced capability in extracting security-related behaviors and relationships while maintaining high precision.

![image](https://i.imgur.com/HFaHHDN.png)

### Classification Model Effectiveness

The tactics model used by **CyberDoctor** demonstrates robust performance in identifying cyber attack tactics and behaviors.

- **Tactics Model**: Trained through active learning on a dataset of 17,420 labeled sentences, the model achieves a weighted F1-score of 89%, with precision reaching 88% and recall at 90%. Notably, the tactics **Persistence** and **Impact** perform exceptionally well, with F1-scores of 92% and 93%, respectively.

### Effectiveness of Article De-Duplication

The article de-duplication feature in CYBERDOC significantly enhances the diversity and comprehensiveness of threat summaries, particularly for less popular CVEs.

- **Increased Diversity**: For the **CVEnvd+** group, de-duplication consistently improved the diversity of unique behaviors in threat summaries. Of the analyzed CVEs, 11 demonstrated greater behavior diversity, and 6 showed no reduction in diversity.
- **Impact on Popular CVEs**: In the **CVE2024pop** group, de-duplication had a more varied effect. While summaries for 7 CVEs showed increased diversity and 8 remained unchanged, 2 CVEs exhibited fewer unique behaviors.
- **Detailed Insights**: De-duplication revealed critical details in some cases.

