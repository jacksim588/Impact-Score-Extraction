from sharepoint import SharePoint

def get_supporting_files(file_name,folder_name):

    # get file
    file  = SharePoint().download_file(file_name, folder_name)

    # save file
    with open(folder_name+'//'+file_name, 'wb') as f:
        f.write(file)
        f.close()
        