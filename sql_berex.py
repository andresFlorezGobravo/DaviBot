
import pandas_gbq
from google.oauth2 import service_account

# Ruta al archivo de credenciales en el Google Drive
credentials_path = "credenciales/service-account-key.json"

# Carga las credenciales desde el archivo JSON en Google Drive
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Configura las credenciales para pandas-gbq
pandas_gbq.context.credentials = credentials


query3 = """

SELECT rtd2_credit_repairs.id, 
rtd2_credit_repairs.bank_reference,
rtd2_credit_repairs.country,
rtd2_credit_repair_debts.id as debt_id,
--replace(replace(rtd2_credit_repair_debts.amount :: text, '(', ''),',COP)','') :: double PRECISION / 100 AS deuda_resuelve,
rtd2_credit_repair_debts.amount,
rtd2_credit_repair_debts.state,
rtd2_credit_repair_debt_activities.end,
rtd2_credit_repair_debt_activities.executed_at,
rtd2_credit_repair_debt_activities.payment_to_bank,
rtd2_credit_repair_debt_activities.type,
rtd2_credit_repair_debt_activities.observations

FROM panoply.rtd2_credit_repairs 
LEFT JOIN panoply.rtd2_credit_repair_debts ON rtd2_credit_repair_debts.credit_repair_id = rtd2_credit_repairs.id
LEFT JOIN panoply.rtd2_credit_repair_debt_activities ON rtd2_credit_repair_debt_activities.debt_id = rtd2_credit_repair_debts.id
WHERE rtd2_credit_repairs.country = 'co' and rtd2_credit_repairs.id = 342501

LIMIT 100

"""

df3 = pandas_gbq.read_gbq(query3,  project_id="panoply-766-6d11bff688c1")
display(df3)
