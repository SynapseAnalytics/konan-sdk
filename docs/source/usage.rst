Usage
=====

.. _installation:

Installation
------------

To use konan-sdk, first install it using pip:

.. code-block:: console

   (.venv) $ pip install konan-sdk

On-Prem Deployments
-------------------

If your Konan instance is hosted on premises, it might be using a custom self-signed SSL
certificate. If that is the case, you'd need to instruct ``requests`` to trust the signing CA.
You may check the relevant documentation [here](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification),
but one easy way to do so is to export the ``REQUESTS_CA_BUNDLE`` variable.

For example:

.. code-block:: bash

   export REQUESTS_CA_BUNDLE=/path/to/your/certificate.pem

Of course, don't forget to use your custom ``auth_url`` and ``api_url`` when initializing a ``KonanSDK`` object.

For example:

.. code-block:: python

   from konan_sdk.sdk import KonanSDK

   sdk = KonanSDK(auth_url="https://auth.konan.onprem.local", api_url="https://api.konan.onprem.local")

Making a prediction
-------------------

To make a prediction, you can use the ``konan_sdk.sdk.KonanSDK.predict()`` method:

For example:

.. code-block:: python

   from konan_sdk.sdk import KonanSDK

   sdk = KonanSDK(verbose=False) # Initialize the SDK.

   user = sdk.login(api_key="<api-key>")  # Login user your valid konan API Key
   # user = sdk.login(email="<email>", password="<password>") # Login user your valid Konan credentials

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
   user = sdk.login(api_key="<api-key>")  # Login user your valid konan API Key
   # user = sdk.login(email="<email>", password="<password>") # Login user your valid Konan credentials

   predictions_generator = sdk.get_predictions(
      deployment_uuid="<deployment-uuid>",
      start_time=datetime.datetime(year=2022, month=9, day=1),
      end_time=datetime.datetime(year=2022, month=10, day=1),
   )

   for predictions in predictions_generator:
      # predictions is a list of KonanPrediction objects
      print(len(predictions))
      # Inspect the first KonanPrediction in the list
      print(predictions[0].uuid, predictions[0].features)
      print(predictions[0].output, predictions[0].feedback)

Konan Model Creation
-------------------------

You can also use **konan-sdk** to kickstart your AI model into production! The ``konan_sdk.konan_service`` subpackage
provides all what you will need to transform your model's logic into a Konan-compatible Model.

Check out the `Konan Template Deployments repo <https://github.com/SynapseAnalytics/konan-template-deployments>`_ and 
`Konan Docs <https://docs.konan.ai/guide-to-konan-deployments/bootstrapping>`_ for more information on 
how to extend the ``konan_sdk.konan_service.*`` classes to prepare your Konan-compatible Model.
