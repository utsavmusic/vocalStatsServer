
import logging

"""
# Logging configuration
  Log format:
  > <timestamp> | <log level> | <file path>:<line number> | <message> 
  Log example:
  > 2025-07-03 05:46:00 | INFO | /home/user/myapp/main.py:12 | This log shows the full path and line number!
"""
logging.basicConfig(
    level=logging.DEBUG,  # Set default level to DEBUG to capture all logs
    format="%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(message)s")

def get_logger(name: str) -> logging.Logger:
  return logging.getLogger(name)