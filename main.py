import database_setup
import tasks

if __name__ == "__main__":
    tasks.init_tasks()
    database_setup.init_all_dbs()
