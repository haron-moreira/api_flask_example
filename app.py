import requests
from flask import Flask, request
from src.model.base_services.valida_login_body import ValidaBodyLogin
from src.helpers.failure_returns import Fail
from src.helpers.success_returns import Success
from src.model.base_services.login import Login
from src.helpers.hash_password import Encrypt
from src.model.base_services.jwt_token import JWT
from prettyconf import config
from src.model.base_services.valida_envio_avulso_body import ValidaBodyEnvioAvulso
from src.helpers.token_spliter import Spliter
from src.model.partner_services.envio_avulso import EnvioAvulso
from src.helpers.generate_transaction_value import TransactionGenerate
from src.model.base_services.register_transaction import Transaction
from src.model.base_services.get_user_id import GetUserId
from src.model.partner_services.get_messages_by_id import GetMessagesById
from src.model.base_services.get_sms_id_register import GetSmsIdRegister
from src.model.base_services.get_sms_register_by_transaction import GetSmsRegister
from src.helpers.date_schedule_validate import DateSchedule
from src.helpers.param_validator import Params
from src.model.partner_services.param_manager import ParamManager
from src.model.base_services.get_sms_by_date import GetSmsByDate
from src.helpers.valida_data import ValidaData
from src.model.base_services.ip_validation import IpValidation
from src.model.base_services.update_sms_status import UpdateSmsStatus
from src.model.base_services.insert_sms_response import InsertSmsResponse
from src.helpers.status_validation import StatusValidation
from src.model.base_services.update_campaign_status import UpdateCampaignStatus
from src.model.base_services.update_campaign_end_status import UpdateCampaignStatusToEnd
from src.logger.log_register import Log

app = Flask(__name__)


# Mudando o padrão de retorno em caso específico de status code
@app.errorhandler(405)
def metodo_nao_permitido(e):
    response = Fail.fail("405")
    return response, response['code']


@app.errorhandler(415)
def metodo_nao_permitido(e):
    response = Fail.fail("415")
    return response, response['code']


@app.errorhandler(404)
def metodo_nao_permitido(e):
    response = Fail.fail("404")
    return response, response['code']


@app.errorhandler(400)
def metodo_nao_permitido(e):
    response = Fail.fail("400-1")
    return response, response['code']


@app.errorhandler(500)
def metodo_nao_permitido(e):
    response = Fail.fail("500")
    return response, response['code']


# rotas de application
@app.route('/api/v1/login', methods=["POST"])
def login():
    if not IpValidation.validate(request.remote_addr):
        Log.register("Tentativa não autorizada de acesso, IP não autorizado",
                     "NULL", "NULL", "Não logado", "/login", request.method, request.remote_addr, 0)
        response = Fail.fail("403-1")
        return response, response['code']

    body = request.json

    if not ValidaBodyLogin.valida(body):
        Log.register("Bad Request no momento do Login",
                     "NULL", "NULL", "Não logado", "/login", request.method, request.remote_addr, 0)
        response = Fail.fail("400-1")
        return response, response['code']

    if not Login.login(body['username'], Encrypt.encrypt(body['password'])):
        Log.register("Login não autorizado",
                     "NULL", "NULL", f"Informado: {body['username']}", "/login", request.method,
                     request.remote_addr, 0)
        response = Fail.fail("401-1")
        return response, response['code']

    token = JWT.generate(body['username'])
    expires = f'{config("JWT_DURATION")} minutes'

    Log.register("Login concluído",
                 token, "NULL", body['username'], "/login", request.method, request.remote_addr, 1)
    response = Success.success_return("200-1", 0, token, expires)
    return response, response['code']


@app.route("/api/v1/message", methods=["POST"])
def envio():
    if not IpValidation.validate(request.remote_addr):
        Log.register("Tentativa não autorizada de acesso, IP não autorizado",
                     request.headers['Authorization'], "NULL", "Not Validated ", "/message", request.method,
                     request.remote_addr, 0)
        response = Fail.fail("403-1")
        return response, response['code']

    header = request.headers
    if not JWT.validate(Spliter.spliter_token(header)):
        Log.register("Token inválido",
                     "NULL", "NULL", "Não logado", "/message", request.method, request.remote_addr, 0)
        response = Fail.fail("401-1")
        return response, response['code']

    body = request.json
    if not ValidaBodyEnvioAvulso.valida(body):
        Log.register("Erro no Body da requisicao",
                     Spliter.spliter_token(header), "NULL", "NULL", "/message", request.method, request.remote_addr, 0)
        response = Fail.fail("400-1")
        return response, response['code']

    if "schedule" in body:
        if DateSchedule.validate(body['schedule']):
            schedule = [
                {
                    "data": body['schedule'],
                    "quantidade": 1
                }
            ]
        else:
            Log.register("Erro de insercao de data",
                         Spliter.spliter_token(header), "NULL", "NULL", "/message", request.method, request.remote_addr,
                         0)
            response = Fail.fail("400-1")
            return response, response['code']
    else:
        schedule = None

    transaction = TransactionGenerate.generate(Spliter.spliter_token(header))
    response = EnvioAvulso.send_message(body['phones'], body['message'], body['name'], body['cost_center'],
                                        config("URL_CALLBACK_RECEBIMENTO"), config("URL_CALLBACK_RESPOSTA"),
                                        agendamentos=schedule)

    if response['id'] is not None:
        Transaction.register(body, response, transaction,
                             GetUserId.get(JWT.token_username(Spliter.spliter_token(header))))
        response = Success.success_return("200-2", transaction)

        Log.register("Campanha de SMS criada com sucesso",
                     Spliter.spliter_token(header), transaction, "NULL", "/message", request.method,
                     request.remote_addr, 1)

        return response, response['code']
    else:

        Log.register("Erro no processo de envio, o response.id é None por alguma razao",
                     Spliter.spliter_token(header), "NULL", "NULL", "/message", request.method, request.remote_addr, 0)

        response = Fail.fail("400-1")
        return response, response['code']


