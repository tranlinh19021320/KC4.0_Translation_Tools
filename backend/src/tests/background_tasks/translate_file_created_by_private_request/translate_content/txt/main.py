from inspect import trace
from modules.background_tasks.translate_file_created_by_private_request.translate_content.txt.main import *
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

from modules.translation_request.database.translation_request.repository import TranslationRequestRepository, TranslationRequestEntity, TranslationRequestProps
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository, TranslationRequestResultEntity, TranslationRequestResultProps
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository, TranslationHistoryEntity, TranslationHistoryProps
from modules.system_setting.database.repository import SystemSettingRepository

import asyncio
import aiohttp


from infrastructure.adapters.logger import Logger

from core.utils.file import get_doc_paragraphs, get_full_path
from infrastructure.configs.translation_task import RESULT_FILE_STATUS, AllowedFileTranslationExtensionEnum, FileTranslationTask_NotYetTranslatedResultFileSchemaV1, FileTranslationTask_TranslatingResultFileSchemaV1, FileTranslationTask_TranslationCompletedResultFileSchemaV1, get_file_translation_file_path, get_file_translation_target_file_name
from core.utils.document import check_if_paragraph_has_text, get_common_style

import traceback

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

LIMIT_NUM_CHAR_TRANSLATE_REQUEST = 3000

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
transation_history_repository = TranslationHistoryRepository()
system_setting_repository = SystemSettingRepository()

contentTranslator = ContentTranslator()

logger = Logger(
    'Task: translate_file_created_by_private_request.translate_content.txt')


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


async def test_read_task_result():
    print('=====================test_read_task_result=====================')
    system_setting = await system_setting_repository.find_one({})

    try:
        from core.value_objects.id import ID
        from infrastructure.configs.task import CreatorTypeEnum
        import uuid

        tasks = []
        tasks_result = []
        tasks_history = []

        # Create random tasks
        for i in range(10):
            new_request = TranslationRequestEntity(
                TranslationRequestProps(
                    creator_id=ID(str(uuid.uuid4())),
                    creator_type=CreatorTypeEnum.end_user,
                    task_name=TranslationTaskNameEnum.private_file_translation,
                    step_status=StepStatusEnum.not_yet_processed.value,
                    current_step=TranslationTaskStepEnum.translating_language.value,
                )
            )

            new_task_result_entity = TranslationRequestResultEntity(
                TranslationRequestResultProps(
                    task_id=new_request.id,
                    step=new_request.props.current_step
                )
            )

            new_translation_history_entity = TranslationHistoryEntity(
                TranslationHistoryProps(
                    creator_id=new_request.props.creator_id,
                    task_id=new_request.id,
                    translation_type=TranslationTaskNameEnum.private_file_translation,
                    status=TranslationHistoryStatus.translating.value,
                    file_path=new_task_result_entity.props.file_path
                )
            )

            tasks.append(new_request)
            tasks_result.append(new_task_result_entity)
            tasks_history.append(new_translation_history_entity)

        tasks_result_and_trans_history_req = [
            tasks_result,
            tasks_history
        ]

        tasks_result, translations_history = await asyncio.gather(*tasks_result_and_trans_history_req)

        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks,
            tasks_result=tasks_result,
            translations_history=translations_history
        )

        valid_tasks_id = list(map(lambda t: t, list(valid_tasks_mapper)))
        chunked_tasks_id = list(chunk_arr(valid_tasks_id, 1))

        print('Test run successfully!')

        return (valid_tasks_mapper, invalid_tasks_mapper, chunked_tasks_id)

    except:
        traceback.print_exc()
        print('Test failed!')

    print(
        f'An task translate_file_created_by_private_request.translate_content.txt end in {datetime.now()}\n')


async def test_mark_invalid_tasks():
    print('=====================test_mark_invalid_tasks=====================')
    (_, invalid_tasks_mapper, _) = await test_read_task_result()
    mark_invalid_tasks(invalid_tasks_mapper)


async def test_execute_in_batch():
    print('=====================test_execute_in_batch=====================')
    (valid_tasks_mapper, _, chunked_tasks_id) = await test_read_task_result()
    for chunk in chunked_tasks_id:
        await execute_in_batch(valid_tasks_mapper, chunk, 1)


async def test_main():
    print('========================================')
    # main()
