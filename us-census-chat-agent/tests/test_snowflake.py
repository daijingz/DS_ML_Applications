from app.services.snowflake_service import SnowflakeService

svc = SnowflakeService()
result = svc.run_query("SELECT CURRENT_VERSION()")
print(result)