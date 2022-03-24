# from email.mime import image
from datetime import datetime
from sqlite3 import Date
from uuid import UUID

import pandas
from tqdm import asyncio
from umongo.frameworks import pymongo

from infrastructure.configs.task import StepStatusEnum
from infrastructure.configs.translation_task import TranslationTaskNameEnum, TranslationTaskStepEnum
from modules.background_tasks.translate_plain_text_created_by_private_request.translate_content.main import (
    read_task_result, mark_invalid_tasks, execute_in_batch, main)
from modules.system_setting.database.repository import SystemSettingRepository
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository
from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.translation_request.database.translation_request_result import TranslationRequestResultRepository
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultEntity


async def test_read_task_result():
    # df = pandas.read_csv('src/tests/background_tasks/delete_invalid_file/sample_data/task_file_data.csv')
    print("=== RUNNINGTest read_task_result ===")

    print("TEST 1\n")
    try:
        # system_setting_repository = SystemSettingRepository()
        # system_setting = await system_setting_repository.find_one({})
        # ALLOWED_CONCURRENT_REQUEST = system_setting.props.translation_api_allowed_concurrent_req
        # translation_request_repository = TranslationRequestRepository()
        # tasks = await translation_request_repository.find_many(
        #     params=dict(
        #         task_name=TranslationTaskNameEnum.private_plain_text_translation.value,
        #         current_step=TranslationTaskStepEnum.translating_language.value,
        #         step_status=StepStatusEnum.not_yet_processed.value,
        #         # expired_date={
        #         #     "$gt": datetime.now()
        #         # }
        #     ),
        #     limit=ALLOWED_CONCURRENT_REQUEST,
        #     order_by=[('created_at', pymongo.ASCENDING)]
        # )
        #
        # tasks_result = []
        # translations_history = []
        # translation_request_result_repository = TranslationRequestResultRepository()
        # tasks_id = list(map(lambda task: task.id.value, tasks))
        # transation_history_repository = TranslationHistoryRepository()
        # tasks_result_and_trans_history_req = [
        #     translation_request_result_repository.find_many(
        #         params=dict(
        #             task_id={
        #                 '$in': list(map(lambda t: UUID(t), tasks_id))
        #             },
        #             step=TranslationTaskStepEnum.translating_language.value
        #         )
        #     ),
        #     transation_history_repository.find_many(
        #         params=dict(
        #             task_id={
        #                 '$in': list(map(lambda t: UUID(t), tasks_id))
        #             }
        #         )
        #     )
        # ]
        # tasks_result, translations_history = await asyncio.gather(*tasks_result_and_trans_history_req)

        tran = TranslationRequestResultEntity()
        tran.id = UUID("660c1f23-6d26-41e8-a5dd-736c44248d0e")
        tran.created_at = Date("2022-03-24T15:26:53.185Z")
        tran.creator_id = None
        tran.task_name = "public_plain_text_language_detection"
        tran.creator_type = "end_user"
        tran.step_status = "closed"
        tran.current_step = "detecting_language"
        tran._cls = "LanguageDetectionRequestOrmEntity"
        tasks = [tran]

        request_res = TranslationRequestResultEntity()
        request_res._id = UUID("377b5a56-51bd-40e7-8b52-73060e5f8c32")
        request_res.created_at = Date("2022-03-24T15:26:53.428Z")
        request_res.updated_at = Date("2022-03-24T15:26:53.428Z")
        request_res.task_id = Date("660c1f23-6d26-41e8-a5dd-736c44248d0e")
        request_res.step = "detecting_language"
        request_res.file_path = "1648110413183__660c1f23-6d26-41e8-a5dd-736c44248d0e.json"
        request_res._cls = "LanguageDetectionRequestResultOrmEntity"

        tasks_result = [request_res]

        tran_history = TranslationHistoryEntity()
        tran_history._id = UUID("76b76d60-2682-4c53-b092-c8262a353dba")
        tran_history.created_at = Date("2022-03-24T15:27:09.865Z")
        tran_history.updated_at = Date("2022-03-24T15:27:10.934Z")
        tran_history.creator_id = None
        # tran_history._id

        translations_history = [tran_history]

        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks,
            tasks_result=tasks_result,
            translations_history=translations_history
        )
        # read_task_result([], [], [])
        print("=== VALID TASKS MAPPER ===\n")
        print(valid_tasks_mapper + "\n")
        print("=== INVALID TASKS MAPPER ===\n")
        print(invalid_tasks_mapper)
        # print("=== Test read_task_result: TRUE  ===")
    except Exception as e:
        # print(e + '\n')
        print("=== Test read_task_result: FALSE ===")

    print("TEST 2\n")
    try:
        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result([], [], [])
        print("=== VALID TASKS MAPPER ===\n")
        print(valid_tasks_mapper + "\n")
        print("=== INVALID TASKS MAPPER ===\n")
        print(invalid_tasks_mapper)
        # print("=== Test read_task_result: TRUE  ===")
    except Exception as e:
        # print(e + '\n')
        print("=== Test read_task_result: FALSE ===")


async def test_mark_invalid_tasks():
    print("=== Test mark_invalid_tasks ===")


async def test_execute_in_batch():
    print("=== Test execute_in_batch ===")


async def test_main():
    print("=== Test main ===")
    # try:
    #     # main()
    # except Exception as e:
    #     print(e)
    #     print('===================FAIL===================')
