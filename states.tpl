{
    "Comment": "Spotify Flow",
    "StartAt": "Get Spotify Playlist",
    "States": {
      "Get Spotifly Playlist": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "OutputPath": "$.Payload",
        "Parameters": {
          "Payload.$": "$",
          "FunctionName": "${lambda_function_arn}:$LATEST"
        },
        "Retry": [
          {
            "ErrorEquals": [
              "Lambda.ServiceException",
              "Lambda.AWSLambdaException",
              "Lambda.SdkClientException",
              "Lambda.TooManyRequestsException"
            ],
            "IntervalSeconds": 2,
            "MaxAttempts": 6,
            "BackoffRate": 2
          }
        ],
        "Next": "Has Next?"
      },
      "Has Next?": {
        "Type": "Choice",
        "Choices": [
          {
            "Variable": "$.next",
            "IsPresent": true,
            "Next": "Get Spotifly Playlist"
          }
        ],
        "Default": "Success"
      },
      "Success": {
        "Type": "Succeed"
      }
    }
  }