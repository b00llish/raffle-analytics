select
  t.block_timestamp as dt_buy -- UTC
  , t.signers[0] as buyer_wallet
  , ifnull(t.instructions[2]:accounts[0], ifnull(t.instructions[3]:accounts[0], ifnull(t.instructions[4]:accounts[0],ifnull(t.instructions[5]:accounts[0],'null')))) as account
  , Round(Abs(t.post_balances[0]/1e9-t.pre_balances[0]/1e9),2) as amt_buy
  --, ifnull(t.pre_token_balances[0]:uiTokenAmount:uiAmount, ifnull(t.pre_token_balances[1]:uiTokenAmount:uiAmount, 'null')) as total_sales_prior
  --, ifnull(t.post_token_balances[0]:uiTokenAmount:uiAmount, ifnull(t.post_token_balances[1]:uiTokenAmount:uiAmount, 'null')) as total_sales_post
FROM
  solana.core.fact_transactions t
WHERE
  -- Get rafffle program info:
  (array_contains(parse_json('{"pubkey":"9ehXDD5bnhSpFVRf99veikjgq8VajtRH7e3D9aVPLqYd","signer":false,"source":"transaction","writable":false}'),account_keys))
  -- date range for data:
  AND date_trunc('day', dt_buy) > CURRENT_DATE - interval '5 days'
  -- AND date_trunc('day', dt_buy) > '2023-01-19' -- exclusive
  -- AND date_trunc('day', dt_buy) <= '2023-01-18' -- inclusive
  -- filter for successful transactions
  AND t.succeeded = TRUE
  -- filter for ticket buys
  AND array_contains('Program log: Instruction: BuyTickets'::variant, t.log_messages)
  -- filter for amounts > 0
  AND amt_buy > 0
ORDER BY dt_buy DESC