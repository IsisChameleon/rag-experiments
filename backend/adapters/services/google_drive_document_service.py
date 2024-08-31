from typing import List

import requests
from application.interfaces.document_service import DocumentService
from domain.value_objects import DocumentId


class GoogleDriveDocumentService(DocumentService):
    def get_documents(self, access_token: str) -> List[DocumentId]:
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(
            'https://www.googleapis.com/drive/v3/files',
            headers=headers,
            params={
                'pageSize': 1000,
                'fields': 'files(id, name)',
            }
        )
        response.raise_for_status()
        files = response.json().get('files', [])
        return [DocumentId(file['id']) for file in files]
