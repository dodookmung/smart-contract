import rlp
from rlp.sedes import big_endian_int, binary
from eth_hash.auto import keccak
from eth_abi import encode  # ABI 인코딩을 위한 라이브러리

# EIP-55 체크섬 주소로 변환하는 함수
def to_checksum_address(address):
    """EIP-55 체크섬 주소로 변환하는 함수"""
    address = address.lower().replace('0x', '')
    hashed = keccak(bytes.fromhex(address))

    checksum_address = '0x'
    for i, char in enumerate(address):
        if hashed[i // 2] >= 8:
            checksum_address += char.upper()
        else:
            checksum_address += char
    return checksum_address

# 이더리움 스마트 컨트랙트 트랜잭션 필드 정의
class Transaction(rlp.Serializable):
    fields = [
        ('nonce', big_endian_int),
        ('gasPrice', big_endian_int),
        ('gasLimit', big_endian_int),
        ('to', binary),
        ('value', big_endian_int),
        ('data', binary)
    ]

def create_transaction(nonce, gas_price, gas_limit, to, value, data):
    """스마트 컨트랙트 트랜잭션을 생성하고 RLP 인코딩하는 함수"""
    tx = Transaction(
        nonce=nonce,
        gasPrice=gas_price,
        gasLimit=gas_limit,
        to=to,
        value=value,
        data=data
    )
    encoded_tx = rlp.encode(tx)
    return encoded_tx

def decode_transaction(encoded_tx):
    """RLP로 인코딩된 트랜잭션을 디코딩하는 함수"""
    decoded_tx = rlp.decode(encoded_tx, Transaction)
    return decoded_tx

# 예시 주소
address = '0x5b6f3c8c02d1d5a8ccac7e3d1b1e71b3f1d9a7dc'
checksum_address = to_checksum_address(address)
print(f"체크섬 주소: {checksum_address}")

# 예시 트랜잭션 데이터
nonce = 1
gas_price = 20000000000  # 20 Gwei
gas_limit = 3000000
to_address = bytes.fromhex(checksum_address[2:])  # 체크섬 주소에서 0x 제거
value = 0  # 이더 전송 없음

# ABI 인코딩된 데이터 생성 예시
function_signature = 'transfer(address,uint256)'  # 예시 함수 시그니처
recipient_address = checksum_address  # 받는 사람 주소
amount = 1000  # 전송할 수량

# 데이터 필드에 ABI 인코딩된 값 설정
data = encode(['address', 'uint256'], [recipient_address, amount])

# 스마트 컨트랙트 트랜잭션 생성
encoded_tx = create_transaction(nonce, gas_price, gas_limit, to_address, value, data)

# 인코딩된 트랜잭션 출력
print(f"RLP 인코딩된 스마트 컨트랙트 트랜잭션: {encoded_tx.hex()}\n")

# 디코딩
decoded_tx = decode_transaction(encoded_tx)

# 디코딩된 트랜잭션 출력
print(f"디코딩된 트랜잭션: {decoded_tx}")
print(f"Nonce: {decoded_tx.nonce}")
print(f"GasPrice: {decoded_tx.gasPrice}")
print(f"GasLimit: {decoded_tx.gasLimit}")
print(f"To: {decoded_tx.to.hex()}")
print(f"Value: {decoded_tx.value}")
print(f"Data: {decoded_tx.data.hex()}")