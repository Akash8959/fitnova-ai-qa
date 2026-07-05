from app.services.ingestion.folder_adapter import FolderAdapter

adapter = FolderAdapter("sample_calls")

files = adapter.get_audio_files()

print(files)