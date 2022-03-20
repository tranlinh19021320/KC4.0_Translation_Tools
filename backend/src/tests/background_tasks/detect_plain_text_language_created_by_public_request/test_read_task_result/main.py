from modules.background_tasks.detect_plain_text_language_created_by_public_request.main import read_task_result
import pymongo
import asyncio
from uuid import UUID
from infrastructure.configs.task import (
    LanguageDetectionTaskStepEnum,
    LanguageDetectionTaskNameEnum,
    StepStatusEnum
)
from modules.language_detection_request.database.language_detection_request.repository import LanguageDetectionRequestRepository, LanguageDetectionRequestEntity
from modules.language_detection_request.database.language_detection_request_result.repository import LanguageDetectionRequestResultRepository, LanguageDetectionRequestResultEntity
from modules.language_detection_request.database.language_detection_history.repository import LanguageDetectionHistoryRepository, LanguageDetectionHistoryEntity
from modules.system_setting.database.repository import SystemSettingRepository



language_detection_request_repository = LanguageDetectionRequestRepository()
system_setting_repository = SystemSettingRepository()
language_detection_request_result_repository = LanguageDetectionRequestResultRepository()
language_detection_history = LanguageDetectionHistoryRepository()
async def test_read_task_result():
    tasks = await language_detection_request_repository.find_many(
        params=dict(
            task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value,
            current_step=LanguageDetectionTaskStepEnum.detecting_language.value,
            step_status=StepStatusEnum.not_yet_processed.value
        ),
        limit=1,
        order_by=[('created_at', pymongo.ASCENDING)]
    )
    

    tasks_id = list(map(lambda task: task.id.value, tasks))
    tasks_result_and_trans_history_req = [
            language_detection_request_result_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    },
                    step=LanguageDetectionTaskStepEnum.detecting_language.value
                )
            ),
            language_detection_history.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    }
                )
            )
        ]

    tasks_result, language_detections_history = await asyncio.gather(*tasks_result_and_trans_history_req)
    
    valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks, 
            tasks_result=tasks_result,
            language_detections_history=language_detections_history
    )

    print("valid_tasks_mapper of read_task_result function:", valid_tasks_mapper)
    print("invalid_tasks_mapper of read_task_result function:", invalid_tasks_mapper)


    

