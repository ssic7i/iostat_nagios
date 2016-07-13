_author_ = 'Serhii Sheiko'
# Licence: MIT
import subprocess
import sys

arguments = sys.argv
base_command = 'iostat'
base_params = ['-d', '-m']

is_times = False

def parce_args():
    run_args = []
    check_args = {}
    extend_output = False
    device_selected = False
    pass_iteration = False
    times_arr = []

    for i in range(0, len(arguments)):
        if arguments[i].strip().endswith('py') or arguments[i].strip().endswith('pyc') or arguments[i].strip().endswith('.exe'):
            continue
        if pass_iteration == True:
            pass_iteration = False
            continue
        if arguments[i] == '-x' and extend_output == False:
            run_args.append('-x')
            extend_output = True
        elif arguments[i] == '-d' and device_selected == False:
            run_args.append(arguments[i+1])
            device_selected = True
            pass_iteration = True
        elif arguments[i] == '-time':
            times_arr.append(arguments[i+1].split(',')[0])
            times_arr.append('2')
            pass_iteration = True
        elif arguments[i] == '-h':
            help_message()
        else:
            check_args[arguments[i][1:]] = arguments[i+1]
            pass_iteration = True

    if device_selected == False:
        sys.stderr.write('Device not selected. Use power of -d key.')
        sys.exit(128)

    return run_args + times_arr, check_args


def help_message():
    help_msg = '''iostat parcer for nagios
keys:
-h - show help message
-d - device
-x - extend output
'''
    print(help_msg)
    sys.exit(128)

def get_output(result_command):
    p = subprocess.Popen(result_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdata, sterr = p.communicate()

    if sterr is not None:
        sys.stderr.write(sterr)
        sys.exit(128)

    splited_lines = stdata.splitlines()
    for i in range(0, len(splited_lines)):
        if splited_lines[i].startswith('Device:'):
            data_line = splited_lines[i+1]
    return data_line.split()

def check_data(data_in, check_values):
    exit_code = 0
    out_string = 'data recived'
    for itm in check_values:
        if itm in data_in:
            warn_c = check_values[itm].split(',')[0]
            err_c  = check_values[itm].split(',')[1]
            if data_in[itm] > warn_c and data_in[itm] < err_c:
                out_string = out_string + '; ' + itm + ': ' + data_in[itm] + ' ' + ' warning'
                if 1 > exit_code:
                    exit_code = 1
            elif data_in[itm] >= err_c:
                out_string = out_string + '; ' + itm + ': ' + data_in[itm] + ' ' + ' error'
                if 2 > exit_code:
                    exit_code = 2
            else:
                out_string = out_string + '; ' + itm + ': ' + data_in[itm] + ' ' + ' OK'
        else:
            out_string = out_string + '; ' + itm + ': n/a unknown'

    if exit_code == 0:
        print(out_string)
        sys.exit()
    else:
        print(out_string)
        sys.stderr.write(out_string + '\n')
        sys.exit(exit_code)

def parce_output():
    args_run, args_check = parce_args()
    result_command = []
    result_command.append(base_command)
    result_command = result_command + args_run + base_params
    output = get_output(result_command)
    data_to_check = {}

    if len(output) > 6:
        # extended output
        data_to_check['device']   = output[0]
        data_to_check['rrqm_s']   = output[1]
        data_to_check['wrqm_s']   = output[2]
        data_to_check['r_s']      = output[3]
        data_to_check['w_s']      = output[4]
        data_to_check['rMB_s']    = output[5]
        data_to_check['wMB_s']    = output[6]
        data_to_check['avgrq_sz'] = output[7]
        data_to_check['avgqu_sz'] = output[8]
        data_to_check['await']    = output[9]
        data_to_check['r_await']  = output[10]
        data_to_check['w_await']  = output[10]
        data_to_check['svctm']    = output[12]
        data_to_check['util']     = output[13]

    else:
        # short output
        data_to_check['device']    = output[0]
        data_to_check['tps']       = output[1]
        data_to_check['MB_read_s'] = output[2]
        data_to_check['MB_wrtn_s'] = output[3]

    check_data(data_to_check, args_check)

parce_output()
