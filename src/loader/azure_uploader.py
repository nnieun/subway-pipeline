import os
import json
from datetime import datetime
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from src.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class AzureUploader:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_CONTAINER_NAME")

        if not self.connection_string:
            raise ValueError("AZURE_CONNECTION_STRING 환경변수가 없습니다.")
        if not self.container_name:
            raise ValueError("AZURE_CONTAINER_NAME 환경변수가 없습니다.")

        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def upload_json(self, data: list, folder_name: str, file_name: str) -> bool:
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            blob_path = f"raw/{folder_name}/{today}/{file_name}"

            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_path
            )

            json_string = json.dumps(data, ensure_ascii=False, indent=2)
            blob_client.upload_blob(json_string, overwrite=True)

            logger.info(f"업로드 성공: {blob_path} ({len(data)}건)")
            return True

        except Exception as e:
            logger.error(f"업로드 실패: {e}")
            return False


if __name__ == "__main__":
    uploader = AzureUploader()
    test_data = [{"test": "data", "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
    uploader.upload_json(test_data, "test", "test.json")