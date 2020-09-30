import dask.dataframe as dd


"""
from gcsfs import GCSFileSystem
from distributed import Client

gcs = GCSFileSystem(project='gothic-space-289008')
gcs.ls('ac295_rberi')
client = Client()
"""


PATH = "/data/metadata.csv"


def simpleQuery(name, path=PATH, username=None, password=None):
    """
    This function searches for the string value contained in "name" variable for a match in the image name in the
    meta data and returns the data-frame of image meta-data wherever image name contains such a string.
    
    Input:
    :string name:
        String containing part or full name of the painting
    :string PATH:
        String containing the path of the meta data file
    :string username:
        String containing the username information to access the database
    :string password:
        String containing the password information to access the database
    
    Return:
    :dask data-frame df:
        Dask data-frame containing the meta-data information of the images where image name contains the string in the
            variable "name"
    """
    
    df = dd.read_csv(path)
    df = df.loc[df['Title'].str.contains(pat=name, case=False, na=False, regex=False)]
    
    return df.compute()


def multiQuery(names, path=PATH, username=None, password=None):
    """
    This function searches for the string value contained in "name" variable for a match in the image name in the
    meta data and returns the data-frame of image meta-data wherever image name contains such a string.
    
    Input:
    :string name:
        String containing single or multiple string values identifying different attributes of the painting
    :string PATH:
        String containing the path of the meta data file
    :string username:
        String containing the username information to access the database
    :string password:
        String containing the password information to access the database
    
    Return:
    :dask data-frame df:
        Dask data-frame containing the meta-data information of the images where image attributes match the string
            values in the variable "name"
    """
    
    punctuation = [
        ',', ':', ';', '.', '|', '/', '(', ')', '!', '%', '$',
        '^', '"', '#', '-', '_', '+', '=', '[', ']', '{', '}'
    ]
    
    for item in punctuation:
        names = names.replace(item, ' ')
    names = names.split()
    
    # Read the data as series i.e. every row is single cell
    ser = dd.read_csv(path, sep='\n')
    
    # Search for rows which contains all the words supplied and build the mask
    mask = ser[ser.columns[0]].str.contains(pat=names[0], case=False, na=False, regex=False)
    for i in range(1, len(names)):
        mask = mask & ser[ser.columns[0]].str.contains(pat=names[i], case=False, na=False, regex=False)
    
    # Read the data as data frame and apply the mask
    df = dd.read_csv(path)
    df = df.loc[mask]
    
    return df.compute()

if __name__ == '__main__':
    print(simpleQuery("Sea"))
    print(multiQuery("Sea"))
    print(multiQuery("Sea, paint boat"))



