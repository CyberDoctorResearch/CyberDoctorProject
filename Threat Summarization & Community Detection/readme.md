# Threat Summarization & Community Detection
## Threat Summarization
CYBERDOC provides an LLM-based approach to generating concise and comprehensive threat summaries from knowledge graph. By leveraging the knowledge graph built in the previous phase, CYBERDOC ensures that its threat summaries are both contextually rich and security-focused. The threat summarization process involves the following steps:

Relevant Edge Filtering: CYBERDOC employs a summarization agent to filter out edges that are not directly related to the threat's characteristics or behaviors. This ensures that only meaningful and relevant information is included in the summary.

Iterative Expansion: The summarization agent iteratively expands the edge network by analyzing nodes connected to the threat and their relationships. It identifies intermediate nodes up to five hops away to ensure comprehensive coverage of the threat’s behaviors and associations.

Summary Composition: Using the refined edge network, CYBERDOC generates a structured and detailed summary that highlights key characteristics and behaviors of the cyber threat, focusing on relationships and behaviors unique to the target entity.

## Community Detection

To further explore the relationship between different entities in the graph, CYBERDOC has a new community detection algorithm that uses the security information provided by the article model and the sentence models to achieve security-oriented community detection and filtering. It has ffollowing steps:

- Type-based Grouping. CYBERDOC checks each entity’s type assigned during the triple extraction step, and applies the Louvain algorithm on only the security-related entities to identify a group of entities that belong to the same type.
- Community Fusion. CYBERDOC merges the names of entities in each community into a single sentence, using the BERTencoder layer in the tactics model to compute theembedding vectors of the community. Then CYBERDOC computes the cosine similarities for each pair of vectors, and mergesthe community pairs whose vector similarity is greater than adefined threshold.
- Community Filtering. CYBERDOC applies the following rules to filter out the communities that are not closely security-related.
  
In the community detection step, CYBERDOC uses the following rules to filter the communities:
- Number of Source Articles: The source sentences of a community's edges must be from at least 2 articles.
- Type of Source Article: All the source articles of a community must be classified as CTI articles.
- Tactics Sentences: The source sentences of a community's edges contain at least three types of tactics.

## Evaluation
We evaluate the performance of the community detection algorithm by comparing the results with core expansion, Lpanni, Leiden, Umstmo, and Angle. The results show that CYBERDOC outperforms the other algorithms in terms of average articles related to community, average correlated security entity number, and precision of community edges. THe following table shows that CYBERDOC can more accurately detect the communities that are closely related to security. Also the community detected by CYBERDOC has more correlated security entities and articles than the other algorithms.
![Alt text](https://i.imgur.com/j93JoOk.png)
