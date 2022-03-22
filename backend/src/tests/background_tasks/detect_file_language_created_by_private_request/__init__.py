def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):

    # from tests.background_tasks.send_translation_email.main import test_send_email_result_for_text_translation
    # from tests.background_tasks.send_translation_email.main import test_send_email_result_for_file_translation

    background_task_1_conf = BACKGROUND_TASKS['test_detect_file_language_created_by_private_request']

    # if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
    #     background_task_scheduler.remove_job(background_task_1_conf.ID)
	# @@ -17,4 +18,46 @@ def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    # )

    return background_task_scheduler