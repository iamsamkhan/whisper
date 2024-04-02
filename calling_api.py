import requests

ans1 = requests.post('http://127.0.0.1:8000/model_answer?question=1')
ans2 = requests.post('http://127.0.0.1:8000/model_text?video=video')
score = requests.post('http://127.0.0.1:8000/get_score?ans1=s1&ans2=c1')
print('*'*100)
print(ans1.text)
print(ans2.text)
print(score.text)
print('*'*100)
