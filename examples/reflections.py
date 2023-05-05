#Python3
import requests
import json
import matplotlib.pyplot as plt
from html.parser import HTMLParser
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import pandas as pd
import dateutil.parser

IMG_PATH='img/'

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


#KEY #canvas key

headers={
    "Authorization": "Bearer "+KEY
}

API_URL='https://canvas.ucsc.edu/api/v1'
#COURSE #canvas course

#LEC_SECTION_ID #canvas section

params={
    'include[]':'total_students'
}


query_url=API_URL+"/courses/"+COURSE
query=requests.request("GET",query_url, headers=headers, params=params)

if (query.status_code==200):
    data=query.json()
    total_students=data['total_students']
else:
    print("Error:"+str(query.status_code))

#assignment_id #canvas assignment

query_url=API_URL+"/courses/"+COURSE+"/assignments/"+assignment_id

query=requests.request("GET",query_url, headers=headers)

if (query.status_code==200):
    data=query.json()
    quiz_id=data['quiz_id']
    unlock_at=data['unlock_at']
    unlock_datetime=dateutil.parser.parse(unlock_at)
else:
    print("Error:"+str(query.status_code))

try:
    query_url=API_URL+"/courses/"+COURSE+"/quizzes/"+str(quiz_id)
    query=requests.request("GET",query_url, headers=headers)
    if (query.status_code==200):
        data=query.json()
        questions=data['question_count']
        quiz_title=data['title']
    else:
        print("Error:"+str(query.status_code))
    query_url=API_URL+"/courses/"+COURSE+"/quizzes/"+str(quiz_id)+"/questions"
    query=requests.request("GET",query_url, headers=headers)
    if (query.status_code==200):
        data_questions=query.json()
    else:
        print("Error:"+str(query.status_code))
except:
    print("Error: No quiz id")

params={
    'include[]':'submission_history',
    'per_page':'50'
}


data_set = []

query_url=API_URL+"/courses/"+COURSE+"/assignments/"+assignment_id+"/submissions"

query=requests.request("GET",query_url,params=params, headers=headers)
if (query.status_code==200):
    data=query.json()
    for quiz in data:
        data_set.append(quiz)
    while query.links['current']['url'] != query.links['last']['url']:
        query=requests.request("GET",query.links['next']['url'], headers=headers)
        if (query.status_code==200):
            data=query.json()
            for quiz in data:
                data_set.append(quiz)
        else:
            print("Error:"+str(query.status_code))
else:
    print("Error:"+str(query.status_code))


#data analysis
columns=['user','submission']
submission_df=pd.DataFrame(columns=columns)
if len(data_set)!=0:
    replies=[]
    for question in range(questions):
        submissions=[]
        times=[]
        if not submission_df.empty:
            submission_df=submission_df.iloc[0:0]
        for quiz in data_set:
            for submission in quiz['submission_history']:
                if not submission['missing']:
                    try:
                        txt=strip_tags(submission['submission_data'][question]['text'].lower())
                        submissions.append(txt)
                        times.append(submission['submitted_at'])
                        submitted_datetime=dateutil.parser.parse(submission['submitted_at'])
                        delta=submitted_datetime-unlock_datetime
                        dict={
                            'user':quiz['user_id'],
                            'submission':delta.total_seconds()
                            #'submission':submission['submitted_at']
                            }
                        submission_df=submission_df.append(dict, ignore_index=True)
                    except:
                        pass
        text=data_questions[question]['question_text']
        dict={
            'text':text,
            'submissions':submissions,
            'times':times
        }
        replies.append(dict)
        print("Number of submissions:" +str(len(submissions)))
        text=" ".join(submissions)
        words=data_questions[question]['question_text'].lower().split(" ")
        stop_words = words + list(STOPWORDS)
        wordcloud = WordCloud(stopwords = stop_words,background_color="white",max_font_size=40, width=600, height=400).generate(text)
        file_name=IMG_PATH+"wordcloud_"+str(question)+".png"
        wordcloud.to_file(file_name)
        submission_df=submission_df.set_index('user')
else:
    print("Empty data set")


columns=['user','total_activity_time','current_score']
grades_df=pd.DataFrame(columns=columns)

