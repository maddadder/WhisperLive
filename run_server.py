import argparse
import os

def get_env_var(var_name, default=None, type_func=str):
    """Utility function to get environment variable or use default."""
    value = os.getenv(var_name)
    if value is None:  # Variable not set
        return default
    return type_func(value) 
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # Update each argument to use environment variable if available
    parser.add_argument('--port', '-p',
                        type=int,
                        default=get_env_var('PORT', 9090, int),
                        help="Websocket port to run the server on.")
    parser.add_argument('--backend', '-b',
                        type=str,
                        default=get_env_var('BACKEND', 'faster_whisper'),
                        help='Backends from ["tensorrt", "faster_whisper", "openvino"]')
    parser.add_argument('--faster_whisper_custom_model_path', '-fw',
                        type=str, 
                        default=get_env_var('FASTER_WHISPER_CUSTOM_MODEL_PATH'),
                        help="Custom Faster Whisper Model")
    parser.add_argument('--trt_model_path', '-trt',
                        type=str,
                        default=get_env_var('TRT_MODEL_PATH'),
                        help='Whisper TensorRT model path')
    parser.add_argument('--trt_multilingual', '-m',
                        action='store_true',
                        default=get_env_var('TRT_MULTILINGUAL', 'false').lower() == 'true',
                        help='Boolean only for TensorRT model. True if multilingual.')
    parser.add_argument('--trt_py_session',
                        action='store_true',
                        default=get_env_var('TRT_PY_SESSION', 'false').lower() == 'true',
                        help='Boolean only for TensorRT model. Use python session or cpp session, By default uses Cpp.')
    parser.add_argument('--omp_num_threads', '-omp',
                        type=int,
                        default=get_env_var('OMP_NUM_THREADS', 1, int),
                        help="Number of threads to use for OpenMP")
    parser.add_argument('--no_single_model', '-nsm',
                        action='store_true',
                        default=get_env_var('NO_SINGLE_MODEL', 'false').lower() == 'true',
                        help='Set this if every connection should instantiate its own model. Only relevant for custom model, passed using -trt or -fw.')
    parser.add_argument('--max_clients',
                        type=int,
                        default=get_env_var('MAX_CLIENTS', 4, int),
                        help='Maximum clients supported by the server.')
    parser.add_argument('--max_connection_time',
                        type=int,
                        default=get_env_var('MAX_CONNECTION_TIME', 300, int),
                        help='The maximum duration (in seconds) a client can stay connected. Defaults to 300 seconds (5 minutes)')
    parser.add_argument('--cache_path', '-c',
                        type=str,
                        default=get_env_var('CACHE_PATH', '~/.cache/whisper-live/'),
                        help='Path to cache the converted ctranslate2 models.')

    args = parser.parse_args()

    if args.backend == "tensorrt" and args.trt_model_path is None:
        raise ValueError("Please Provide a valid TensorRT model path")

    if "OMP_NUM_THREADS" not in os.environ:
        os.environ["OMP_NUM_THREADS"] = str(args.omp_num_threads)

    from whisper_live.server import TranscriptionServer
    server = TranscriptionServer()
    server.run(
        "0.0.0.0",
        port=args.port,
        backend=args.backend,
        faster_whisper_custom_model_path=args.faster_whisper_custom_model_path,
        whisper_tensorrt_path=args.trt_model_path,
        trt_multilingual=args.trt_multilingual,
        trt_py_session=args.trt_py_session,
        single_model=not args.no_single_model,
        max_clients=args.max_clients,
        max_connection_time=args.max_connection_time,
        cache_path=args.cache_path
    )
