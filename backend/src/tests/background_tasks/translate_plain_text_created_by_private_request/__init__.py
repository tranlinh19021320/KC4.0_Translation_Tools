

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_read_task_result
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_mark_invalid_tasks
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_execute_in_batch
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_main
    background_task_1_conf = BACKGROUND_TASKS['test_read_task_result']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) is not None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_read_task_result,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler


def add_fresh_jobs2(background_task_scheduler, BACKGROUND_TASKS):
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_read_task_result
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_mark_invalid_tasks
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_execute_in_batch
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_main
    background_task_1_conf = BACKGROUND_TASKS['test_mark_invalid_tasks']

    if background_task_scheduler.get_job(background_task_1_conf.ID) is not None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)

    background_task_scheduler.add_job(
        test_mark_invalid_tasks,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )

    return background_task_scheduler


def add_fresh_jobs3(background_task_scheduler, BACKGROUND_TASKS):
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_read_task_result
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_mark_invalid_tasks
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_execute_in_batch
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_main
    background_task_1_conf = BACKGROUND_TASKS['test_execute_in_batch']

    if background_task_scheduler.get_job(background_task_1_conf.ID) is not None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)

    background_task_scheduler.add_job(
        test_execute_in_batch,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )

    return background_task_scheduler

def add_fresh_jobs4(background_task_scheduler, BACKGROUND_TASKS):
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_read_task_result
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_mark_invalid_tasks
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_execute_in_batch
    from tests.background_tasks.translate_plain_text_created_by_private_request.main import test_main
    background_task_1_conf = BACKGROUND_TASKS['test_main']

    if background_task_scheduler.get_job(background_task_1_conf.ID) is not None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)

    background_task_scheduler.add_job(
        test_main,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )

    return background_task_scheduler
