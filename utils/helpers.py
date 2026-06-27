from pathlib import Path


def load_documents(folder_path: str) -> list[str]:
    """
    Load all .txt and .md files from a folder.
    """

    folder = Path(folder_path)

    documents = []

    if not folder.exists():
        return documents

    for file in folder.rglob("*"):

        if file.suffix.lower() not in [".txt", ".md"]:
            continue

        with open(file, "r", encoding="utf-8") as f:
            documents.append(f.read())

    return documents