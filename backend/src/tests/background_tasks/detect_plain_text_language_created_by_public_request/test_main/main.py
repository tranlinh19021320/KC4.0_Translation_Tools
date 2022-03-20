from modules.background_tasks.detect_plain_text_language_created_by_public_request import main
from modules.system_setting.database.repository import SystemSettingRepository

system_setting_repository = SystemSettingRepository()
async def test_allowed_concurrent_request():
    system_setting = await system_setting_repository.find_one({})
    ALLOWED_CONCURRENT_REQUEST = system_setting.props.language_detection_api_allowed_concurrent_req
    print("ALLOWED_CONCURRENT_REQUEST: ", ALLOWED_CONCURRENT_REQUEST)

def test_main():
    main()

