# adapter/services/dropbox_document_service.py
from typing import List

import requests
from application.interfaces.document_service import DocumentService
from domain.value_objects import DocumentId


class DropboxDocumentSource(DocumentService):
    def get_documents(self, access_token: str) -> List[DocumentId]:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        response = requests.post(
            'https://api.dropboxapi.com/2/files/list_folder',
            headers=headers,
            json={
                'path': '',
                'recursive': False,
                'include_media_info': False,
                'include_deleted': False,
                'include_has_explicit_shared_members': False,
            }
        )
        response.raise_for_status()
        entries = response.json().get('entries', [])
        return [DocumentId(entry['id']) for entry in entries if entry['.tag'] == 'file']
