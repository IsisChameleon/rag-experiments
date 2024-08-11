from adapter.event_bus.in_memory_event_bus import InMemoryEventBus
from adapter.services.dropbox_document_service import DropboxDocumentSource
from adapter.services.dropbox_oauth_service import DropboxOAuthService
from adapter.services.google_drive_document_service import GoogleDriveDocumentSource
from adapter.services.google_oauth_service import GoogleOAuthService
from dependency_injector import containers, providers


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    event_bus = providers.Singleton(InMemoryEventBus)

    oauth_service_factory = providers.Selector(
        config.provider,
        google=providers.Factory(GoogleOAuthService),
        dropbox=providers.Factory(DropboxOAuthService),
    )

    document_source_factory = providers.Selector(
        config.provider,
        google=providers.Factory(GoogleDriveDocumentSource),
        dropbox=providers.Factory(DropboxDocumentSource),
    )
