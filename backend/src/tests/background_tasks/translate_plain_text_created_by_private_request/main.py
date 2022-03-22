# from email.mime import image
import pandas

from modules.background_tasks.translate_plain_text_created_by_private_request.translate_content.main import read_task_result


def test_read_task_result():
    df = pandas.read_csv('/home/tj/Kiểm thử đảm bảo chất lượng phần '
                         'mềm/KC4.0_Translation_Tools/backend/src/tests/background_tasks'
                         '/translate_plain_text_created_by_private_request/sample_data/task_file_data.csv')
    read_task_result([], [], [])
    print("=== Test read_task_result ===")


def test_mark_invalid_tasks():
    print("=== Test mark_invalid_tasks ===")


def test_execute_in_batch():
    print("=== Test execute_in_batch ===")


def test_main():
    print("=== Test main ===")
    # try:
    #     # main()
    # except Exception as e:
    #     print(e)
    #     print('===================FAIL===================')
