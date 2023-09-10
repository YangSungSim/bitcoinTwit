import asyncio
import csv
import json
import websockets
from config import url
import datetime
from kafka import KafkaProducer

PARAMS = {
    "action": "subscribe",  # 구독을 하겠다는 의미
    "params": {
        "symbols": "ETH/BTC"  # ETH/BTC는 비트코인 심볼
    }
}

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         api_version=(0, 11, 5),
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))


async def run():
    # websockets 모듈을 가져와 연결을 한다. 연결에는 대상 url이 필요하며,
    # ping_interval은 10초 간격으로 핑을 통해 연결을 유지하겠다는 의미이다.
    websocket = await websockets.connect(url, ping_interval=10)
    # 위에 기재한 메시지를 json으로 바꾸어 연결된 웹소켓을 통해 전달한다.
    await websocket.send(json.dumps(PARAMS))

    while True:
        message = await websocket.recv()
        data = json.loads(message)

        if "timestamp" in list(data.keys()):
            data["timestamp"] = datetime.datetime.fromtimestamp(data["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
            print(data)
            producer.send('data-stream', data)
            print('Price sent to consumer')
        else:
            continue


# 이 코드는 비동기 함수인 run을 실행하는 코드이다.
# 이 스크립트를 메인으로 사용하는 경우에만 실행한다.
if __name__ == "__main__":
    asyncio.run(run())