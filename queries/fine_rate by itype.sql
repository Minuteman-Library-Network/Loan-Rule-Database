select 
CAST(d.itype AS INTEGER) AS itype,
(REPLACE(l.AmountOfFine1stFPer,'$','') + REPLACE(l.AmountOfFine2NDFPer,'$','')) AS fine_rate,
COUNT(DISTINCT d.location) AS library_count,
group_concat(DISTINCT REPLACE(d.location,'*','')) AS locations

FROM
determiner_expanded d
JOIN
loan_rule l
ON
d.rule_number = l.LoanRuleNum

GROUP BY 1,2

ORDER BY 1,2,3 desc,2