SELECT
i.code AS 'itype_code',
i.name AS 'itype',
l.name AS 'location',
COUNT(d.rule_number)

FROM
itypes i, locations l
LEFT JOIN
determiner_expanded d
ON i.code = d.itype AND l.code = TRIM(REPLACE(d.location,'*',''))

WHERE l.code IN (
SELECT
TRIM(REPLACE(d.location,'*',''))
FROM
determiner_expanded d
WHERE
TRIM(REPLACE(d.location,'*','')) NOT IN ('trn','mls','fp3')
)
AND i.code != '80'
GROUP BY 1,2,3
HAVING COUNT(d.rule_number) = 0