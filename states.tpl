{
  "Comment": "Spotify Flow",
  "StartAt": "Get Spotify Playlists",
  "States": {
    "Get Spotify Playlists": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "${spotify_playlist_arn}:$LATEST"
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
      "Next": "Has Next Playlist?"
    },
    "Has Next Playlist?": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.next_playlist",
          "IsPresent": true,
          "Next": "Get Spotify Playlists"
        }
      ],
      "Default": "Process Spotify Tracks"
    },
    "Process Spotify Tracks": {
      "Type": "Map",
      "ItemProcessor": {
        "ProcessorConfig": {
          "Mode": "INLINE"
        },
        "StartAt": "Get Spotify Tracks",
        "States": {
          "Get Spotify Tracks": {
            "Type": "Task",
            "Resource": "arn:aws:states:::lambda:invoke",
            "OutputPath": "$.Payload",
            "Parameters": {
              "Payload.$": "$",
              "FunctionName": "${spotify_track_arn_arn}:$LATEST"
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
            "Next": "Has Next Tracks?"
          },
          "Has Next Tracks?": {
            "Type": "Choice",
            "Choices": [
              {
                "Variable": "$.next_tracks",
                "IsPresent": true,
                "Next": "Get Spotify Tracks"
              }
            ],
            "Default": "Success Map"
          },
          "Success Map": {
            "Type": "Succeed"
          }
        }
      },
      "Next": "Success",
      "ItemsPath": "$.tracks",
      "MaxConcurrency": 1
    },
    "Success": {
      "Type": "Succeed"
    }
  }
}