Usage
=====

.. _installation:

Installation
------------

To use konan-sdk, first install it using pip:

.. code-block:: console

   (.venv) $ pip install konan-sdk

Making a prediction
-------------------

To make a prediction, you can use the ``konan_sdk.sdk.KonanSDK.predict()`` method:

For example:

.. code-block:: python

   from konan_sdk.sdk import KonanSDK

   sdk = KonanSDK(verbose=False) # Initialize the SDK.

   user = sdk.login("<email>", "<password>") # Login user your valid konan credentials

   input_data = {"feature_1": 1, "feature_2": "abc", } # Define the input data to be passed to your model

   prediction_uuid, ml_output = sdk.predict("<deployment_uuid>", input_data) # Run the prediction

   print(prediction_uuid, ml_output) # Print the returned output

Listing Past Predictions
-------------------------

To list past predictions, make use of the ``konan_sdk.sdk.KonanSDK.get_predictions()`` method, which
uses `yield`-based semantics to both allow you to retrieve a large number of predictions while
also maintaining low request latency and response size.

.. code-block:: python

   import datetime
   from konan_sdk.sdk import KonanSDK

   sdk = KonanSDK(verbose=False) # Initialize the SDK.
   user = sdk.login("<email>", "<password>") # Login user your valid konan credentials

   predictions_generator = sdk.get_predictions(
      deployment_uuid="<deployment-uuid>",
      start_time=datetime.datetime(year=2022, month=9, day=1),
      end_time=datetime.datetime(year=2022, month=10, day=1),
   )

   for predictions in predictions_generator:
      print(len(predictions))
      print(predictions[0].uuid, predictions[0].features)
      print(predictions[0].output, predictions[0].feedback)

Konan Model Creation
-------------------------

You can also use **konan-sdk** to kickstart your AI model into production! The ``konan_sdk.konan_service`` subpackage
provides all what you will need to transform your model's logic into a Konan-compatible Model.

Check out the `Konan Template Deployments repo <https://github.com/SynapseAnalytics/konan-template-deployments>`_ and 
`Konan Docs <https://docs.konan.ai/guide-to-konan-deployments/bootstrapping>`_ for more information on 
how to extend the ``konan_sdk.konan_service.*`` classes to prepare your Konan-compatible Model.
