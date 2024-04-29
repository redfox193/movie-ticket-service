PROTO_DIR = ../protobufs
PROTO_FILE = iticket

# use to generate grpc server and client
protoc: $(PROTO_DIR)
	python -m grpc_tools.protoc -I $(PROTO_DIR) --python_out=src/generated_code --grpc_python_out=src/generated_code $(PROTO_FILE).proto
