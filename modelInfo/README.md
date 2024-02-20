# Model Info

Eventually this will contain all the scripts that were used during training and for running inferences / possibly backend. 

To run the model you will need to download python and some packages onto whatever machine we end up using. `pip install requirements.txt` in the terminal of the remote machine / server should download the necessary packages.

`loading_test.py` is completed, you should be able to run the script after downloading the above libraries and it will load an LLM and run a test inference to make sure things are working ok.

Let me know when that test case is working - the model used in that file is like 1/14 the size of the model I think we are going to use, so I want to test that once we have a simple model running. We will need an auth token to download a private model, so just lemme know whenever you do that

- Let me know if there are issues, Logan
