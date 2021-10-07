SELECT
l.LoanRuleNum,
l.Name
FROM
loan_rule l
LEFT JOIN
determiner d
ON
l.LoanRuleNum = d.rule_number
WHERE
d.id IS NULL