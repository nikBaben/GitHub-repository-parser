from pathlib import Path
from datetime import timedelta

from parser.infrastructure.github.config import settings
from parser.infrastructure.github.clients.client import GitHubClient
from parser.infrastructure.adapters import (
    GitHubRepositoryHistoryAdapter,
    JsonHistoryStorageAdapter
)
from parser.application.ports import (
    RepositoryHistoryPort,
    RepositoryHistoryStoragePort,
    ScoreConfigPort
)
from parser.application.services import (
    CachePolicy,
    HistoryCacheService,
    HistoryCutoffFilter,
    HistoryLoader,
    HistoryMerger,
    HistoryService,
)
from parser.application.use_cases import (
    GetHistoryUseCase,
    СountMetricsRepositoryUseCase
)
from parser.domain.services import(
    CountMetricsService, 
    RepositoryScoringService,
    ScoreConfig
)
from parser.infrastructure.datasets.kaggle_provider import KaggleScoreConfigProvider
from parser.presentation.renders import PlotlyRepositoryDashboardRenderer
from parser.presentation.mappers import HistoryChartMapper
from parser.presentation.ports import RepositoryDashboardRendererPort

class AppContainer:
    """Composition Root."""
    def __init__(
        self,
        github_client: GitHubClient,
        score_dataset_path: str | Path = "data/csv/kaggle/github_repos.csv",
    ) -> None:
        self._github_client = github_client
        self._score_dataset_path = Path(score_dataset_path)

    def repository_history(self) -> RepositoryHistoryPort:
        return GitHubRepositoryHistoryAdapter(self._github_client)

    def history_storage(self) -> RepositoryHistoryStoragePort:
        return JsonHistoryStorageAdapter()

    def history_loader(self) -> HistoryLoader:
        return HistoryLoader(
            repository_history=self.repository_history(),
        )

    def history_cache_service(self) -> HistoryCacheService:
        return HistoryCacheService(
            storage=self.history_storage(),
            cache_policy=self.cache_policy(),
        )

    def history_merger(self) -> HistoryMerger:
        return HistoryMerger()

    def history_cutoff_filter(self) -> HistoryCutoffFilter:
        return HistoryCutoffFilter()

    def history_service(self) -> HistoryService:
        return HistoryService(
            loader=self.history_loader(),
            cache=self.history_cache_service(),
            merger=self.history_merger(),
            cutoff_filter=self.history_cutoff_filter(),
        )

    def score_config_provider(self) -> ScoreConfigPort:
        return KaggleScoreConfigProvider(
            csv_path=self._score_dataset_path,
            percentile=0.99,
        )
    
    def count_metrics_service(self) -> CountMetricsService:
        return CountMetricsService()
    
    def scoring_service(self) -> RepositoryScoringService:
        score_config = self.score_config_provider().get_config()
        return RepositoryScoringService(config=score_config)
    
    def cache_policy(self) -> CachePolicy:
        return CachePolicy(
            ttl=timedelta(seconds=settings.HISTORY_CACHE_TTL_SECONDS),
        )

    def get_history_use_case(self) -> GetHistoryUseCase:
        return GetHistoryUseCase(
            service=self.history_service(),
        )   

    def analytics_use_case(self) -> СountMetricsRepositoryUseCase:
        return СountMetricsRepositoryUseCase(
            count_metrics_service = self.count_metrics_service(),
            scoring_service = self.scoring_service(),
        )
    
    def repository_dashboard_renderer(self) -> RepositoryDashboardRendererPort:
        return PlotlyRepositoryDashboardRenderer() 

    