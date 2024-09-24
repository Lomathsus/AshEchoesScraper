from character import download_characters
from memory_trace import download_memory_traces
from skill import download_skills


def download_all():
    download_characters()
    download_memory_traces()
    download_skills()


download_all()
