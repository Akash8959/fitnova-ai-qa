from pathlib import Path


class FolderAdapter:

    SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".m4a"}

    def __init__(self, folder_path: str):
        self.folder = Path(folder_path)

    def get_calls(self):
        calls = []

        for file in self.folder.iterdir():

            if not file.is_file():
                continue

            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            calls.append(
                {
                    "source_id": file.stem,
                    "file_name": file.name,
                    "file_path": str(file.resolve()),
                    "file_type": file.suffix.lower(),
                }
            )

        return calls