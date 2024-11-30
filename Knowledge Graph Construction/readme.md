# Knowledge Graph Construction

### Overview
In the **Knowledge Graph Construction** module, we leverage SECDoc to create a security-oriented knowledge graph from Cyber Threat Intelligence (CTI) articles. The system plays a crucial role in identifying hidden behaviors and relationships of cyber threats described across multiple CTI articles. The constructed knowledge graph provides a comprehensive view of security-related entities, such as vulnerabilities (CVEs), attack tactics, and threat groups, along with the relationships between them.

### Key Steps

1. **CTI Sentence Classification**:
   - SECDoc employs RoBERTa classification models for **Sentence Tactic Classification**, which is a critical step in focusing on relevant information in large CTI articles. This model is used to classify sentences into **tactics sentences**, distinguishing those that describe cyber attack techniques from irrelevant content.

2. **Security-Related Entity Recognition**:
   - **Security-related entity recognition** is another essential step where SECDoc identifies critical entities, such as malware names, CVE identifiers, IP addresses, and more. Multiple LLM agents are used to extract security-specific entities from the text, ensuring that key information related to cyber threats is captured efficiently.
   - This step is vital in forming the nodes of the knowledge graph, as it determines which entities (such as malware or CVEs) should be connected within the graph structure. By recognizing these entities with high accuracy, SECDoc ensures that the graph represents real-world cyber threats and their interactions across various CTI articles.

3. **Triple Extraction**:
   - After identifying relevant sentences and security entities, SECDoc extracts knowledge in the form of triples (subject, relation, object) that describe how different entities interact (e.g., "Formbook **is** malware" or "CVE-2024-XXXX **exploits** Windows").
   - Multiple LLM agents collaborate to extract these triples, refining and merging them through a feedback loop. This process ensures the accuracy of the knowledge represented in the graph, with each triple contributing to the relationships between entities like vulnerabilities, tactics, and malware.

4. **Graph Construction**:
   - The knowledge graph is built using the triples extracted from CTI articles. The nodes represent the security-related entities (e.g., CVEs, malware, APT groups), while the edges depict the relationships or interactions (e.g., exploitation, attack behaviors) among these entities.
   - SECDoc uses advanced techniques to ensure consistency across multiple articles, refining connections using vector embeddings to align similar entities. The result is a comprehensive, security-oriented knowledge graph that reveals cross-article correlations.


