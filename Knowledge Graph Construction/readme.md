# Knowledge Graph Construction

### Overview
In the **Knowledge Graph Construction** module, we leverage CYBERDOC to create a security-oriented knowledge graph from Cyber Threat Intelligence (CTI) articles. The system plays a crucial role in identifying hidden behaviors and relationships of cyber threats described across multiple CTI articles. The constructed knowledge graph provides a comprehensive view of security-related entities, such as vulnerabilities (CVEs), attack tactics, and threat groups, along with the relationships between them.

### Key Steps

1. **CTI Sentence Classification**:
   - CYBERDOC employs RoBERTa classification models for **Sentence Tactic Classification**, which is a critical step in focusing on relevant information in large CTI articles. This model is used to classify sentences into **tactics sentences**, distinguishing those that describe cyber attack techniques from irrelevant content.

2. **Security-Related Entity Recognition**:
   - **Security-related entity recognition** is another essential step where CYBERDOC identifies critical entities, such as malware names, CVE identifiers, IP addresses, and more. Multiple LLM agents are used to extract security-specific entities from the text, ensuring that key information related to cyber threats is captured efficiently.
   - This step is vital in forming the nodes of the knowledge graph, as it determines which entities (such as malware or CVEs) should be connected within the graph structure. By recognizing these entities with high accuracy, CYBERDOC ensures that the graph represents real-world cyber threats and their interactions across various CTI articles.

3. **Triple Extraction**:
   - After identifying relevant sentences and security entities, CYBERDOC extracts knowledge in the form of triples (subject, relation, object) that describe how different entities interact (e.g., "Formbook **is** malware" or "CVE-2024-XXXX **exploits** Windows").
   - Multiple LLM agents collaborate to extract these triples, refining and merging them through a feedback loop. This process ensures the accuracy of the knowledge represented in the graph, with each triple contributing to the relationships between entities like vulnerabilities, tactics, and malware.

4. **Graph Construction**:
   - The knowledge graph is built using the triples extracted from CTI articles. The nodes represent the security-related entities (e.g., CVEs, malware, APT groups), while the edges depict the relationships or interactions (e.g., exploitation, attack behaviors) among these entities.
   - CYBERDOC uses advanced techniques to ensure consistency across multiple articles, refining connections using vector embeddings to align similar entities. The result is a comprehensive, security-oriented knowledge graph that reveals cross-article correlations.

### Workflow

The following files and scripts in the directory serve specific purposes in the **Knowledge Graph Construction** workflow:

1. **`Article Duplication Dataset.csv`**  
   Contains 1,000 CTI articles related to 100 CVEs from 2024 for building and testing the knowledge graph.

2. **`Article De-duplication Dataset.xlsx`**  
   Documents the results of the article de-duplication process, showing original and filtered CTI articles.

3. **`Knowledge Graph Construction.ipynb`**  
   Jupyter Notebook for constructing the knowledge graph, including classification, entity recognition, and triple extraction.

4. **`LLM AutoEval.ipynb`**  
   Notebook for evaluating the precision and recall of the knowledge graph using automated LLM-based metrics.

5. **`complete_list_of_15079_cves_recorded_in_2024_on_nvd.csv`**  
   Full list of 15,079 CVEs from 2024 used to select and analyze specific CVEs.

6. **`random_sampled_100CVEs_names.pkl`**  
   Stores a random selection of 100 CVEs for focused analysis.

7. **`readme.md`**  
   Project documentation providing an overview, usage instructions, and file descriptions.

### Knowledge Graph Construction

In terms of knowledge graph construction, **CyberDoctor** achieves superior performance with higher recall and F1 scores compared to **GPT-4o** and **GraphRAG**, demonstrating its advanced capability in extracting security-related behaviors and relationships while maintaining high precision.

![image](https://i.imgur.com/HFaHHDN.png)
