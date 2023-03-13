SELECT
    t.block_timestamp as dt_start
    , ifnull(t.instructions[2]:accounts[0]
        , ifnull(t.instructions[3]:accounts[0]
        , ifnull(t.instructions[4]:accounts[0]
        , ifnull(t.instructions[5]:accounts[0]
        , ifnull(t.instructions[6]:accounts[0]
        , ifnull(t.instructions[7]:accounts[0]
        , ifnull(t.instructions[8]:accounts[0]
        , ifnull(t.instructions[9]:accounts[0]
        , ifnull(t.instructions[10]:accounts[0]
        , 'null'
            ))))))))) as account

    -- convert_timezone('UTC','EST',t.block_timestamp) as start_date
    , t.signers[0] as host_wallet
    , t.inner_instructions[1]:instructions[1]:parsed:info:mint as nft_mint -- mint address for nft
  FROM
    solana.core.fact_transactions t
  WHERE
    -- date range for data:
    date_trunc('day', dt_start) > CURRENT_DATE - interval '3 days'
    -- date_trunc('day', dt_start) >= '2023-01-18' -- inclusive
    -- AND date_trunc('day', dt_start) < '2023-01-01' --exclusive
    -- Get rafffle program info:
      AND (array_contains(parse_json('{"pubkey":"9ehXDD5bnhSpFVRf99veikjgq8VajtRH7e3D9aVPLqYd","signer":false,"source":"transaction","writable":false}'),account_keys))
    -- filter for successful transactions
      AND t.succeeded = TRUE
    -- Filter for raffle action:
      AND array_contains('Program log: Instruction: CreateRaffle'::variant, t.log_messages)
ORDER BY dt_start desc