import logging
import sys

def setup_logger():
    # إعداد التنسيق: وقت الخطأ - مستوى الخطأ - الرسالة
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout) # عرض الأخطاء في سجلات رندر
        ]
    )
    logger = logging.getLogger("INDEX_LOGS")
    return logger

# محرك التنبيه الذكي
def log_critical_error(e):
    logging.error(f"🚨 عطل فني في المحرك: {str(e)}")
