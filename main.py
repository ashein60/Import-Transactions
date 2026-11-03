import database_handler
import tasks
from transactions import transaction_controller

if __name__ == "__main__":
    tasks.init_tasks()
    database_handler.init_all_dbs()
    transaction_controller.import_transactions("data.csv")
