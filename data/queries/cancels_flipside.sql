SELECT
  t.block_timestamp as dt_cancel
  , i.value:accounts[0] as account
  --, t.instructions[array_size(t.instructions)-3]:accounts[0] as canceled_acct
FROM
  solana.core.fact_transactions t
, lateral flatten (input => INSTRUCTIONS) i
WHERE
  -- date range for data:
  date_trunc('day', t.block_timestamp) > CURRENT_DATE - interval '3 days'
  --date_trunc('day', dt_canc) >= '2022-10-31'
  --AND date_trunc('day', dt_canc) < '2022-12-01'
  -- Get rafffle program info:
  AND (array_contains(parse_json('{"pubkey":"9ehXDD5bnhSpFVRf99veikjgq8VajtRH7e3D9aVPLqYd","signer":false,"source":"transaction","writable":false}'),account_keys))
  -- filter for canceled raffles:
  AND (array_contains('Program log: Instruction: CancelRaffle'::variant, t.log_messages)
      OR array_contains('Program log: Instruction: CancelRaffleV2'::variant, t.log_messages))
  -- filter for successful transactions
  AND t.succeeded = TRUE
  -- drop null rows
  AND i.value:accounts[0] IS NOT NULL
ORDER BY t.block_timestamp desc