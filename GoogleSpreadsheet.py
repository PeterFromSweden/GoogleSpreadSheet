from googleapiclient import discovery
from oauth2client import service_account

class GoogleSpreadsheet:
    """description of class"""
    scopes = ["https://www.googleapis.com/auth/drive", 
              "https://www.googleapis.com/auth/drive.file", 
              "https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, filename, templatename):
        self.filename = filename
        self.templatename = templatename
        self.credentials = self.__get_credentials()
        self.fid = self.__open_create();

    def __create_credentials_guide(self):
        print("How to create 'Credentials.json':")
        print("https://console.developers.google.com/apis")
        print("Create/select project in top bar")
        print("Dashboard | Enable APIs and services. Drive & Sheet")
        print("Credentials|Create Service Account Key role=project editor")
        print("Rename json to 'Credentials.json' and put into script folder")

    def __get_credentials(self):
        try:
            return service_account.ServiceAccountCredentials.from_json_keyfile_name(
                'Credentials.json', scopes=self.scopes)
        except OSError as e:
            print(e)
            self.__create_credentials_guide()
            return None
        
    def __open_create(self):
        try:
            # drive api
            service = discovery.build('drive', 'v3', credentials=self.credentials)
            
            # Does template exist?
            source = service.files().list(
                q='name = "' + self.templatename + '"',
                spaces='drive', 
                fields='*',#'nextPageToken, files(id,name)', 
                pageToken=None).execute()
            if len(source['files']) != 1:
                raise Exception("Template file not found")

            # Does file exist?
            destination = service.files().list(
                q='name = "' + self.filename + '"',
                spaces='drive', 
                fields='*', #'nextPageToken, files(id,name)', 
                pageToken=None).execute()
            if len(destination['files']) >= 1:
                #for file in destination['files']:
                #    file_id = file['id']
                #    result = service.files().delete(fileId = file_id).execute()
                #return None
                return destination['files'][0]['id']

            # Make copy of template in same folder
            source_file = source['files'][0]
            new_file_body = {
                'name' : self.filename,
                'parents' : source_file['parents'].copy(),
                }
            new_file = service.files().copy(
                fileId = source_file['id'],
                body = new_file_body).execute()

            # Change owner to owner of template
            permissionId = source_file['owners'][0]['permissionId']
            user_permission_body = { 'role': 'owner'}
            permission = service.permissions().update(
                fileId = new_file['id'],
                permissionId = permissionId,
                transferOwnership=True,
                body = user_permission_body).execute()
            
            return new_file['id']

        except Exception as e:
            print('An error occurred: ', e)
            return None

    def Update(self, sheetname, data):
        try:
            # sheets api
            service = discovery.build('sheets', 'v4', credentials=self.credentials)
            body = { 'values' : data }
            result = service.spreadsheets().values().append(
                spreadsheetId = self.fid, 
                range= sheetname + '!A1:A1',
                valueInputOption='USER_ENTERED', 
                insertDataOption='INSERT_ROWS',
                body=body).execute()                     

        except Exception as e:
            print('An error occurred: ', e)

def main():
    print("GoogleSpreadsheet main")
    gss = GoogleSpreadsheet("Templog Nov", "Templog Template")
    data = [
        ['R1C1', 'R1C2'],
        ['R2C1', 'R2C2']]
    gss.Update("Sheet1", data)
    gss.Update("Sheet2", data)

if __name__ == "__main__":
    main()
