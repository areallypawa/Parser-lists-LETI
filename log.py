import logging
import os

# Папка для логов

# Название логгера
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)
# Удаление всех обработчиков, если они уже есть
def clear_logger_handlers():
    if logger.hasHandlers():
        logger.handlers.clear()

# Функция настройки логгера
def setup_logger(iteration, egpu):
    log_dir = f'./Точный ЛЭТИ/logs/{egpu}'
    os.makedirs(log_dir, exist_ok=True)


    clear_logger_handlers()  # удаляем предыдущие обработчики
    filename = os.path.join(log_dir, f'log_{egpu}_{iteration}.log')

    handler = logging.FileHandler(filename, mode='w', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    

# Пример цикла
# for i in range(3):
#     setup_logger(i)
#     logger.info(f"Начало итерации {i}")
#     # Твоя логика
#     logger.debug("Что-то происходит...")
#     logger.info(f"Конец итерации {i}")