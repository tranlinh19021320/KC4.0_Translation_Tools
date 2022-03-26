

def add_fresh_jobs_1(background_task_scheduler, BACKGROUND_TASKS):
    
    from tests.background_tasks.delete_invalid_task.main import test_get_task_id_from_task_result_file_path_delete_invalid_task
    
    background_task_1_conf = BACKGROUND_TASKS['test_get_task_id_from_task_result_file_path_delete_invalid_task']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_get_task_id_from_task_result_file_path_delete_invalid_task,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler


def add_fresh_jobs_2(background_task_scheduler, BACKGROUND_TASKS):
    from tests.background_tasks.delete_invalid_task.main import  test_main_delete_invalid_task

    background_task_1_conf = BACKGROUND_TASKS['test_main_delete_invalid_task']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_main_delete_invalid_task,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler

def add_fresh_jobs_3(background_task_scheduler, BACKGROUND_TASKS):
    from tests.background_tasks.delete_invalid_task.main import  test_get_to_be_deleted_file_path_delete_invalid_task

    background_task_1_conf = BACKGROUND_TASKS['test_get_to_be_deleted_file_path_delete_invalid_task']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_get_to_be_deleted_file_path_delete_invalid_task,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler