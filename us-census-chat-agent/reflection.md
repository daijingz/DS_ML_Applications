\### Project Reflection



\#### Strengths

\- Provides an intuitive natural language interface for querying complex census data  

\- Clean modular architecture separating API, LLM, data, and service layers  

\- Real-time integration with Snowflake enables access to large, reliable datasets  

\- Transparent pipeline with visible SQL queries improves debuggability and trust  

\- Easily extensible design for adding new metrics, geographies, or features  



\---



\#### Limitations

\- Geographic understanding is limited and may fail for complex or ambiguous queries  

\- SQL generation relies on heuristic mapping rather than full semantic understanding  

\- Limited error handling for invalid queries or missing data scenarios  

\- Performance depends on Snowflake query latency and network conditions  

\- No deployment setup, runs only in local environment  

\- Minimal frontend features and lacks advanced UI/UX improvements  



\---



\#### Future Improvements

\- Enhance intent parsing with more robust NLP or fine-tuned models  

\- Improve geographic resolution (county, zip code, multi-region queries)  

\- Add caching to reduce repeated query latency  

\- Deploy backend and frontend to cloud for public access  

\- Improve frontend experience with better visualization and interaction  

\- Add more comprehensive testing and monitoring  

