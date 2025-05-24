#multithreaded_calculation.py
#!/usr/bin/env python3
"""
멀티스레드를 사용한 계산 예제
여러 스레드를 활용하여 병렬로 계산을 수행합니다.

작성자: 심대한 (dhsim@yonsei.ac.kr)
버전: 1.0.0
날짜: 2025-05-08
"""

import threading
import time
import random
import logging
import concurrent.futures
import os
from typing import List, Callable, Any

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def cpu_intensive_task(task_id: int, iterations: int = 10**7) -> float:
    """CPU 집약적인 작업을 시뮬레이션하는 함수"""
    logger.info(f"Task {task_id} 시작")
    start_time = time.time()
    
    # CPU 집약적인 작업 시뮬레이션
    result = 0
    for i in range(iterations):
        result += random.random()
    
    elapsed_time = time.time() - start_time
    logger.info(f"Task {task_id} 완료: {elapsed_time:.2f}초 소요, 결과: {result:.2f}")
    return result

def run_with_threads(tasks: List[Callable], max_workers: int = None) -> List[Any]:
    """
    스레드 풀을 사용하여 여러 작업을 병렬로 실행
    
    Args:
        tasks: 실행할 작업 목록
        max_workers: 최대 작업자 수 (None이면 자동으로 설정)
    
    Returns:
        실행 결과 목록
    """
    if max_workers is None:
        # 기본적으로 CPU 코어 수의 2배로 설정 (I/O 작업이 많을 경우 유리)
        max_workers = os.cpu_count() * 2
    
    logger.info(f"스레드 풀 시작 (최대 작업자 수: {max_workers})")
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task) for task in tasks]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"작업 실행 중 오류 발생: {e}")
    
    return results

def run_with_manual_threads(tasks: List[Callable]) -> None:
    """
    스레드를 수동으로 생성하여 작업multithreaded_calculation.py
    """
    threads = []
    
    # 스레드 생성 및 시작
    for i, task in enumerate(tasks):
        thread = threading.Thread(target=task, name=f"Thread-{i}")
        threads.append(thread)
        thread.start()
    
    # 모든 스레드가 완료될 때까지 대기
    for thread in threads:
        thread.join()

def main():
    """메인 함수"""
    num_tasks = os.cpu_count() if os.cpu_count() else 4
    logger.info(f"시스템 CPU 코어 수: {num_tasks}")
    
    # 작업 목록 생성
    tasks = [lambda task_id=i: cpu_intensive_task(task_id) for i in range(num_tasks)]
    
    # 스레드 풀 사용 예제
    logger.info("===== 스레드 풀 실행 =====")
    start_time = time.time()
    results = run_with_threads(tasks)
    elapsed_time = time.time() - start_time
    logger.info(f"스레드 풀 총 실행 시간: {elapsed_time:.2f}초")
    logger.info(f"결과 합계: {sum(results):.2f}")
    
    # 비교를 위한 순차 실행
    logger.info("\n===== 순차 실행 =====")
    start_time = time.time()
    sequential_results = [task() for task in tasks]
    elapsed_time = time.time() - start_time
    logger.info(f"순차 실행 총 시간: {elapsed_time:.2f}초")
    logger.info(f"결과 합계: {sum(sequential_results):.2f}")

if __name__ == "__main__":
    main()