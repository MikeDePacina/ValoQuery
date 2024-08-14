from llama_index.readers.file import CSVReader
from llama_index.core import SimpleDirectoryReader

parser = CSVReader()

file_extractor = {".csv": parser}
csvs = SimpleDirectoryReader("./csvs", file_extractor=file_extractor).load_data()
print(csvs[0])