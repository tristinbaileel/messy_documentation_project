"""
Doc Log solo va a modificar un archivo que diga cuales fueron los archivos documentados 
y el numero de snippets documentados, archivos eliminados, y snippets eliminados el commit hash especificado (usar el hash resumido) 

1. debe verificar si existe el doc log en la carpeta raiz del proyecto
"""
from pathlib import Path
from snippet_storage import SnippetStorage
from git_manager import GitManager
from textwrap import dedent
from git_retrieaver import GitRetrieaver
# snippets to delete no tiene en cuenta los archivos eliminados

class DocLog:
    @staticmethod
    def create_doc_log():
        desired_path = DocLog.get_doc_log_path()
        desired_path.touch()

    @staticmethod
    def update_doc_log(
        snippets_to_doc: SnippetStorage, snippets_to_delete: SnippetStorage
    ):
        DocLog.create_doc_log()
        num_snippets_to_doc = len(snippets_to_doc)
        num_snippets_to_delete = len(snippets_to_delete)
        head_commit_hash: str = GitManager.head_commit().short_id
        new_log_message = dedent(
        f"""
        COMMIT_HASH:{head_commit_hash}
        NUMBER_OF_SNIPPETS_TO_DOC:{num_snippets_to_doc}
        NUMBER_OF_SNIPPETS_TO DELETE:{num_snippets_to_delete}
        """
        )
        doc_log_path = DocLog.get_doc_log_path()
        original_log_content = doc_log_path.read_text()
        doc_log_path.write_text(new_log_message + original_log_content)

    @staticmethod
    def exists_doc_log() -> bool:
        desired_path = Path("./doc.log")
        try:
            GitManager.select_front_commit()
            GitRetrieaver.get_file_git_object(desired_path)
            return True
        except Exception:
            return False

    @staticmethod
    def get_doc_log_path() -> Path:
        return Path("./doc.log")
