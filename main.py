from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from bs4 import BeautifulSoup

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/api/ku_login")
def ku_login(id: str, password: str):
    if id == "" and password == "":
        return HTTPException(
            status_code=400,
            detail="id and password is null"
        )

    elif id == "":
        return HTTPException(
            status_code=400,
            detail="id is null"
        )

    elif password == "":
        return HTTPException(
            status_code=400,
            detail="password is null"
        )

    session = requests.Session()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
    }

    session.post("https://ecampus.konkuk.ac.kr/ilos/lo/logout.acl", timeout=10)

    body = {
        "usr_id": id,
        "usr_pwd": password,
        "campus_div": "1",
        "encoding": "utf-8"
    }

    login_response = session.post(url="https://ecampus.konkuk.ac.kr/ilos/lo/login.acl?data=jsonLogin",
               headers=headers,
               data=body
               )

    login_response_json = json.loads(login_response.text.strip()[11:-2])

    if login_response_json["isError"]:
        if login_response_json["message"] == "ID 또는 비밀번호를 5회이상 잘못 입력하셨습니다. 5분 후에 다시 접속하시기 바랍니다.":
            return HTTPException(
                status_code=403,
                detail="ban for 5 minutes"
            )

        return HTTPException(
            status_code=401,
            detail="incorrect id or password"
        )

    info_response = session.get(
        url="https://ecampus.konkuk.ac.kr/ilos/mp/myinfo_form.acl",
        headers=headers
    )

    info_html = BeautifulSoup(info_response.text, "html.parser")

    tds = []

    for td in info_html.select("td"):
        tds.append(td.text.strip())

    info = {
        "student_number": tds[1][-10:-1],
        "name": tds[1][:-11],
        "contact": tds[4],
        "email": tds[6]
    }

    return HTTPException(
        status_code=200,
        detail=info
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)