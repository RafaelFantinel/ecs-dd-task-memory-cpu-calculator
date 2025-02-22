import math
import boto3

def get_ecs_task_definition(task_definition_name):
    client = boto3.client('ecs')
    response = client.describe_task_definition(taskDefinition=task_definition_name)
    container_definitions = response['taskDefinition']['containerDefinitions']
    return container_definitions

def calculate_task_memory(app_memory, app_memory_percentage, dd_memory, buffer_percentage):
    task_memory = math.ceil((app_memory / (app_memory_percentage / 100)) + dd_memory)
    buffer_memory = math.ceil(task_memory * (buffer_percentage / 100))
    total_memory = task_memory + buffer_memory
    return total_memory

# Obtendo dados do ECS
task_definition_name = "my-ecs-task"
container_definitions = get_ecs_task_definition(task_definition_name)

# Extraindo valores da aplicação
app_container = next((c for c in container_definitions if c['name'] == 'java-app'), None)
dd_container = next((c for c in container_definitions if c['name'] == 'datadog-agent'), None)

if app_container and dd_container:
    app_memory = app_container.get('memory', 1024)  # MiB
    dd_memory = dd_container.get('memory', 256)  # MiB
    app_memory_percentage = 80  # %
    buffer_percentage = 20  # % de sobra para evitar estouro de memória

    task_memory = calculate_task_memory(app_memory, app_memory_percentage, dd_memory, buffer_percentage)
    print(f"Memória ideal para a task (com sobra): {task_memory} MiB")
else:
    print("Erro: Não foi possível recuperar os dados dos containers do ECS.")
