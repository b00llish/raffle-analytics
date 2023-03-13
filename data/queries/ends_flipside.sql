SELECT
  t.block_timestamp as dt_end -- UTC
  , t.instructions[0]:accounts[0] as account

FROM
  solana.core.fact_transactions t
WHERE
  -- date range for data:
  date_trunc('day', dt_end) > CURRENT_DATE - interval '2 days'
  -- date_trunc('day', date_end) >= '2022-10-31' -- inclusive
  -- AND date_trunc('day', date_end) < '2023-01-01' --exclusive

  -- Get rafffle program info:
  AND (array_contains(parse_json('{"pubkey":"9ehXDD5bnhSpFVRf99veikjgq8VajtRH7e3D9aVPLqYd","signer":false,"source":"transaction","writable":false}'),account_keys))
  AND t.signers[0]   = '84RNKV2kRrRKPjqXnv4SUAJSS7fre7AzqrMaNyoKm3Xm'
  AND array_contains('Program log: Instruction: RevealWinners'::variant, t.log_messages)
  -- filter for successful transactions
  AND t.succeeded = TRUE
  ORDER BY dt_end desc

