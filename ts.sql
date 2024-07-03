CREATE OR REPLACE VIEW dlbiadvdanltcs._SRM_RCS____WEEKLY_RELCAND_1_P_ADJ AS
WITH PB AS (
    SELECT  
        P._KEY, 
        P.CALDT, 
        CAST(P.Y AS FLOAT) AS Y, 
        CAST(P.P AS FLOAT) AS P, 
        P.p_unadjusted, 
        P.SCORE_SK, 
        B.CMTSFQDNDESC, 
        B.MARKET, 
        B.REGION 
    FROM 
        dlbiadvdanltcs._SRM_RCS____WEEKLY_RELCAND_1_P P
    JOIN 
        dlbiadvdanltcs.SRM_MODEL_DATA B 
        ON P._KEY = B._KEY 
    WHERE 
        B.CALDT_K >= DATEADD(MONTH, -6, CURRENT_DATE)
)
SELECT 
    PB._KEY, 
    PB.CALDT, 
    PB.Y, 
    PB.P, 
    PB.p_unadjusted, 
    PB.SCORE_SK,
    PB.P * CMTS_CF.CF AS P_ADJ_CMTS,
    PB.P * MARKET_CF.CF AS P_ADJ_MARKET,
    PB.P * REGION_CF.CF AS P_ADJ_REGION 
FROM 
    PB
LEFT JOIN (
    SELECT 
        CALDT, 
        CMTSFQDNDESC, 
        COUNT(*) AS CNT, 
        AVG(Y) AS AVG_Y, 
        AVG(P) AS AVG_P, 
        AVG(Y) / AVG(P) AS CF 
    FROM 
        PB 
    GROUP BY 
        CALDT, CMTSFQDNDESC  
) CMTS_CF 
ON 
    PB.CMTSFQDNDESC = CMTS_CF.CMTSFQDNDESC 
    AND PB.CALDT = CMTS_CF.CALDT 
LEFT JOIN (
    SELECT 
        CALDT, 
        MARKET, 
        COUNT(*) AS CNT, 
        AVG(Y) AS AVG_Y, 
        AVG(P) AS AVG_P, 
        AVG(Y) / AVG(P) AS CF 
    FROM 
        PB 
    GROUP BY 
        CALDT, MARKET  
) MARKET_CF 
ON 
    PB.MARKET = MARKET_CF.MARKET 
    AND PB.CALDT = MARKET_CF.CALDT 
LEFT JOIN (
    SELECT 
        CALDT, 
        REGION, 
        COUNT(*) AS CNT, 
        AVG(Y) AS AVG_Y, 
        AVG(P) AS AVG_P, 
        AVG(Y) / AVG(P) AS CF 
    FROM 
        PB 
    GROUP BY 
        CALDT, REGION  
) REGION_CF  
ON 
    PB.REGION = REGION_CF.REGION 
    AND PB.CALDT = REGION_CF.CALDT;
