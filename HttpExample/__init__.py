import logging
import os
import json
import azure.functions as func


# The validation event, see https://aka.ms/esvalidation for details
SUBSCRIPTION_VALIDATION_EVENT = "Microsoft.EventGrid.SubscriptionValidationEvent"
# Blob created in a storage account
STORAGE_BLOB_CREATED_EVENT = "Microsoft.Storage.BlobCreated"
# The one used in the "Publisher" sample
CUSTOM_EVENT = "PersonalEventType"


def main(req: func.HttpRequest) -> func.HttpResponse:
    for event in req.get_json():
        event_data = event['data']

        # Deserialize the event data into the appropriate type based on event type using if/elif/else

        if event['eventType'] == SUBSCRIPTION_VALIDATION_EVENT:
            validation_code = event_data['validationCode']
            # If you don't use the preview version of EventGrid, this might no exist
            validation_url = event_data.get('validationUrl', None)
            print("Got a SubscriptionValidation event data, validation code is: {}, validation url is {}".format(
                validation_code,
                validation_url
            ))
            answer_payload = {
                "validationResponse": validation_code
            }
            return func.HttpResponse(
                json.dumps(answer_payload),
                status_code=200
        )
        elif event['eventType'] == STORAGE_BLOB_CREATED_EVENT:
            print("Got BlobCreated event data, blob URI {}".format(
                event_data['url']))
            return func.HttpResponse(
                "Got BlobCreated event data",
                status_code=200)
        elif event['eventType'] == CUSTOM_EVENT:
            print("Got a custom event {} and received {}".format(
                CUSTOM_EVENT, event_data))
            return func.HttpResponse(
                "Got a custom event",
                status_code=200)
