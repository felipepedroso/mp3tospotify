from os import environ

def get_environment_variable(variable_name):
    value = environ.get(variable_name)

    if value is None:
        print("The environment variable " + variable_name + " is required. Please ensure that you added to your system.")
        exit()

    return value