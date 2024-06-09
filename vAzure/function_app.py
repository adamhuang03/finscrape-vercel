import azure.durable_functions as df
import azure.functions as func
import logging
import json
from helper.betakitFunction import BetakitFundingScraper, headers

# app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
app = df.DFApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="orchestrator")
@app.durable_client_input(client_name="client")
async def http_start(
    req: func.HttpRequest,
    client: df.DurableOrchestrationClient):

    # Subcription hook
    validation_token = req.params.get('validationtoken')

    if validation_token:
        logging.info(f"Validation token received: {validation_token}")
        # Respond with the validation token in plain text
        return func.HttpResponse(validation_token, mimetype="text/plain")

    # JSON Handle
    try:
        # Parse the JSON body
        req_body = req.get_json()
    except ValueError:
        # Handle the error if the body is not JSON
        logging.info('Body was not JSON.')
        return func.HttpResponse("Invalid JSON", status_code=400)

    # Durable Function
    instance_id = await client.start_new("orchestrator_function", None, req_body)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    timeout = 5*60*1000  # milli-seconds

    # Wait for the orchestration to complete or return a check status response
    response = await client.wait_for_completion_or_create_check_status_response(req, instance_id, timeout)
    
    if response.status_code == 202:
        # The orchestration is still running, return a status-check response
        return response
    elif response.status_code == 200:
        # The orchestration completed successfully, return the result
        result = response.get_body()
        return func.HttpResponse(result, status_code=200)
    else:
        # Handle other potential statuses (e.g., failures)
        return func.HttpResponse("Failed to process request", status_code=500)
    
    return client.create_check_status_response(req, instance_id)

@app.orchestration_trigger(context_name="context")
def orchestrator_function(context: df.DurableOrchestrationContext):
    """Data filter and function calling distributor.

    JSON template:
    {
        "function_call": ...,
        "parameters": {
            ...
        }
    }
    """

    # Assume we get a webhook
    body = context.get_input()

    if body.get('parameters'):
        params = body.get('parameters')

    if body.get('function_call') == "betakitAPI":
        if params:
            targetString = params.get("target_string")
            article_dict = yield context.call_activity(
                        'appBetakit',
                        targetString
                    )
            return article_dict # 1

# input_name aka "binding name" needs to be valid by the below:
# https://stackoverflow.com/questions/72275772/what-is-a-valid-binding-name-for-azure-function
# no underscores
@app.activity_trigger(input_name="targetString")
def appBetakit(targetString):
    try:
        # betakit = BetakitFundingScraper(
        #     header=headers,
        #     target_string=targetString
        # )
        # return json.dumps(betakit.filtered_articles) #1
        return json.dumps({"test": 1}) #1
    except Exception as e:
        logging.error(f"Error in appBetakit: {str(e)}")
        return json.dumps({"error": str(e)})