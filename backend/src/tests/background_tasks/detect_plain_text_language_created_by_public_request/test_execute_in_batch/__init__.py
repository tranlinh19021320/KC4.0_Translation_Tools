

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from tests.background_tasks.detect_plain_text_language_created_by_public_request.test_execute_in_batch.main import test_execute_in_batch
    
    background_task_1_conf = BACKGROUND_TASKS['test_execute_in_batch_detect_by_public_request']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_execute_in_batch,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler
    