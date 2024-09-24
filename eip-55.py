from eth_hash.auto import keccak

def to_checksum_address(address):
    """EIP-55 체크섬 주소로 변환하는 함수"""
    # 주소를 소문자로 변환하고, 0x 접두사를 제거
    address = address.lower().replace('0x', '')
    # keccak256 해시 계산
    hashed = keccak(bytes.fromhex(address))

    # 체크섬 주소 생성
    checksum_address = '0x'
    for i, char in enumerate(address):
        # 각 바이트를 직접 비교
        if hashed[i // 2] >= 8:  
            checksum_address += char.upper()
        else:
            checksum_address += char
    return checksum_address

# 예시 주소
address = '0x5b6f3c8c02d1d5a8ccac7e3d1b1e71b3f1d9a7dc'

address2 = '0x5b6f3c8c02d1d5a8ccac7e3d1b1eeeb3f1d9a7dc'
checksum_address = to_checksum_address(address2)
print(f"체크섬 주소: {checksum_address}")