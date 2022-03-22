from modules.background_tasks.detect_file_language_created_by_private_request.main \
    import read_task_result, mark_invalid_tasks, execute_in_batch


async def test_read_task_result():
    task_result = []
    tasks = []
    language_detections_history = []
    read_task_result(task_result, tasks, language_detections_history)

async def test_mark_invalid_tasks():
    invalid_task_mapper = []
    mark_invalid_tasks(invalid_task_mapper)

async def test_execute_in_batch():
    valid_tasks_mapper = []
    tasks_id = None
    allowed_concurrent_request = None
    execute_in_batch(valid_tasks_mapper, tasks_id, allowed_concurrent_request)
