# this project is aimed to monitor whether the price of a token is within a certain range
# if not, send a notification to the user
#

from web3 import Web3
from contract_abi import uni_nft_abi, pool_abi

alchemy_url = ""
nft_id = 0


pool_contract_address = Web3.toChecksumAddress(
    '0x45dda9cb7c25131df268515131f647d726f50608')
nft_contract_address = Web3.toChecksumAddress(
    '0xC36442b4a4522E871399CD717aBDD847Ab11FE88')

w3 = Web3(Web3.HTTPProvider(alchemy_url))
uni_v3_contract = w3.eth.contract(address=pool_contract_address, abi=pool_abi)
nft_contract = w3.eth.contract(address=nft_contract_address, abi=uni_nft_abi)

# 当前tick
(sqrtPriceX96, tick, observationIndex, observationCardinality, observationCardinalityNext,
 feeProtocol, unlocked) = uni_v3_contract.functions.slot0().call()
# user
# nonce uint96, operator address, token0 address, token1 address, fee uint24, tickLower int24, tickUpper int24, liquidity uint128, feeGrowthInside0LastX128 uint256, feeGrowthInside1LastX128 uint256, tokensOwed0 uint128, tokensOwed1 uint128
(nonce, operator, token0, token1, fee, tickLower, tickUpper, liquidity, feeGrowthInside0LastX128, feeGrowthInside1LastX128, tokensOwed0, tokensOwed1) = nft_contract.functions.positions(nft_id).call()

if (tickLower < tick < tickUpper):
    print("in range")
else:
    print("out of range")
