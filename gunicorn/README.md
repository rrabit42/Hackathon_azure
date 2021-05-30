# Gunicorn+docker로 배포하기  
## Docker 설치  

## Docker 컨테이너 배포(nginx & gunicorn)  
출처 : https://inma.tistory.com/125  

### Dockerfile 작성  
```
# <django_project>/Dockerfile

FROM python:3.6.4
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./ code/
```  
#### (1) FROM python:3.6.4  
* 파이썬 3.6.4 버전을 베이스 이미지로 사용합니다.  

#### (2) RUN mkdir /code  
* 컨테이너에 /code 디렉토리를 생성합니다.  

#### (3) WORKDIR /code  
* /code 디렉토리로 워킹 디렉토리를 변경합니다.  

#### (4) ADD requirements.txt /code/  
* 로컬 위치의 requirements.txt 파일을 /code 디렉토리 하위로 복사합니다.  

#### (5) RUN pip install -r requirements.txt  
* 프로젝트에 필요한 파이썬 패키지를 설치합니다.  

#### (6) ADD ./ code/  
* 로컬 위치의 모든 파일 및 디렉토리를 /code/ 디렉토리 하위로 복사합니다.  


```
FROM python:3

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

# download wait-for-it
RUN mkdir /script
RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh > /script/wait-for-it.sh
RUN ["chmod", "+x", "/script/wait-for-it.sh"]

# copy project
COPY . /app/
```  

#### (+) wait-for-it.sh  
* 호스트 및 TCP 포트의 가용성을 기다리는 순수한 bash 스크립트입니다.  
연결된 Docker 컨테이너와 같은 상호 의존적인 서비스의 spin-up을 동기화하는 데 유용합니다.  
순수한 bash 스크립트이기 때문에 외부 종속성이 없습니다.  


### docker-compose.yml 작성  
* docker-compose를 활용하여 Dockerfile을 build할 준비를 합니다.  

```
# <django_project>/docker-compose.yml

version '3'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
```  

#### (1) version  
* docker compose 정의 파일의 버전  

#### (2) services
* 서비스 정의  

#### (3) web  
* 서비스명  

#### (4) build
* 빌드 지정  

#### (5) context
* Dockerfile이 있는 디렉토리의 경로  

#### (6) dockerfile
* 도커 파일명  

#### (7) command  
* 컨테이너 안에서 작동하는 명령 지정
* 베이스 이미지에 지정되어있을 경우 덮어 씁니다.  

#### (8) volumes  
* 컨테이너에 볼륨을 마운트합니다.  

#### (9) ports
* 컨테이너가 공개하는 포트는 ports로 지정합니다.
* <호스트 머신의 포트번호>:<컨테이너의 포트번호>

```
version: '3'

services:
  db:
    image: mysql:5.7
    command: --character-set-server=utf8 --collation-server=utf8_general_ci
    restart: always
    env_file:
      - .env
    environment:
      - MYSQL_DATABASE=hearo
      - MYSQL_RANDOM_ROOT_PASSWORD=yes
      - MYSQL_USER=${DB_USERNAME}
      - MYSQL_PASSWORD=${DB_PASSWORD}
    ports:
      - "3306:3306"
#   use this on production
#   expose:
#     - "3306"
    volumes:
      - my-db:/var/lib/mysql

  redis:
    image: redis:6
    ports:
      - "6379:6379"
#   use this on production
#   expose:
#     - "6379"

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./:/app/
      - ./.config/nginx:/etc/nginx/conf.d
      - /static:/static
      - nginx-log:/var/log/nginx
    depends_on:
      - django

  django:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    command: /script/wait-for-it.sh db:3306 -- bash -c "
      python manage.py migrate &&
      python manage.py collectstatic --noinput &&
      gunicorn hearo_api.wsgi -w 4 --bind 0.0.0.0:8000"
    env_file:
      - .env
    expose:
      - "8000"
    volumes:
      - ./:/app/
      - /static:/static
      - app-log:/app/.logs

  mq:
    image: hearo_api_django
    restart: always
    command: celery -A hearo_api worker -l info
    env_file:
      - .env

volumes:
  my-db:
  nginx-log:
  app-log:
```
