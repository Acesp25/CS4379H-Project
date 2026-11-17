import os

# Returns the file path of the project root directory as a 'str'.
def get_project_root() -> str:
    this_file = os.path.abspath(__file__)
    src_dir = os.path.dirname(this_file)
    project_root = os.path.dirname(src_dir)

    return project_root
