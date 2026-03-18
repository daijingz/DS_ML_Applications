### Project Reflection

#### Strengths

- Provides an intuitive natural language interface for querying complex census data  
- Clean modular architecture separating API, LLM, data, and service layers  
- Real-time integration with Snowflake enables access to large, reliable datasets  
- Transparent pipeline with visible SQL queries improves debuggability and trust  
- Easily extensible design for adding new metrics, geographies, or features  

---

#### Limitations

- Geographic understanding is limited and may misinterpret ambiguous locations (e.g., New York city vs state). It lacks a structured mapping from user input to precise census geographic levels.  
- SQL generation relies on heuristic mapping rather than true semantic parsing. This can produce valid but incorrect queries that do not match user intent.  
- Schema awareness is shallow and tightly coupled to hardcoded column mappings. This makes it difficult to generalize across tables or maintain correctness at scale.  
- The system lacks validation of generated queries and results. It may return confident but incorrect answers without detecting inconsistencies.  
- Conversation context is not effectively maintained across turns. Follow-up queries may lose previously inferred intent such as region or metric.  
- No deployment setup, runs only in local environment. This limits accessibility and real-world usability.  

---

#### Future Improvements

- Introduce a structured geographic resolution layer (e.g., mapping to state, county, tract IDs) to eliminate ambiguity in location queries  
- Replace heuristic SQL generation with a stronger semantic parsing approach using LLM grounding and schema-aware prompting  
- Build a centralized metric and schema catalog to decouple logic from hardcoded column names and improve maintainability  
- Add query and result validation checks to ensure outputs align with user intent before generating responses  
- Implement session-based memory to support multi-turn conversations and context-aware follow-up queries  
- Deploy backend and frontend to a cloud platform to enable public access and improve scalability   

