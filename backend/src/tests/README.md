*Môi trường: Ubuntu 20.04*

### Nơi thực hiện viết các ca kiểm thử

``` sh
#/backend/src/tests
```

### Nơi thêm mới cấu hình cho các background_jobs mới

``` sh
#/backend/src/infrastructure/configs/main.py#TEST_BACKGROUND_TASKS
```

### 

### Khởi chạy các ca kiểm thử

``` sh
#/backend/
$ python3 src/server.py run-test -p 8001
```