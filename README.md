Extract the provided code in a folder.The directory structure should be

```
.
├── BankingSystemUtility.py
├── Branch.py
├── Customer.py
├── README.md
├── assets
│   ├── mw_input.json
│   └── rw_input.json
├── bankingsystem_pb2.py
├── bankingsystem_pb2_grpc.py
├── protos
│   └── bankingsystem.proto
└── requirements.txt
```

Run the following command within the folder to setup the python ‘virtual environment’.

```commandline
python3 -m venv venv
```

From the same folder run the following command to activate the virtual environment.

```commandline
source venv/bin/activate
```

Run the following command to install the required libraries with the specific versions.

```commandline
python -m pip install -r requirements.txt
```

Use the following command to generate the python code from the protobuf files.

```commandline
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/bankingsystem.proto
```

Run the following command to run the branch process. ‘-i’ will take the input json file to create the branches.

For Monotonic-write 
```commandline
python Branch.py -i ./assets/mw_input.json
```

For read-your-writes 
```commandline
python Branch.py -i ./assets/rw_input.json
```
Run the following command to run the customer process. ‘-i’ will take the input json file. And ‘-o’ will take the path
and name of the output json file.

For Monotonic-write

```commandline
python Customer.py -i ./assets/mw_input.json -o ./output.json
```
For read-your-writes
```commandline
python Customer.py -i ./assets/mw_input.json -o ./output.json
```

The output will be available in the path specified while running the branch process. The out put should be some thing
like :

```json
[
  {
    "id": 1,
    "balance": 0
  }
]
```