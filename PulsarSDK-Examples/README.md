# PulsarSDK-examples

This folder provides a collection of examples intended to show the users how the API of the [Pulsar SDK](https://pypi.org/project/BinhoPulsar/) works.

### Blocking API

Since the [Pulsar SDK](https://pypi.org/project/BinhoPulsar/) API is non-blocking and the responses and notification sent by the host adapter device are handled by a callback function, the API might not be suitable for applications where a blocking API is required. The example inside the folder [blocking-api](./blocking-api/) shows how user can generate a new wrapper class and dynamically decorates the Pulsar class methods to generate a blocking API.

### Jupyter Notebooks

The [notebooks](./notebooks/) folder hosts different Jupyter notebooks sorted in sub folders by protocol or interface. [Jupyter Notebooks](https://jupyter.org/) are an interactive user interface that allows user to run code in cells. Maybe you do not know the name Jupyter Notebooks but you may have used [Google Colab](https://colab.google/) which is based on Jupyter Notebooks, or used [Visual Studio Code extension for Jupyter Notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).

## Customer support

For any questions or doubts you can visit our [Customer Support Portal](https://support.binho.io/) or just reach out at **techsupport@binho.io**.