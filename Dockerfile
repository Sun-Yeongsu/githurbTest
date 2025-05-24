# 필요한 패키지 설치 및 시스템 업데이트
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    python3-full \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 가상 환경 생성 및 활성화
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 필요한 파이썬 패키지 설치
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY multithreaded_calculation.py .

# 컨테이너 실행 시 파이썬 스크립트 실행
CMD ["python3", "multithreaded_calculation.py"]
