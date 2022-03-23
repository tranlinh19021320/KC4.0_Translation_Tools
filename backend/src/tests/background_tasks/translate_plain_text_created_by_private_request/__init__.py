

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):

    from tests.background_tasks.translate_plain_text_created_by_private_request.main import (
        test_read_task_result, test_mark_invalid_tasks, test_execute_in_batch, test_main)

    background_task_1_conf = BACKGROUND_TASKS['test_translate_plain_text_created_by_private_request.translate_content']


    if background_task_scheduler.get_job(background_task_1_conf.ID) is not None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)

    background_task_scheduler.add_job(
        test_main,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )

    return background_task_scheduler
