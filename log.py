import logging
import os
from time import strftime
from datetime import datetime
# Папка для логов

# Название логгера
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)
dt = datetime.now().strftime("%d-%m-%H-%M")

# Удаление всех обработчиков, если они уже есть
def clear_logger_handlers():
    if logger.hasHandlers():
        logger.handlers.clear()

# Функция настройки логгера
def setup_logger(iteration, egpu, **kwargs):
    flag = kwargs.get('flag')

    log_dir = f'./logs/{dt}/{egpu}'
    os.makedirs(log_dir, exist_ok=True)

    clear_logger_handlers()  # удаляем предыдущие обработчики

    if flag:
        filename = os.path.join(log_dir, f'Result_{egpu}.log')
    else:
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