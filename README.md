# iostat_nagios
Nagios plugin for iostat

usage:

python iostat_n.py [-d %device_name%] [-x][-tps %warning_value%,%critical_value%][-MB_read_s %warning_value%,%critical_value%][-MB_wrtn_s %warning_value%,%critical_value%][-rrqm_s %warning_value%,%critical_value%][-wrqm_s %warning_value%,%critical_value%][-r_s %warning_value%,%critical_value%][-w_s %warning_value%,%critical_value%][-rMB_s %warning_value%,%critical_value%][-wMB_s %warning_value%,%critical_value%][-avgrq_sz %warning_value%,%critical_value%][-avgqu_sz %warning_value%,%critical_value%][-await %warning_value%,%critical_value%][-r_await %warning_value%,%critical_value%][-w_await %warning_value%,%critical_value%][-svctm %warning_value%,%critical_value%][-util %warning_value%,%critical_value%][-time %dalay_time%]

You always should select device name and one of parameters. If no parameter in selected output - it wil be passed.
Warning walue and critical value seperated by comma(",")

Requirements: iostat (sysinfo package), python
