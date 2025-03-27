# MACMORNING - BE

## IngQ Project

### 개발 환경 구축

#### Local 개발 환경 구축 시 docker-compose 사용
1. Docker와 docker-compose 설치(각각 설치 필요)

2. git clone을 통해 해당 repository 내용 로컬로 복사

    ```
    git clone https://github.com/JNU-econovation/MacMorning-BE.git macmorning_be
    ```

3. .env 파일 추가
    
    ![alt text](image-1.png)

    __ingq 디렉터리 XXX, .env 파일 위치 주의!!!__

    5번(도커 컴포즈) 진행하면 mysql 디렉터리는 자동으로 생성됩니다.

    이미지에는 없지만 /ingq 위쪽에 /ai 디렉터리도 있습니다!

4. docker-compose 빌드

    ```
    docker-compose -f docker-compose-local.yml build
    ```

5. docker-compose 실행

    ```
    docker-compose -f docker-compose-local.yml up -d
    ```

6. 실행중인 컨테이너 확인

    ```
    docker ps
    ```

    3개의 서버가 실행중이면 정상 작동

7. 개발 진행