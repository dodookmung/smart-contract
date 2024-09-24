import hashlib
import json
import time

def create_block(parent_hash, beneficiary, gas_limit, gas_used, timestamp, extra_data):
    block = {
        "parentHash": parent_hash,
        "beneficiary": beneficiary,
        "stateRoot": "0x" + "0" * 64,  # 상태 루트 (예: 0으로 초기화)
        "transactionsRoot": "0x" + "0" * 64,  # 트랜잭션 루트 (예: 0으로 초기화)
        "logsBloom": "0x" + "0" * 512,  # 블룸 필터 (예: 0으로 초기화)
        "difficulty": "0x0",  # POS 체인에서는 사용되지 않음
        "number": 1,  # 제네시스 블록 다음 블록 (변경 필요)
        "gasUsed": gas_used,
        "gasLimit": gas_limit,
        "timestamp": timestamp,
        "extraData": extra_data
    }
    return block

# genesis.json 파일을 읽어오기
with open('genesis.json') as f:
    genesis_block = json.load(f)

# 부모 해시 계산
parent_hash = hashlib.sha256(json.dumps(genesis_block).encode()).hexdigest()

# 새로운 블록 생성
new_block = create_block(
    parent_hash="0x" + parent_hash,
    beneficiary=genesis_block['alloc'].keys().__iter__().__next__(),  # 첫 번째 주소 사용
    gas_limit=genesis_block['gasLimit'],
    gas_used="0x0",
    timestamp=hex(int(time.time())),
    extra_data="0x"
)

print(json.dumps(new_block, indent=2))