# This module to test async/await

from infrastructure.configs.translation_task import (
    PLAIN_TEXT_TRANSLATION_TASKS, 
    FILE_TRANSLATION_TASKS, 
    TRANSLATION_PRIVATE_TASKS, 
    TRANSLATION_PUBLIC_TASKS
)
from infrastructure.configs.task import (
    TranslationTaskStepEnum, 
    StepStatusEnum
)
from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.system_setting.database.repository import SystemSettingRepository

from modules.background_tasks.send_translation_email.main import send_email_result_for_file_translation
from modules.background_tasks.send_translation_email.main import send_email_result_for_text_translation
from email.message import EmailMessage
import pandas as pd
import random
import pymongo
import asyncio
import warnings
warnings.filterwarnings("ignore")

system_setting_repository = SystemSettingRepository()
translation_request_repository = TranslationRequestRepository()

random.seed(10)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self



def create_content_string_for_file(year, month, day, minute, hour):
    res = f"""
        Xin chào,
            
        Chúng tôi xin gửi bạn kết quả dịch đã được yêu cầu vào {hour} giờ {minute} phút ngày {day}/{month}/{year}.
            
        Trân trọng,
        Nhóm phát triển 
        """
    return res


def get_payload(msg, id, decode):
    attachment = msg.get_payload()[id]
    content = attachment.get_payload(decode=True).decode(decode)
    return content


async def test_send_translation_email():
    system_setting = await system_setting_repository.find_one({})

    print ("Translation API URL: ", system_setting.props.translation_api_url)


def mutation(id):
    if random.random() < 0.5:
        # change length
        strim_len = random.randint(10, len(id) - 1)
        id = id[:strim_len]

        # change character
        pos = random.randint(2, len(id) - 1)
        id = id[:pos] + "." + id[pos + 1:]
        return id
    else:
        if random.random() < 0.5:
            # change length
            strim_len = random.randint(10, len(id) - 1)
            id = id[:strim_len]

            return id
        else:
            # change character
            pos = random.randint(2, len(id) - 1)
            id = id[:pos] + "." + id[pos + 1:]

            return id


def add(df, year, month, day, hour, minute, id, translate_content, filename, type, isCrash=False):
    df = df.append({
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'id': id,
        'type': type,
        'translate_content': translate_content,
        'filename': filename,
        'isCrash': isCrash,
        'result': False,
        'reason': ''
    }, ignore_index=True)
    return df


def reformat(df):
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['day'] = df['day'].astype(int)
    df['hour'] = df['hour'].astype(int)
    df['minute'] = df['minute'].astype(int)
    return df


def test_generator(candidate_uuid, type):
    df = pd.DataFrame()

    # gen correct input test for uuid
    for id in candidate_uuid:
        df = add(df, 2021, 12, 2, 10, 30, id, "", "", type, False)

    # gen incorrect input test for uuid
    for i in range(2):
        for id in candidate_uuid:
            df = add(df, 2021, 12, 2, 10, 30, mutation(id), "", "", type, True)
            df = add(df, 2021, 12, 2, 10, 30, mutation(id), "", "", type, True)

    # gen test for datetime
    # year
    years = [-1000, 1990, 2023, 100000]
    for year in years:
        df = add(df, year, 12, 2, 10, 30, candidate_uuid[0], "", "", type, False)

    # month
    months = [0, 13]
    for month in months:
        df = add(df, 2021, month, 2, 10, 30, candidate_uuid[0], "", "", type, False)

    # day
    days = [0, 32]
    for day in days:
        df = add(df, 2021, 12, day, 10, 30, candidate_uuid[0], "", "", type, False)

    # hour
    hours = [0, 25]
    for hour in hours:
        df = add(df, 2021, 12, 2, hour, 30, candidate_uuid[0], "", "", type, False)

    # minute
    mins = [0, 60]
    for min in mins:
        df = add(df, 2021, 12, 2, 10, min, candidate_uuid[0], "", "", type, False)
    # gen test complete
    
    # change number columns to int columns
    df = reformat(df)

    print("Total test generated: ", len(df))

    return df


async def test_send_email_result_for_file_translation():
    print('========== START TEST SEND EMAIL RESULT FILE TRANSLATION =============')

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
                }
            },
            order_by=[('created_at', pymongo.ASCENDING)]
        )

    print ("Length of current tasks: ", len(tasks))

    candidate_uuid_file = []

    for task in tasks:
        if task.props.task_name in FILE_TRANSLATION_TASKS:
            candidate_uuid_file.append(task.id.value)

    df = test_generator(candidate_uuid_file, "file")

    result = pd.DataFrame()

    for i, item in df.iterrows():
        # create mock task

        task = AttrDict({
            'created_at': AttrDict({
                'value': AttrDict({
                    'year': item['year'],
                    'month': item['month'],
                    'day': item['day'],
                    'minute': item['minute'],
                    'hour': item['hour']
                })
            }),
            'id': AttrDict({
                'value': item['id']
            })
        })

        # create mock msg
        msg = EmailMessage()

        msg['Subject'] = f'Kết quả dịch #'
        msg['To'] = "send@gmail.com"
        msg['From'] = "receive@gmail.com"

        isOK = True

        try:
            return_msg = await send_email_result_for_file_translation(task, msg)

            content = get_payload(return_msg, 0, 'utf-8')[:-1]
            content2 = create_content_string_for_file(item['year'], item['month'], item['day'], item['minute'], item['hour'])

            if content != content2:
                isOK = False
                df.loc[i]['result'] = isOK
                df.reason[i] = "content difference"

            if item['isCrash']:
                isOK = False
                df.reason[i] = "not crash"
        except Exception as e:
            if item['isCrash']:
                isOK = True
            else:
                isOK = False
                df.reason[i] = e         
            

        df.result[i] = isOK

    save_path = 'src/tests/background_tasks/send_translation_email/tests/test_send_email_result_for_file_translation.csv'

    df.to_csv(save_path)
    print('========== DONE TEST SEND EMAIL RESULT FILE TRANSLATION =============')
    print('== Test content and result is logged at: ', save_path)


