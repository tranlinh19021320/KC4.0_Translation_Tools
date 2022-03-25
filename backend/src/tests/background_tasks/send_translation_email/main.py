# This module to test async/await

from infrastructure.configs.translation_task import (
    TRANSLATION_PRIVATE_TASKS, 
    TRANSLATION_PUBLIC_TASKS
)
from infrastructure.configs.task import (
    TranslationTaskStepEnum, 
    StepStatusEnum
)
from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.system_setting.database.repository import SystemSettingRepository
from modules.background_tasks.send_translation_email.main import send_email_result_for_text_translation
import pymongo

system_setting_repository = SystemSettingRepository()
translation_request_repository = TranslationRequestRepository()

async def test_send_translation_email():
    system_setting = await system_setting_repository.find_one({})

    print ("Translation API URL: ", system_setting.props.translation_api_url)

async def test_send_email_result_for_text_translation():
    tasks = await translation_request_repository.find_many(
            params={
                'task_name': { '$in': TRANSLATION_PRIVATE_TASKS + TRANSLATION_PUBLIC_TASKS },
                'current_step': TranslationTaskStepEnum.translating_language.value,
                'step_status': {
                    '$in': [
                        StepStatusEnum.completed.value
                    ]
                },
                'receiver_email': {
                    '$ne': None
                },
                'total_email_sent': { '$in': [None, 0] }
            },
            limit=1,
            order_by=[('created_at', pymongo.ASCENDING)]
        )

    print ("Length of current tasks: ", len(tasks))






