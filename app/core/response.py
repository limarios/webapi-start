def success_response(data=None, message="Operação realizada com sucesso"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def error_response(message="Ocorreu um erro", details=None):
    return {
        "status": "error",
        "message": message,
        "details": details
    }
