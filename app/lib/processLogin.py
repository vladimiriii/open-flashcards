

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'scopes': credentials.scopes
    }


def generate_error_message(sys_info):
    message = "ERROR FOUND\nError Type: \"" + str(sys_info[0]) + "\"\nError Value: \"" + str(
        sys_info[1]) + "\"\nError Traceback: \"" + str(sys_info[2]) + "\""
    return message
