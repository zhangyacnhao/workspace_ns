from flask import request
from flask import Blueprint
from flask import jsonify
import os
import time
import subprocess


demo = Blueprint('demo', __name__)

@demo.route('/heartbeat', methods=['GET', 'POST'])
def hello():
    response = {'errcode': 0, 'msg': 'OK'}
    return jsonify(response), 200
 
@demo.route('/reboot/win2debian', methods=['GET'])
def reboot_win_debian():
    cmd = 'shutdown /soft /r /t 1'
    # print(cmd)
    subprocess.Popen(cmd)
    return jsonify({'errmsg': 'OK', 'errcode': 0}), 200

@demo.route('/shutdown/win', methods=['GET'])
def shutdown_win():
    password = request.args.get('password')
    if not password:
        return jsonify({'errmsg': 'No password provided', 'errcode': 1}), 400
    cmd = f'shutdown /s /t 20'
    try:
        subprocess.check_call(cmd, shell=True)
        return jsonify({'errmsg': 'Shutdown scheduled after 20s', 'errcode': 0}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'errmsg': f'Error executing command: {e}', 'errcode': 1}), 500

@demo.route('/shutdown/debian', methods=['GET'])
def shutdown_debian():
    password = request.args.get('password')
    if not password:
        return jsonify({'errmsg': 'No password provided', 'errcode': 1}), 400
    cmd = f'sleep 20 && echo {password} | sudo -S  shutdown -h now'
    try:
        subprocess.check_call(cmd, shell=True)
        return jsonify({'errmsg': 'Shutdown scheduled after 20s', 'errcode': 0}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'errmsg': f'Error executing command: {e}', 'errcode': 1}), 500


@demo.route('/reboot/debian2win', methods=['GET'])
def reboot_debian_win():
    password = request.args.get('password')
    if not password:
        return jsonify({'errmsg': 'No password provided', 'errcode': 1}), 400
    cmd = f'echo {password} | sudo -S grub-reboot 2 && echo {password} | sudo -S shutdown -r +1'
    try:
        subprocess.check_call(cmd, shell=True)
        return jsonify({'errmsg': 'Reboot scheduled after 10 minutes', 'errcode': 0}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'errmsg': f'Error executing command: {e}', 'errcode': 1}), 500


@demo.route('/reboot/debian2debian', methods=['GET'])
def reboot_debian_debian():
    password = request.args.get('password')
    if not password:
        return jsonify({'errmsg': 'No password provided', 'errcode': 1}), 400

    cmd = f'echo {password} | sudo -S shutdown -r +10'
    try:
        subprocess.check_call(cmd, shell=True)
        return jsonify({'errmsg': 'Reboot scheduled after 10 minutes', 'errcode': 0}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'errmsg': f'Error executing command: {e}', 'errcode': 1}), 500
