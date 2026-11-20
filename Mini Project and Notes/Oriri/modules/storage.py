
import json
import os
import tempfile


# ==========================================================
# ORIRI — STORAGE MODULE
# JSON Data Management
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")


class StorageManager:

    def __init__(self, data_directory=DATA_DIR):
        self.data_directory = data_directory

        os.makedirs(
            self.data_directory,
            exist_ok=True
        )

    # ------------------------------------------------------
    # FILE PATH
    # ------------------------------------------------------

    def get_path(self, filename):

        if not filename.endswith(".json"):
            filename += ".json"

        # Only allow filenames, not arbitrary paths.
        if os.path.basename(filename) != filename:
            raise ValueError("Invalid storage filename.")

        return os.path.join(
            self.data_directory,
            filename
        )

    # ------------------------------------------------------
    # LOAD JSON
    # ------------------------------------------------------

    def load_json(self, filename, default=None):

        path = self.get_path(filename)

        if default is None:
            default = {}

        if not os.path.exists(path):
            self.save_json(filename, default)
            return default

        try:
            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return default

    # ------------------------------------------------------
    # SAVE JSON
    # ------------------------------------------------------

    def save_json(self, filename, data):

        path = self.get_path(filename)

        file_descriptor, temporary_path = tempfile.mkstemp(
            dir=self.data_directory,
            prefix=".oriri_",
            suffix=".tmp"
        )

        try:
            with os.fdopen(
                file_descriptor,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            os.replace(temporary_path, path)

        except Exception:
            try:
                os.remove(temporary_path)
            except OSError:
                pass

            raise

        return True

    # ------------------------------------------------------
    # DELETE JSON
    # ------------------------------------------------------

    def delete_json(self, filename):

        path = self.get_path(filename)

        if os.path.exists(path):
            os.remove(path)
            return True

        return False

    # ------------------------------------------------------
    # CHECK FILE
    # ------------------------------------------------------

    def file_exists(self, filename):

        return os.path.exists(
            self.get_path(filename)
        )

    # ------------------------------------------------------
    # RESET FILE
    # ------------------------------------------------------

    def reset_json(self, filename, default=None):

        if default is None:
            default = {}

        self.save_json(filename, default)

        return default

    # ------------------------------------------------------
    # UPDATE JSON
    # ------------------------------------------------------

    def update_json(self, filename, updates):

        data = self.load_json(filename, {})

        if not isinstance(data, dict):
            raise TypeError(
                "Cannot update JSON because its root is not a dictionary."
            )

        data.update(updates)

        self.save_json(filename, data)

        return data


# ==========================================================
# SHARED STORAGE INSTANCE
# ==========================================================

storage = StorageManager()
