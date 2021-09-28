### Getting Started

```Python
from konan_sdk.sdk import KonanSDK

if __name__ == '__main__':
    # Initialize the SDK. Set verbose to True if you want verbose logging.
    sdk = KonanSDK(verbose=False)

    # Login user your valid konan credentials
    user = sdk.login("<email>", "<password>")

    # Define the input data to be passed to your model
    input_data = {"feature_1": 1, "feature_2": "abc", }

    # Run the prediction
    prediction_uuid, ml_output = sdk.predict("<deployment_uuid>", input_data)

    # Print the returned output
    print(prediction_uuid, ml_output)
```