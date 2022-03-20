from datetime import datetime
import io
import pickle
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.translation_history import TranslationHistoryStatus
from core.utils.common import chunk_arr
from docx import Document
from typing import List
from uuid import UUID
import pymongo
from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    TranslationTask_TranslationCompletedResultFileSchemaV1, 
    TranslationTask_NotYetTranslatedResultFileSchemaV1, 
    TranslationTaskNameEnum, 
    TranslationTaskStepEnum, 
    StepStatusEnum
)

from infrastructure.adapters.content_translator.main import ContentTranslator 

from modules.translation_request.database.translation_request.repository import TranslationRequestRepository, TranslationRequestEntity
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository, TranslationRequestResultEntity
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository, TranslationHistoryEntity
from modules.system_setting.database.repository import SystemSettingRepository

import asyncio
import aiohttp

from infrastructure.adapters.logger import Logger

from core.utils.file import get_doc_paragraphs, get_full_path
from infrastructure.configs.translation_task import RESULT_FILE_STATUS, AllowedFileTranslationExtensionEnum, FileTranslationTask_NotYetTranslatedResultFileSchemaV1, FileTranslationTask_TranslatingResultFileSchemaV1, FileTranslationTask_TranslationCompletedResultFileSchemaV1, get_file_translation_file_path, get_file_translation_target_file_name
from core.utils.document import check_if_paragraph_has_text, get_common_style

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

LIMIT_NUM_CHAR_TRANSLATE_REQUEST = 3000

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
transation_history_repository = TranslationHistoryRepository()
system_setting_repository = SystemSettingRepository()

contentTranslator = ContentTranslator()

logger = Logger('Task: translate_file_created_by_private_request.translate_content.txt')

from modules.background_tasks.translate_file_created_by_private_request.translate_content.txt.main import *

async def test_read_task_result():
    print('========================================')
    system_setting = await system_setting_repository.find_one({})
    
    ALLOWED_CONCURRENT_REQUEST = system_setting.props.translation_api_allowed_concurrent_req
    
    if ALLOWED_CONCURRENT_REQUEST <= 0: return
    
    tasks = await translation_request_repository.find_many(
        params=dict(
            current_step=TranslationTaskStepEnum.translating_language.value,
            step_status={
                '$in': [
                    StepStatusEnum.not_yet_processed.value,
                    StepStatusEnum.in_progress.value
                ]
            }
        ),
        limit=1,
        order_by=[('created_at', pymongo.ASCENDING)]
    )
        
    if not tasks or not (tasks[0].props.task_name == TranslationTaskNameEnum.private_file_translation.value and \
        tasks[0].props.current_step == TranslationTaskStepEnum.translating_language.value and \
        tasks[0].props.file_type == AllowedFileTranslationExtensionEnum.txt.value and \
        tasks[0].props.step_status in [StepStatusEnum.not_yet_processed.value, StepStatusEnum.in_progress.value]): return

    logger.debug(
        msg=f'New task translate_file_created_by_private_request.translate_content.txt run in {datetime.now()}'
    )

    print(f'New task translate_file_created_by_private_request.translate_content.txt run in {datetime.now()}')
    
    try:
        tasks = await translation_request_repository.find_many(
            params=dict(
                task_name=TranslationTaskNameEnum.private_file_translation.value,
                current_step=TranslationTaskStepEnum.translating_language.value,
                step_status={
                    '$in':[StepStatusEnum.not_yet_processed.value, StepStatusEnum.in_progress.value]
                },
                # expired_date={
                #     "$gt": datetime.now()
                # }
            ),
            limit=ALLOWED_CONCURRENT_REQUEST
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        if len(tasks_id) == 0: 
            logger.debug(
                msg=f'An task translate_file_created_by_private_request.translate_content.txt end in {datetime.now()}\n'
            )
            print(f'An task translate_file_created_by_private_request.translate_content.txt end in {datetime.now()}\n')
            return

        tasks_result_and_trans_history_req = [
            translation_request_result_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    },
                    step=TranslationTaskStepEnum.translating_language.value
                )
            ),
            transation_history_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    }
                )
            )
        ]

        tasks_result, translations_history = await asyncio.gather(*tasks_result_and_trans_history_req)

        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks, 
            tasks_result=tasks_result,
            translations_history=translations_history
        )

        await mark_invalid_tasks(invalid_tasks_mapper)

    except Exception as e:
        logger.error(e)
        
        print(e)

    logger.debug(
        msg=f'An task translate_file_created_by_private_request.translate_content.txt end in {datetime.now()}\n'
    )

    print(f'An task translate_file_created_by_private_request.translate_content.txt end in {datetime.now()}\n')

async def test_mark_invalid_tasks():
    print('========================================')
    mark_invalid_tasks()

async def test_execute_in_batch():
    print('========================================')
    execute_in_batch()

async def test_main():
    print('========================================')
    main()