@app.route("/api/v1/message/<transaction>", methods=["GET"])
def messages(transaction):
    if not IpValidation.validate(request.remote_addr):
        Log.register("Tentativa não autorizada de acesso, IP não autorizado",
                     "NULL", transaction, "NULL", "/message", request.method, request.remote_addr, 0)
        response = Fail.fail("403-1")
        return response, response['code']

    header = request.headers
    if not JWT.validate(Spliter.spliter_token(header)):
        Log.register("Token inválido",
                     Spliter.spliter_token(header), transaction, "NULL", "/message", request.method,
                     request.remote_addr, 0)
        response = Fail.fail("401-1")
        return response, response['code']

    if len(transaction) != 32:
        Log.register("O tamanho da transacao informada é inválido",
                     Spliter.spliter_token(header), transaction, "NULL", "/message", request.method,
                     request.remote_addr, 0)
        response = Fail.fail("404")
        return response, response['code']

    if not UpdateCampaignStatusToEnd.update(transaction):
        UpdateCampaignStatusToEnd.update(transaction)
        Log.register("Falha para atualizar o status da campanha para encerrado",
                     Spliter.spliter_token(header), transaction, "NULL", "/message", request.method,
                     request.remote_addr, 0)

    body_data_main = GetSmsRegister.get(transaction, GetUserId.get(JWT.token_username(Spliter.spliter_token(header))))

    if body_data_main == 0:
        Log.register("Os registros desta transação estão vazios.",
                     Spliter.spliter_token(header), transaction, "NULL", "/message", request.method,
                     request.remote_addr, 0)
        response = Fail.fail("404")
        return response, response['code']

    result_by_number = []
    for sms_id in GetSmsIdRegister.get(transaction):
        print(sms_id[0])
        result_by_number.append(GetMessagesById.Get(sms_id[0]))

    Log.register("Busca de transação concluída com sucesso",
                 Spliter.spliter_token(header), transaction, "NULL", "/message", request.method, request.remote_addr, 1)
    response = Success.success_return("200-3", transaction, body_main=body_data_main, details=result_by_number)
    return response, response['code']


