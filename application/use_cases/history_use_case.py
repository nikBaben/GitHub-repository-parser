from application.dto import RepositoryHistoryDTO
from application.queries.queries import GetHistoryQuery
from application.services import HistoryService


class GetHistoryUseCase:
    def __init__(self, service: HistoryService) -> None:
        self.service = service

    async def execute(self, query: GetHistoryQuery) -> RepositoryHistoryDTO:
        return await self.service.get_history(query)
