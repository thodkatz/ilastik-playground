import argparse
import grpc
from tiktorch.proto import training_pb2, training_pb2_grpc
from tiktorch_playground.utils import expand_loaders_path


class TrainingClient:
    def __init__(self, host="127.0.0.1", port=5567):
        print("Connecting to server...")
        print(f"Host: {host}, Port: {port}")
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        print(f"Channel: {self.channel}")
        self.stub = training_pb2_grpc.TrainingStub(self.channel)

    def init(self, yaml_path):
        config = expand_loaders_path(yaml_path)
        try:
            response = self.stub.Init(training_pb2.TrainingConfig(yaml_content=config))
            print(f"Training session initialized with ID: {response.id}")
        except grpc.RpcError as e:
            print(f"Error during Init: {e}")

    def start(self, session_id):
        try:
            self.stub.Start(training_pb2.TrainingSessionId(id=session_id))
            print("Training started.")
        except grpc.RpcError as e:
            print(f"Error during Start: {e}")

    def pause(self, session_id):
        try:
            self.stub.Pause(training_pb2.TrainingSessionId(id=session_id))
            print("Training paused.")
        except grpc.RpcError as e:
            print(f"Error during Pause: {e}")

    def resume(self, session_id):
        try:
            self.stub.Resume(training_pb2.TrainingSessionId(id=session_id))
            print("Training resumed.")
        except grpc.RpcError as e:
            print(f"Error during Resume: {e}")

    def save(self, file_path, session_id):
        try:
            training_session_id = training_pb2.TrainingSessionId(id=session_id)
            save_request = training_pb2.SaveRequest(
                sessionId=training_session_id, filePath=file_path
            )
            self.stub.Save(save_request)
            print("Training saved.")
        except grpc.RpcError as e:
            print(f"Error during Save: {e}")

    def export(self, file_path, session_id):
        try:
            training_session_id = training_pb2.TrainingSessionId(id=session_id)
            export_request = training_pb2.ExportRequest(
                sessionId=training_session_id, filePath=file_path
            )
            self.stub.Export(export_request)
            print("Training exported.")
        except grpc.RpcError as e:
            print(f"Error during Export: {e}")

    def is_best(self, session_id):
        try:
            stream = self.stub.IsBestModel(training_pb2.TrainingSessionId(id=session_id))
            for i, _ in enumerate(stream):
                print(f"Training is best {i}.")
        except grpc.RpcError as e:
            print(f"Error during Export: {e}")

    def get_status(self, session_id):
        try:
            response = self.stub.GetStatus(
                training_pb2.TrainingSessionId(id=session_id)
            )
            print(f"Training status: {response.state}")
        except grpc.RpcError as e:
            print(f"Error during GetStatus: {e}")

    def close_session(self, session_id):
        try:
            self.stub.CloseTrainerSession(training_pb2.TrainingSessionId(id=session_id))
            print("Training session closed.")
        except grpc.RpcError as e:
            print(f"Error during CloseTrainerSession: {e}")


def main():
    parser = argparse.ArgumentParser(description="CLI for Training Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server hostname")
    parser.add_argument("--port", type=int, default=5567, help="Server port")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Init
    init_parser = subparsers.add_parser("init", help="Initialize a training session")
    init_parser.add_argument(
        "--yaml", type=str, required=True, help="YAML configuration for training"
    )

    # Start
    start_parser = subparsers.add_parser("start", help="Start training")
    start_parser.add_argument(
        "--session-id", type=str, required=True, help="Session ID to use"
    )

    # Pause
    pause_parser = subparsers.add_parser("pause", help="Pause training")
    pause_parser.add_argument(
        "--session-id", type=str, required=True, help="Session ID to use"
    )

    # Resume
    resume_parser = subparsers.add_parser("resume", help="Resume training")
    resume_parser.add_argument(
        "--session-id", type=str, required=True, help="Session ID to use"
    )

    # Save
    save_parser = subparsers.add_parser("save", help="Save the training state")
    save_parser.add_argument(
        "--session-id", type=str, required=True, help="Session ID to use"
    )
    save_parser.add_argument(
        "--file-path", type=str, required=True, help="file path to use"
    )

    # Export
    export_parser = subparsers.add_parser("export", help="Export the trained model")
    export_parser.add_argument(
        "--session-id", type=str, required=True, help="Session ID to use"
    )
    export_parser.add_argument(
        "--file-path", type=str, required=True, help="file path to use"
    )

    # Get Status
    status_parser = subparsers.add_parser(
        "status", help="Get the current training status"
    )
    status_parser.add_argument(
        "--session-id", type=str, required=True, help="Session ID to use"
    )

    # Get Status
    is_best_parser = subparsers.add_parser("is_best", help="Best model notification")
    is_best_parser.add_argument(
        "--session-id", type=str, required=True, help="Session ID to use"
    )

    # Close Session
    close_parser = subparsers.add_parser("close", help="Close the training session")
    close_parser.add_argument(
        "--session-id", type=str, required=True, help="Session ID to use"
    )

    args = parser.parse_args()

    # Create a client
    client = TrainingClient(host=args.host, port=args.port)

    # Command execution
    if args.command == "init":
        client.init(args.yaml)
    elif args.command == "start":
        client.start(args.session_id)
    elif args.command == "pause":
        client.pause(args.session_id)
    elif args.command == "resume":
        client.resume(args.session_id)
    elif args.command == "save":
        client.save(args.file_path, args.session_id)
    elif args.command == "export":
        client.export(args.file_path, args.session_id)
    elif args.command == "status":
        client.get_status(args.session_id)
    elif args.command == "close":
        client.close_session(args.session_id)
    elif args.command == "is_best":
        client.is_best(args.session_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
