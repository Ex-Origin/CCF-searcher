#!/usr/bin/python3

from flask import Flask, request, make_response, render_template
import json
import pandas as pd

app = Flask(__name__)

df = None

@app.route("/", methods = ['GET', 'POST'])
def home_page():
    return render_template('index.html')

@app.route("/api/search", methods=["post"])
def api_utilization():
    title = request.form.get('title')
    if(title):
        res = {"info": "success", "data":[]}
        if(hash(title)):
            result = df[df['hash'] == hash(title)][
                ["year", "title", "doi", "authors", "ccf_rank", "abbreviation", "ccf_name", "full_name", "publisher"]
            ]
            for i in range(len(result)):
                res['data'] += [result.iloc[i].to_json()]
        response = make_response(json.dumps(res))
        response.headers["Content-Type"] = "application/json"
    else:
        res = {"info": "failed", "data": "Unknown parameter \"title\""}
        response = make_response(json.dumps(res))
        response.headers["Content-Type"] = "application/json"
    return response

def hash(s):
    s = s.lower()
    r = ''
    for v in s:
        if(v >= 'a' and v <= 'z'):
            r += v
    return r

def hash_all(s):
    title_list = s['title'].values.tolist()
    hash_list = []
    for i in range(len(title_list)):
        hash_list += [hash(title_list[i])]
    s['hash'] = hash_list

def main():
    app.run(port=9031, host='0.0.0.0')

if __name__ == "__main__":
    df = pd.DataFrame(json.loads(open('dblp_crawler_output.json', 'r').read()), 
        columns=["year", "title", "doi", "authors", "ccf_rank", "abbreviation", "ccf_name", "full_name", "publisher"])
    hash_all(df)
    main()
