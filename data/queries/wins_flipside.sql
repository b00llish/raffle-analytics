SELECT
  t.block_timestamp as dt_win -- utc
  ,  ifnull(t.instructions[0]:accounts[0]
    ,ifnull(t.instructions[1]:accounts[0] 
    ,ifnull(t.instructions[2]:accounts[0]
    ,ifnull(t.instructions[3]:accounts[0]
    ,ifnull(t.instructions[4]:accounts[0]   
    ,ifnull(t.instructions[5]:accounts[0]
    ,ifnull(t.instructions[6]:accounts[0]
    ,ifnull(t.instructions[7]:accounts[0]
    ,ifnull(t.instructions[8]:accounts[0]
    ,ifnull(t.instructions[9]:accounts[0]
    ,ifnull(t.instructions[10]:accounts[0]
    ,ifnull(t.instructions[11]:accounts[0]
    ,ifnull(t.instructions[12]:accounts[0]
    ,ifnull(t.instructions[13]:accounts[0]
    ,ifnull(t.instructions[14]:accounts[0]
    , NULL
      ))))))))))))))) as account
  --, i.value:mint as nft_mint
  , i.value:owner as winner_wallet

FROM
  solana.core.fact_transactions t 
  , lateral flatten (input => t.post_token_balances) i
WHERE
  -- Get rafffle program info:
  (array_contains(parse_json('{"pubkey":"9ehXDD5bnhSpFVRf99veikjgq8VajtRH7e3D9aVPLqYd","signer":false,"source":"transaction","writable":false}'),account_keys))
  -- date range for data:
  AND date_trunc('day', block_timestamp) > CURRENT_DATE - interval '3 days'
  -- AND date_trunc('day', date_collect) > '10/31/2022' -- exclusive
  -- AND date_trunc('day', date_collect) <= '11/30/2022' -- inclusive
  -- filter for successful transactions
  AND t.succeeded = TRUE
  -- filter for collecting proceeds or claiming prize
    AND (array_contains('Program log: Instruction: ClaimPrize'::variant, t.log_messages)
    OR array_contains('Program log: Instruction: ClaimPrizeV2'::variant, t.log_messages))
  -- filter for non wSOL transactions
  AND NOT i.value:mint = 'So11111111111111111111111111111111111111112'
  AND i.value:uiTokenAmount:uiAmount = 1
  -- AND RAFFLE_ACCT IS NOT NULL
ORDER BY block_timestamp DESC
