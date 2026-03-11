# 건국대학교 재학생 인증 API ku-auth
![](https://i.namu.wiki/i/eKnJUBhT_j5ToOnlFN6LyZnjXDH6ABd0CWbO84AJn8U2nw6O2mzx33U-jD-8H2CzeqeZk0BpR7l7breQjGQEKD9s8rXV4ctjf2CgvLoG-nl0iRZVeOJE58yNeR88Zv4abvWyNpwMknIXMR9JkMbYPA.webp)

# 개요
이 API는 [건국대학교 ecampus](https://ecampus.konkuk.ac.kr/)의 로그인 시스템을 활용하여 건국대학교 재학생들을 대상으로 하는 서비스 개발에 유용하게 사용될 수 있도록 개발하였습니다.

# 사용 방법
`/api/ku_login` 주소로 `POST` 요청을 보냅니다. 이때 Body에 다음과 같이`id`와 `password` 값을 `json` 형태로 보냅니다.
```json
{
  "id": "ku",
  "password": "konkuk"
}
```

만일 로그인이 성공하였다면, `200 OK`와 다음과 같은 결과값을 반환하게 됩니다. 이때, 반환된 정보는 ecampus에 등록된 사용자 정보를 반환합니다.
```json
{
  "detail": {
    "student_number": "202612345",
    "name": "김건국",
    "contact": "01012345678",
    "email": "ku@konkuk.ac.kr"
  }
}
```

만일 로그인이 실패하였다면, `401 UNAUTHORIZED`와 다음과 같은 결과값을 반환하게 됩니다.
```json
{
  "detail": "incorrect id or password"
}
```

만일 로그인이 5회 이상 실패하면 ecampus에서 해당 아이디의 로그인을 **5분 동안 정지** 시킵니다. 이때는 `403 FORBIDDEN`과 다음과 같은 결과값을 반환하게 됩니다.
```json
{
  "detail": "ban for 5 minutes"
}
```

만일 `id` 값이 비어있다면, `400 BAD REQUEST`와 다음과 같은 결과값을 반환하게 됩니다. 
```json
{
  "detail": "id is null"
}
```

만일 `password` 값이 비어있다면, `400 BAD REQUEST`와 다음과 같은 결과값을 반환하게 됩니다.
```json
{
  "detail": "password is null"
}
```

만일 `id`와 `password` 값이 동시에 비어있다면, `400 BAD REQUEST`와 다음과 같은 결과값을 반환하게 됩니다.
```json
{
  "detail": "id and password is null"
}
```