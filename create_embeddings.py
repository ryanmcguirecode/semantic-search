from configparser import ConfigParser
from connections import set_openai_key, postgreSQL_connect, postgreSQL_disconnect
from embeddings import get_embedding
from pg import insert_rows, setup_table
import markdown

def get_html_section(text, start_index):
    i = start_index
    j = start_index
    while i < text_length - 1:
        if text[i:i+2] == "</":
            j = i
            while text[j] != ">":
                j += 1
            break
        i += 1
    return text[start_index:j+1].strip(), j+1

def get_chunks(section, chunk_size):
    chunks = []
    i = 0
    text = section.split()
    while i < len(text):
        chunks.append(" ".join(text[i:i+chunk_size]))
        i += chunk_size
    return chunks

CHUNK_SIZE = 100
FILE = "evolution_textbook.md"

table_name = "evolution_embeddings"
schema = {
    "chapter": "INT",
    "subheading": "INT",
    "paragraph": "INT",
    "chunk": "INT",
    "content": "TEXT",
    "embedding": "vector(1536)"
}

config = ConfigParser()
config.read("credentials.ini")

set_openai_key(config)
connection, cursor = postgreSQL_connect(config)
setup_table(connection, cursor, table_name, schema)

text = markdown.markdown(open(FILE).read(), output_format="xhtml")

text_length = len(text)
current_chapter = 0
current_subsection = 0
current_paragraph = 0
start_index = 0
    
new_rows = []
section, start_index = get_html_section(text, start_index)

while section != "":
    if section[:4] == "<h1>":
        current_chapter += 1
        current_subsection = 0
        current_paragraph = 0
    elif section[:4] == "<h2>":
        current_subsection += 1
        current_paragraph = 0
    elif section[:3] == "<p>":
        current_paragraph += 1
        section_text = section[3:-4]
        chunks = get_chunks(section_text, CHUNK_SIZE)
        for current_chunk, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            new_rows.append((current_chapter, current_subsection, current_paragraph, current_chunk, chunk, embedding))
    else:
        print("Error: section not recognized.", section)
        exit()
    
    section, start_index = get_html_section(text, start_index)

column_names = list(schema.keys())
insert_rows(cursor, table_name, column_names, new_rows)
connection.commit()

postgreSQL_disconnect(connection, cursor)