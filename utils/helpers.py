from pathlib import Path

from config import Config


def load_documents(folder_path: str) -> list[str]:
    """
    Load all .md files from a folder and return raw text.
    """
    folder = Path(folder_path)
    documents = []

    if not folder.exists():
        return documents

    for file in sorted(folder.rglob("*.md")):
        with open(file, "r", encoding="utf-8") as f:
            documents.append(f.read())

    return documents


def chunk_documents(folder_path: str) -> list[dict]:
    """
    Load markdown files, split by ## headings, then by
    CHUNK_SIZE if a section is too long.

    Returns list of {"text": ..., "source": ...}
    """
    folder = Path(folder_path)
    chunks = []

    if not folder.exists():
        return chunks

    for file in sorted(folder.rglob("*.md")):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        source = file.name
        sections = _split_by_headings(content)

        for section in sections:
            section = section.strip()
            if not section:
                continue

            if len(section) <= Config.CHUNK_SIZE:
                chunks.append({
                    "text": section,
                    "source": source
                })
            else:
                # Split long sections into smaller chunks
                sub_chunks = _split_by_size(
                    section,
                    Config.CHUNK_SIZE,
                    Config.CHUNK_OVERLAP
                )
                for sub in sub_chunks:
                    chunks.append({
                        "text": sub,
                        "source": source
                    })

    return chunks


def _split_by_headings(text: str) -> list[str]:
    """
    Split markdown text by ## headings.
    Each section includes its heading.
    """
    lines = text.split("\n")
    sections = []
    current = []

    for line in lines:
        if line.startswith("## ") and current:
            sections.append("\n".join(current))
            current = [line]
        else:
            current.append(line)

    if current:
        sections.append("\n".join(current))

    return sections


def _split_by_size(
    text: str,
    chunk_size: int,
    overlap: int
) -> list[str]:
    """
    Split text into chunks of roughly chunk_size characters
    with overlap.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Try to break at a newline (only if not at end)
        if end < len(text):
            newline_pos = text.rfind("\n", start, end)
            if newline_pos > start:
                end = newline_pos + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # If we've reached the end, stop
        if end >= len(text):
            break

        # Advance, ensuring we always move forward
        next_start = end - overlap
        start = max(next_start, start + 1)

    return chunks