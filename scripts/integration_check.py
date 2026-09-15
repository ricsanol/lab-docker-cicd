# Permite trabalhar com respostas e requisições JSON.
import json

# Gera um valor único para não repetir títulos entre execuções.
from uuid import uuid4

# Recursos para realizar requisições HTTP.
from urllib.error import HTTPError
from urllib.request import Request, urlopen


# Endereço do dashboard Nginx.
BASE_URL = "http://127.0.0.1:8080"


# Executa uma requisição HTTP e devolve o corpo da resposta.
def send_request(
    path: str,
    method: str = "GET",
    payload: dict[str, str] | None = None,
    expected_status: int = 200,
) -> str:
    request_data = None
    headers = {}

    # Converte o dicionário Python em JSON UTF-8.
    if payload is not None:
        request_data = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

        headers["Content-Type"] = "application/json; charset=utf-8"

    request = Request(
        url=f"{BASE_URL}{path}",
        data=request_data,
        headers=headers,
        method=method,
    )

    try:
        with urlopen(request, timeout=10) as response:
            status_code = response.status
            response_body = response.read().decode("utf-8")
    except HTTPError as error:
        status_code = error.code
        response_body = error.read().decode("utf-8")

    # Interrompe o teste se o código HTTP for diferente do esperado.
    if status_code != expected_status:
        raise AssertionError(
            f"{method} {path}: esperado HTTP {expected_status}, "
            f"recebido HTTP {status_code}. Corpo: {response_body}"
        )

    return response_body


# Executa o fluxo integrado completo.
def main() -> None:
    study_id: int | None = None

    try:
        # Confirma que o Nginx está entregando o dashboard.
        dashboard_html = send_request("/")

        if "Registro de Estudos" not in dashboard_html:
            raise AssertionError(
                "O HTML do dashboard não contém o título esperado."
            )

        print("[OK] Dashboard respondeu corretamente.")

        # Confirma que o Nginx encaminha a requisição para a API.
        health_body = send_request("/api/health")
        health_data = json.loads(health_body)

        if health_data != {"status": "healthy"}:
            raise AssertionError("A resposta do healthcheck está incorreta.")

        print("[OK] Proxy do Nginx alcançou a FastAPI.")

        # Cria um título único para esta execução.
        unique_title = f"Teste integrado {uuid4()}"

        # Cria um registro no PostgreSQL.
        create_body = send_request(
            "/api/studies",
            method="POST",
            payload={
                "title": unique_title,
                "description": "Registro criado pelo teste integrado.",
            },
            expected_status=201,
        )

        created_study = json.loads(create_body)
        study_id = created_study["id"]

        print(f"[OK] Estudo criado com ID {study_id}.")

        # Consulta o registro criado.
        get_body = send_request(f"/api/studies/{study_id}")
        found_study = json.loads(get_body)

        if found_study["title"] != unique_title:
            raise AssertionError("O título consultado está incorreto.")

        print("[OK] Estudo consultado pelo identificador.")

        # Confirma que o registro aparece na listagem.
        list_body = send_request("/api/studies")
        studies = json.loads(list_body)

        if not any(study["id"] == study_id for study in studies):
            raise AssertionError("O estudo não apareceu na listagem.")

        print("[OK] Estudo encontrado na listagem.")

        # Exclui o registro criado pelo teste.
        send_request(
            f"/api/studies/{study_id}",
            method="DELETE",
            expected_status=204,
        )

        print("[OK] Estudo excluído.")

        # Confirma que o registro excluído responde com HTTP 404.
        not_found_body = send_request(
            f"/api/studies/{study_id}",
            expected_status=404,
        )

        not_found_data = json.loads(not_found_body)

        if not_found_data != {
            "detail": "Registro de estudo não encontrado."
        }:
            raise AssertionError("A resposta HTTP 404 está incorreta.")

        study_id = None

        print("[OK] Exclusão confirmada com HTTP 404.")
        print("[SUCESSO] Teste integrado concluído.")

    except Exception:
        # Tenta remover o registro temporário caso o teste seja interrompido.
        if study_id is not None:
            try:
                send_request(
                    f"/api/studies/{study_id}",
                    method="DELETE",
                    expected_status=204,
                )
            except Exception:
                pass

        raise


# Executa o teste quando o arquivo é chamado diretamente.
if __name__ == "__main__":
    main()