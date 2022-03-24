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
    print("=== Test read_task_result: TRUE ===")
    print("TEST 1\n")
    try:
        tran = TranslationRequestResultEntity()
        tran.id = UUID("660c1f23-6d26-41e8-a5dd-736c44248d0e")
        tran.created_at = Date("2022-03-24T15:26:53.185Z")
        tran.creator_id = None
        tran.task_name = "public_plain_text_language_detection"
        tran.creator_type = "end_user"
        tran.step_status = "closed"
        tran.current_step = "detecting_language"
        tran._cls = "LanguageDetectionRequestOrmEntity"
        print ("-->tran: ")
        print(tran)
        tasks = [tran]

        request_res = TranslationRequestResultEntity()
        request_res._id = UUID("377b5a56-51bd-40e7-8b52-73060e5f8c32")
        request_res.created_at = Date("2022-03-24T15:26:53.428Z")
        request_res.updated_at = Date("2022-03-24T15:26:53.428Z")
        request_res.task_id = Date("660c1f23-6d26-41e8-a5dd-736c44248d0e")
        request_res.step = "detecting_language"
        request_res.file_path = "1648110413183__660c1f23-6d26-41e8-a5dd-736c44248d0e.json"
        request_res._cls = "LanguageDetectionRequestResultOrmEntity"
        print("-->request_result: ")
        print(request_res)
        tasks_result = [request_res]

        tran_history = TranslationHistoryEntity()
        tran_history._id = UUID("76b76d60-2682-4c53-b092-c8262a353dba")
        tran_history.created_at = Date("2022-03-24T15:27:09.865Z")
        tran_history.updated_at = Date("2022-03-24T15:27:10.934Z")
        tran_history.creator_id = None
        tran_history.task_id = UUID("89aa81e5-6dca-4589-afc4-af2f56d9cb9f")
        tran_history.translation_type = UUID("public_plain_text_translation")
        tran_history.status = "translated"
        tran_history.file_path = "1648110429829__89aa81e5-6dca-4589-afc4-af2f56d9cb9f.json"
        # tran_history._id
        print("-->history: ")
        print(tran_history)
        translations_history = [tran_history]

        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks,
            tasks_result=tasks_result,
            translations_history=translations_history
        )
        print("=== Test read_task_result: TRUE ===")
        print("=== VALID TASKS MAPPER ===\n")
        print(valid_tasks_mapper + "\n")
        print("=== INVALID TASKS MAPPER ===\n")
        print(invalid_tasks_mapper)
        print("=== Test read_task_result: TRUE  ===")
    except Exception as e:
        print(e)
        print("=== Test read_task_result: FALSE ===")

    # print("TEST 2\n")
    # try:
    #     valid_tasks_mapper, invalid_tasks_mapper = await read_task_result([], [], [])
    #     print("=== VALID TASKS MAPPER ===\n")
    #     print(valid_tasks_mapper + "\n")
    #     print("=== INVALID TASKS MAPPER ===\n")
    #     print(invalid_tasks_mapper)
    #     # print("=== Test read_task_result: TRUE  ===")
    # except Exception as e:
    #     # print(e + '\n')
    #     print("=== Test read_task_result: FALSE ==="


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
