

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from background_tasks.translate_file_created_by_private_request.translate_content.txt.main import test_read_task_result, test_mark_invalid_tasks, test_execute_in_batch, test_main
    
    background_task_1_conf = BACKGROUND_TASKS['test_translate_file_created_by_private_request.translate_content.txt']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_read_task_result,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )

    background_task_scheduler.add_job(
        test_mark_invalid_tasks,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )

    background_task_scheduler.add_job(
        test_execute_in_batch,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )

    background_task_scheduler.add_job(
        test_main,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler
    