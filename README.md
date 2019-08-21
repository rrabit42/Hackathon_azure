# Hackathon_azure
azure와 docker 이용한 배포

accounts까지 다 만들고 터미널에서
build => 이미지 만드는 명령어
* docker build -t mydjango(이미지명)

uwsgi는 로컬이 아니라 도커 이미지 만드는 과정에서 별개로 생성이 되고 있는 것


그리고
* docker run mydjango(이미지명)
으로 잘 도는지 확인

docker container ls -all 해서 이름 확인하고 제거는 rm으로!

근데 접속을 할 수가 없음 포트를 오픈해줘야함

* docker run --rm -p 8000:80 mydjango

이렇게 돌리자(그리고 삭제는 stop으로도 가능)
