import requests

url = 'http://localhost:9696/predict'

# fact: popular course
course = {'course_id' : 1009622,
         'is_paid' : 'yes',
         'price' : 80,
         'num_lectures' : 43,
         'level' : 'Beginner Level',
         'content_duration' : 5.5,
         'subject' : 'Graphic Design'
         }

response = requests.post(url, json=course).json()

print(response)