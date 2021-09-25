from modules.translation_request.domain.entities.translation_history import TranslationHistoryProps

from modules.user.commands.auth.command import AuthCommand
from modules.user.domain.services.auth_service import AuthDService


class AuthService():

    def __init__(self) -> None:
        
        self.__authDService = AuthDService()

    async def create_token(self, command: AuthCommand):

        return await self.__authDService.create_token(command=command)

    async def renew_token():
        pass
    