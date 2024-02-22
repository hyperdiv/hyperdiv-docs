import os
import json
import pathlib

metadata = None
json_path = pathlib.Path(os.path.dirname(__file__), "docs_metadata.json")


def get_docs_metadata():
    global metadata

    if metadata:
        return metadata

    if json_path.exists():
        with open(json_path) as f:
            metadata = json.loads(f.read())
            return metadata
    else:
        from .extractor.main import extract

        metadata = extract()
        return metadata


def create_docs_metadata():
    """
    (Re)-creates the stored JSON file containing docs metadata.
    """
    from .extractor.main import extract

    if json_path.exists():
        os.unlink(json_path)
    data = extract()
    with open(json_path, "w") as f:
        f.write(json.dumps(data, indent=2))
