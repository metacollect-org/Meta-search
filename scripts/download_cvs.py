import requests

def get():
   response = requests.get('https://docs.google.com/spreadsheet/ccc?key=102ZqoXXyzAJGD4SVEgbFaxvh4RvWvOfTMsYeLU8KYpY&output=csv')
   assert response.status_code == 200, 'Wrong status code'

   with open("output.cvs", "w") as text_file:
       text_file.write(str(response.content))

   text_file.close()
