import logging
import psycopg2

class log_handler (logging.Handler):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect("dbname = project1 user = postgres password =  6068 host = localhost port = 5432")
        self.conn.autocommit = True
    
    def emit(self, record):
        try:
            with self.conn.cursor() as cur:
                cur.execute ("INSERT INTO LOGS (level,message) VALUES (%s,%s)",(record.levelname, record.getMessage()))
        except Exception as e:
            print("Logging Failed: ", e)

def get_logger():
    logger = logging.getLogger("PROJECT1")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logs = log_handler()
        logger.addHandler(logs)
        
    return logger