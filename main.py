# Settings
utterances_repo = "absucc/c-xkcd"
host = "0.0.0.0"
port = "8080"


__version__ = "2.1 (Lite)"
from flask import Flask, render_template, request
import urllib3
import json
import os
import random
app = Flask("XKmodern")
http = urllib3.PoolManager()

def clean():
  os.system("cls" if os.name=="nt" else "clear")
clean()

@app.route("/", methods=["GET"])
def xkcdreader():
  clean()
  if request.method == "GET":
    lastcomic = http.request('GET', 'https://xkcd.com/info.0.json')
    lccode = json.loads(lastcomic.data.decode('utf-8'))
    numberz = request.args.get("num")
    if numberz is not None:
      clean()
      return "<meta http-equiv=\"refresh\" content=\"0;url=/" + numberz + "\">"
    else:
      clean()
      return "<meta http-equiv=\"refresh\" content=\"0;url=/" + str(lccode["num"]) + "\">"

@app.route("/<path:num>")
def numreal(num):
    clean()
    lastcomic = http.request('GET', 'https://xkcd.com/info.0.json')
    lccode = json.loads(lastcomic.data.decode('utf-8'))
    numberz = num
    @app.errorhandler(500)
    def err5002(error):
      clean()
      return render_template("error.html", **locals(), numcomic=str(lccode["num"]), random_num=str(random.randint(1, lccode["num"])), booktitle="This comic wasn't found"),500
    clean()
    jdat = http.request("GET", "https://xkcd.com/" + numberz + "/info.0.json")
    jsdata = json.loads(jdat.data.decode("utf-8"))
    if jsdata["num"] == lccode["num"]: last = "/" + str(lccode["num"]) + "#"
    else: last = "/" + str(jsdata["num"] + 1)
    if jsdata["num"] == 1: back="1#"
    else: back=jsdata["num"] - 1
    if jsdata["num"] == 1608: fimage = "No image"
    else: fimage = jsdata["img"]
    return render_template("reader.html", **locals(), numcomic=str(lccode["num"]), comic=fimage, title=jsdata["title"], booktitle=jsdata["title"], not_the_last=back, the_last=last, alt=jsdata["alt"], thiscomic=str(jsdata["num"]), thedate=jsdata["month"]+"/"+jsdata["day"]+"/"+jsdata["year"], urlbase=request.base_url, random_num=str(random.randint(1, lccode["num"])), utes_repo=utterances_repo, search_action="/")

@app.route("/random")
def randomcomic():
  clean()
  lastcomic = (http.request('GET', 'https://xkcd.com/info.0.json'))
  lccode = (json.loads(lastcomic.data.decode('utf-8')))
  return """<meta http-equiv="refresh" content="0;url=/?num=""" + str(random.randint(1, lccode["num"])) + """\">"""

if __name__ == "__main__":
  clean()
  app.run(debug=False, host=host, port=port)
  clean()
