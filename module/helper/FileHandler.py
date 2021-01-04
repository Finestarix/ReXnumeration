import tarfile
from tqdm import tqdm


def compress(file_name, file):

    tar = tarfile.open(file_name, mode="w:gz")
    file_data = tqdm(file)
    # for
