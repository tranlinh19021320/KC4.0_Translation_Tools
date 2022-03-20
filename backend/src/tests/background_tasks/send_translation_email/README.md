# Module kiểm thử nhóm 13

## Kiểm thử các hàm khác
Để chuẩn bị cho kiểm thử:
1. Đảm bảo trong cơ sở dữ liệu có các document liên quan đến trả kết quả bằng email.
2. Trong /backend/src/infrastructure/configs/main.py, thêm phần sau vào TEST_BACKGROUND_TASKS:
```buildoutcfg
        "test_send_email_result_for_text_translation": BackgroundTask(
            ID="test_send_email_result_for_text_translation",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "test_send_email_result_for_file_translation": BackgroundTask(
            ID="test_send_email_result_for_file_translation",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        )
```
~3. Trong /backend/src/tests/background_tasks/main.py, thêm 

```buildoutcfg
from tests.background_tasks.send_translation_email import <x> as <name>
```
Trong đó, x là:
- **add_fresh_jobs** nếu kiểm thử hàm **send_email_result_for_text_translation**
- **add_fresh_jobs_2** for testing **send_email_result_for_file_translation**

Sau đó, thêm dòng lệnh sau vào cuối file 

```buildoutcfg
new_background_task_scheduler = <name>(new_background_task_scheduler, BACKGROUND_TASKS)
```

**name** là tên mà mình muốn đặt cho hàm.

## Đối với hàm main

1. Sử dụng Robo 3T hoặc các phần mềm cho phép trực quan tương tác với cơ sở dữ liệu.
2. Đối với các bản ghi trong Collection Task có trường receiver_email khác null, thực hiện thay đổi giá trị của num_sents. Tuy nhiên cách này khiến run-test bị lỗi. Nên đến giờ việc kiểm thử hàm main vẫn không thể đánh giá được.