query_en=API_URL+"/courses/"+COURSE+"/enrollments"
params={
    'type[]':'StudentEnrollment',
    'per_page':'50'
}
query=requests.request("GET",query_en, headers=headers, params=params)
if (query.status_code==200):
    data=query.json()
    for enrollment in data:
        if str(enrollment['course_section_id'])==LEC_SECTION_ID:
            dict={
                'user':enrollment['user']['id'],
                'total_activity_time':enrollment['total_activity_time'],
                'current_score':enrollment['grades']['current_score']
            }
            grades_df=grades_df.append(dict,ignore_index=True)
    while query.links['current']['url'] != query.links['last']['url']:
        query=requests.request("GET",query.links['next']['url'], headers=headers)
        if (query.status_code==200):
            data=query.json()
            for enrollment in data:
                if str(enrollment['course_section_id'])==LEC_SECTION_ID:
                    dict={
                        'user':enrollment['user']['id'],
                        'total_activity_time':enrollment['total_activity_time'],
                        'current_score':enrollment['grades']['current_score']
                    }
                    grades_df=grades_df.append(dict,ignore_index=True)
        else:
            print("Error:"+str(query.status_code))
    grades_df=grades_df.set_index('user')
else:
    print("Error:"+str(query.status_code))

df=submission_df.merge(grades_df, left_index=True, right_index=True)

df.plot(x='submission', y='current_score', style='o')
file_name=IMG_PATH+"submission_scores.png"
plt.savefig(file_name)
plt.close()

bounded=df['total_activity_time']<1250000

df[bounded].plot(x='total_activity_time', y='current_score', style='o')
file_name=IMG_PATH+"activity_scores.png"
plt.savefig(file_name)
plt.close()

submissions=replies[len(replies)-1]['times']
df = pd.DataFrame(submissions)
df[0]=pd.to_datetime(df[0])
df_local=df[0].dt.tz_convert('US/Pacific')
histo=df_local.groupby([df_local.dt.day,df_local.dt.hour]).count().plot(kind="bar", figsize=(8,6))
file_name=IMG_PATH+"times.png"
plt.savefig(file_name)
plt.close()

n=len(replies[len(replies)-1]['submissions'])
labels = ['Submitted', 'Missing']
sizes = [n,total_students-n ]
explode = (0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
file_name=IMG_PATH+"submissions.png"
plt.savefig(file_name)
plt.close()





#generate html
html="""
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Insights for
"""

html+=quiz_title

html+="""
  </title>
  <meta name="description" content="The HTML5 Herald">
  <meta name="author" content="SitePoint">

   <!-- Latest compiled and minified CSS -->
   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

   <!-- jQuery library -->
   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

   <!-- Latest compiled JavaScript -->
   <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

</head>

<body>
<div class='container'>
  <h1>
  """
html+=quiz_title

html+="""
</h1>
"""

html+="<div class='row'>"
html+="<h3>Submitted</h3>"
html+="<div class='text-center'>"
html+="<a href='"+IMG_PATH+"submissions.png'>"
html+="<img src='"+IMG_PATH+"submissions.png' class='rounded'>"
html+="</a>"
html+="</div>"
html+="</div>"




html+="<div class='row'>"
html+="<h3>Submission times</h3>"
html+="<div class='text-center'>"
html+="<a href='"+IMG_PATH+"times.png'>"
html+="<img src='"+IMG_PATH+"times.png' class='rounded'>"
html+="</a>"
html+="</div>"
html+="</div>"

for question in range(questions):
    html+="<div class='row'>"
    html+="<h3>"+str(question+1)+". "+data_questions[question]['question_text']+"</h3>"
    html+="<div class='text-center'>"
    html+="<a href='"+IMG_PATH+"wordcloud_"+str(question)+".png'"+">"
    html+="<img src='"+IMG_PATH+"wordcloud_"+str(question)+".png'"+" class='rounded'>"
    html+="</a>"
    html+="</div>"
    html+="</div>"



html+="<div class='row'>"
html+="<h3>Submission times and Current score</h3>"
html+="<div class='text-center'>"
html+="<a href='"+IMG_PATH+"submission_scores.png'>"
html+="<img src='"+IMG_PATH+"submission_scores.png' class='rounded'>"
html+="</a>"
html+="</div>"
html+="</div>"


html+="<div class='row'>"
html+="<h3>Total Canvas time and Current score</h3>"
html+="<div class='text-center'>"
html+="<a href='"+IMG_PATH+"activity_scores.png'>"
html+="<img src='"+IMG_PATH+"activity_scores.png' class='rounded'>"
html+="</a>"
html+="</div>"
html+="</div>"


html+="""
</div>
</body>
</html>
"""

f = open('insight.html','w')
f.write(html)
f.close()
