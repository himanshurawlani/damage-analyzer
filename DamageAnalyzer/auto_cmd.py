import subprocess, os, signal

activate_this = "/home/tcs/tensorflow/bin/activate_this.py"
exec(open(activate_this).read(), dict(__file__=activate_this))

os.chdir("/home/tcs/Desktop/TCS/DamageAnalyzer/DamageAnalyzer")
tf_da_server = ""
tf_ada_server = ""
flask_server = ""
node_server = ""

try:
    tf_da_server = subprocess.Popen(["tensorflow_model_server "
                                     "--model_base_path=/home/tcs/Desktop/Himanshu/tf_serving/damage_analyzer "
                                     "--rest_api_port=9000 --model_name=DamageAnalyzer"],
                                    stdout=subprocess.DEVNULL,
                                    shell=True,
                                    preexec_fn=os.setsid)
    print("Started TensorFlow DamageAnalyzer server!")

    tf_ada_server = subprocess.Popen(["tensorflow_model_server "
                                      "--model_base_path=/home/tcs/Desktop/Himanshu/tf_serving/appliance_damage_analyzer "
                                      "--rest_api_port=9001 --model_name=ApplianceDamageAnalyzer"],
                                     stdout=subprocess.DEVNULL,
                                     shell=True,
                                     preexec_fn=os.setsid)
    print("Started TensorFlow ApplianceDamageAnalyzer server!")

    flask_server = subprocess.Popen(["export FLASK_ENV=development && flask run --host=0.0.0.0"],
                                    stdout=subprocess.DEVNULL,
                                    shell=True,
                                    preexec_fn=os.setsid)
    print("Started Flask server!")

    os.chdir("/home/tcs/Desktop/Rasa/node/")
    node_server = subprocess.Popen(["node server.js"],
                                   stdout=subprocess.DEVNULL,
                                   shell=True,
                                   preexec_fn=os.setsid)
    print("Started node server!")

    while True:
        print("Type 'exit' and press 'enter' to quit: ")
        in_str = input().strip().lower()
        if in_str == 'q' or in_str == 'exit':
            print('Shutting down all servers...')
            os.killpg(os.getpgid(tf_da_server.pid), signal.SIGTERM)
            os.killpg(os.getpgid(tf_ada_server.pid), signal.SIGTERM)
            os.killpg(os.getpgid(flask_server.pid), signal.SIGTERM)
            os.killpg(os.getpgid(node_server.pid), signal.SIGTERM)
            print('Servers successfully shutdown!')
            break
        else:
            continue
except KeyboardInterrupt:
    print('Shutting down all servers...')
    os.killpg(os.getpgid(tf_da_server.pid), signal.SIGTERM)
    os.killpg(os.getpgid(tf_ada_server.pid), signal.SIGTERM)
    os.killpg(os.getpgid(flask_server.pid), signal.SIGTERM)
    os.killpg(os.getpgid(node_server.pid), signal.SIGTERM)
    print('Servers successfully shutdown!')
