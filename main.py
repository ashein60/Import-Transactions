import database_handler
import tasks

if __name__ == "__main__":
    tasks.init_tasks()
    database_handler.init_all_dbs()
    # ui.main_loop()
