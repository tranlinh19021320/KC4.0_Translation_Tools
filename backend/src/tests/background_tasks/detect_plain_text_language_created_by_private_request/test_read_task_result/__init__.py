

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from tests.background_tasks.detect_plain_text_language_created_by_private_request.test_read_task_result.main import test_read_task_result
    
    background_task_1_conf = BACKGROUND_TASKS['test_read_task_result_detect_by_private_request']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_read_task_result,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler
    