@app.route("/api/v1/message/<param_type>/<transaction>", methods=["PUT"])
def status_manager(transaction, param_type):
    if not IpValidation.validate(request.remote_addr):
        Log.register("Tentativa não autorizada de acesso, IP não autorizado",
                     "NULL", transaction, "NULL", f"/message/{param_type}", request.method,
                     request.remote_addr, 0)
        response = Fail.fail("403-1")
        return response, response['code']

    header = request.headers
    if not JWT.validate(Spliter.spliter_token(header)):
        Log.register("Token inválido",
                     Spliter.spliter_token(header), transaction, "NULL", f"/message/{param_type}", request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("401-1")
        return response, response['code']

    if len(transaction) != 32:
        Log.register("O tamanho da transacao informada é inválido",
                     Spliter.spliter_token(header), transaction, "NULL", f"/message/{param_type}", request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("404")
        return response, response['code']

    if not Params.validate(param_type):
        Log.register("O parametro informado não existe ou está mal escrito",
                     Spliter.spliter_token(header), transaction, "NULL", f"/message/{param_type}", request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("400-2")
        return response, response['code']

    if not ParamManager.manager(param_type, transaction):
        Log.register("A transacao de PUT na partner deu algo errado.",
                     Spliter.spliter_token(header), transaction, "NULL", f"/message/{param_type}", request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("400-3")
        return response, response['code']

    Log.register("Comando aplicado na API da partner com sucesso",
                 Spliter.spliter_token(header), transaction, "NULL", f"/message/{param_type}", request.method,
                 request.remote_addr, 1)
    response = Success.success_return("200-4", transaction, action=param_type)
    return response, response['code']


@app.route("/api/v1/message/relatory/<startDate>/<endDate>", methods=["GET"])
def relatory(startDate, endDate):
    if not IpValidation.validate(request.remote_addr):
        Log.register("Tentativa não autorizada de acesso, IP não autorizado",
                     "NULL", "NULL", "NULL", f"/message/relatory/{startDate}/{endDate}",
                     request.method,
                     request.remote_addr, 0)
        response = Fail.fail("403-1")
        return response, response['code']

    header = request.headers
    if not JWT.validate(Spliter.spliter_token(header)):
        Log.register("Token inválido",
                     Spliter.spliter_token(header), "NULL", "NULL", f"/message/relatory/{startDate}/{endDate}",
                     request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("401-1")
        return response, response['code']

    if not DateSchedule.validate(startDate) or not DateSchedule.validate(endDate):
        Log.register("Datas inválidas",
                     Spliter.spliter_token(header), "NULL", "NULL", f"/message/relatory/{startDate}/{endDate}",
                     request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("400-4")
        return response, response['code']

    if not ValidaData.range_of_date(startDate, endDate):
        Log.register("Data inicial é maior que a data final",
                     Spliter.spliter_token(header), "NULL", "NULL", f"/message/relatory/{startDate}/{endDate}",
                     request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("400-4")
        return response, response['code']

    Log.register("Relatorio de data gerado com sucesso",
                 Spliter.spliter_token(header), "NULL", "NULL", f"/message/relatory/{startDate}/{endDate}",
                 request.method,
                 request.remote_addr,
                 1)
    response = Success.success_return("200-5", information_json=GetSmsByDate.get(startDate, endDate, GetUserId.get(
        JWT.token_username(Spliter.spliter_token(header)))),
                                      start_date=startDate, end_date=endDate)
    return response, response['code']


@app.route("/api/v1/health_check", methods=["GET"])
def health_check():
    validation_json = {
        "IpValidation": False,
        "JWT Generate and Login": False,
        "partner Services": False,
        "External Internet from Application": False,
         "Service": False
    }

    try:
        if IpValidation.validate(request.remote_addr):
            validation_json["IpValidation"] = True

        if Login.login(config("HEALTH_CHECK_USER"), Encrypt.encrypt(config("HEALTH_CHECK_USER"))):
            validation_json["JWT Generate and Login"] = True

        if requests.get("https://google.com.br").status_code == 200:
            validation_json['External Internet from Application'] = True

        headers = {
            "Authorization": config("PARTNER_BASIC")
        }
        if requests.get("https://URL/status",
                        headers=headers).status_code == 200:
            validation_json['partner Services'] = True

    except Exception as e:
        print(e)
        return validation_json, 500

    validation_json["Service"] = True
    return validation_json, 200


@app.route("/api/v1/message/update_status", methods=["POST"])
def callback():
    print(request.json)
    body = request.json
    if request.remote_addr not in ['177.53.20.75']:
        Log.register("Algum IP que nao o partner esta tentando chamar a API de callback",
                     "NULL", "NULL", "NULL", f"/message/relatory/update_status", request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("403-1")
        return response, response['code']

    if not UpdateSmsStatus.update(body['smsId'], StatusValidation.validate(body['status']), body['operadora']):
        UpdateSmsStatus.update(body['smsId'], StatusValidation.validate(body['status']), body['operadora'])
        Log.register(f"Erro para atualizar dados de um sms {body['smsId']}",
                     "NULL", "NULL", "NULL", f"/message/relatory/update_status", request.method,
                     request.remote_addr,
                     0)

    if not UpdateCampaignStatus.update(body['smsId']):
        UpdateCampaignStatus.update(body['smsId'])
        Log.register(f"Erro para atualizar dados de uma campanha que o sms: {body['smsId']} participa",
                     "NULL", "NULL", "NULL", f"/message/relatory/update_status", request.method,
                     request.remote_addr,
                     0)

    Log.register(f"Campanha atualizada com sucesso, smsId: {body['smsId']}",
                 "NULL", "NULL", "partner", f"/message/relatory/update_status", request.method,
                 request.remote_addr,
                 1)
    return {"status": "OK"}, 200


@app.route("/api/v1/message/response_by_client", methods=["POST"])
def callback_resposta():
    print(request.json)
    body = request.json
    if request.remote_addr not in ['PARTNER_IP']:
        Log.register("Algum IP que nao o partner esta tentando chamar a API de callback",
                     "NULL", "NULL", "NULL", f"/message/relatory/response_by_client", request.method,
                     request.remote_addr,
                     0)
        response = Fail.fail("403-1")
        return response, response['code']

    if not InsertSmsResponse.insert(body['smsId'], body['resposta']):
        InsertSmsResponse.insert(body['smsId'], body['resposta'])
        Log.register(f"Erro para inserir a resposta do cliente para o smsId: {body['smsId']}",
                     "NULL", "NULL", "NULL", f"/message/relatory/response_by_client", request.method,
                     request.remote_addr,
                     0)

    Log.register(f"Resposta armazenada com sucesso para o smsId: {body['smsId']}",
                 "NULL", "NULL", "NULL", f"/message/relatory/response_by_client", request.method,
                 request.remote_addr,
                 1)
    return {"status": "OK"}, 200


if __name__ == '__main__':
    app.run(debug=True, port=5500, host="0.0.0.0")
