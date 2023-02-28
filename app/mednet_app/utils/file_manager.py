import os
import uuid
from werkzeug.utils import secure_filename

class FileManager:
    def __init__(self, upload_path):
        self.upload_path = upload_path

    def get_file_abs_path(self, filename):
        file_abs_path = os.path.join(self.upload_path, filename)
        if os.path.isfile(file_abs_path):
            return file_abs_path
        return None

    def get_all_files_abs_paths(self):
        files_abs_paths = []
        for filename in os.listdir(self.upload_path):
            file_abs_path = self.get_file_abs_path(filename)
            if file_abs_path:
                files_abs_paths.append(file_abs_path)
        return files_abs_paths

    def get_all_files_names(self):
        filenames = []
        for filename in os.listdir(self.upload_path):
            filenames.append(filename)
        return filenames

    def upload_files(self, files_to_upload, valid_extensions= None):
        for file in files_to_upload:
            if file.filename != '':
                file_uuid = str(uuid.uuid4())[:8]
                filename = f"{file_uuid[:8]}_{secure_filename(file.filename)}"
                if valid_extensions:
                    file_ext = os.path.splitext(file.filename)[1]
                    if file_ext not in valid_extensions:
                        raise ValueError('Image does not possess a correct format')
                file.save(os.path.join(self.upload_path, filename))

    def delete_file(self, filename):
        file_abs_path = os.path.join(self.upload_path, filename)
        if os.path.isfile(file_abs_path):
            os.unlink(file_abs_path)

    def delete_all_files(self):
        for filename in os.listdir(self.upload_path):
            self.delete_file(filename)
            
