import config
import requests
import urllib3
import re
import base64

urllib3.disable_warnings()  #不显示https证书警告


def nesssus_scans():
    nessus_scans_result = requests.get(config.nessus_baseurl + "scans", headers=config.nessus_headers, verify=False)
    nessus_scans_result_json_date = nessus_scans_result.json()

    nesssus_scans_dict = {}
    for key in nessus_scans_result_json_date["scans"]:
        #print(key)
        nesssus_scans_dict[key["id"]] = key["name"], key["status"]

    return nesssus_scans_dict


def print_nessus_scans(nesssus_scans_dict):
    print("nessus scans:")
    for nessus_scans_id in nesssus_scans_dict:
        nesssus_scans_dict_name = nesssus_scans_dict[nessus_scans_id][0]
        nesssus_scans_dict_status = nesssus_scans_dict[nessus_scans_id][1]
        print("[{}]:{}:{}".format(nessus_scans_id, nesssus_scans_dict_name, nesssus_scans_dict_status))


def input_nessus_scan_id():
    nessus_scan_id = input("nessis id:")
    return nessus_scan_id


def nessus_scan_info(nessus_scan_id):
    nessus_scan_result = requests.get(config.nessus_baseurl + "scans" + "/" + str(nessus_scan_id), headers=config.nessus_headers, verify=False)
    nessus_scan_result_json_date = nessus_scan_result.json()

    host_info_dict = {}

    for i in range(len(nessus_scan_result_json_date["hosts"])):
        host_info = nessus_scan_result_json_date["hosts"][i]
        host_info_high = host_info["high"]
        host_info_medium = host_info["medium"]
        host_info_low = host_info["low"]
        host_info_hostname = host_info["hostname"]

        host_info_dict[host_info_hostname] = host_info_high, host_info_medium, host_info_low

    return host_info_dict


def fofa_scans(nessus_scan_id_host_info_dict):
    for hostname in nessus_scan_id_host_info_dict:
        host_info_high = nessus_scan_id_host_info_dict[hostname][0]
        host_info_medium = nessus_scan_id_host_info_dict[hostname][1]
        print("[{}],high:{},medium:{}".format(hostname, host_info_high, host_info_medium))

        if (host_info_high + host_info_medium) > 0:   #只fofa 有中高漏洞的hostname
            if check_ip(hostname):  #ip
                fofa_search_result_data_json = fofa_result(fofa_search_ip(hostname))
                title = fofa_result_results(fofa_search_result_data_json)
                print(title)
            else:   #host
                fofa_search_result_data_json = fofa_result(fofa_search_host(hostname))
                title = fofa_result_results(fofa_search_result_data_json)
                print(title)


def check_ip(hostname):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(hostname):
        return True
    else:
        return False


def fofa_search_ip(ip):
    fofa_search_ip_str = "ip = \"" + ip + "\""
    fofa_search_url = config.fofa_baseurl + str_base64(fofa_search_ip_str)
    return fofa_search_url


def fofa_search_host(host):
    fofa_search_host_str = "host = \"" + host + "\""
    fofa_search_url = config.fofa_baseurl + str_base64(fofa_search_host_str)
    return fofa_search_url


def fofa_result(fofa_search_url):
    fofa_search_result = requests.get(fofa_search_url, verify=False)
    fofa_search_result_data_json = fofa_search_result.json()

    return fofa_search_result_data_json


def fofa_result_results(fofa_search_result_data_json):  #处理fofa返回的json里面的result key
    fofa_result_results_list = fofa_search_result_data_json["results"]
    for i in range(len(fofa_result_results_list)):
        if fofa_result_results_list[i][1] not in config.fofa_result_keywords_blacklist:
            #print(fofa_result_results_list[i][1])
            return fofa_result_results_list[i][1]


# def print_nessus_high_medium(nessus_scan_id_host_info_dict):
#     for host_info_hostname in nessus_scan_id_host_info_dict:
#         host_info_high = nessus_scan_id_host_info_dict[host_info_hostname][0]
#         host_info_medium = nessus_scan_id_host_info_dict[host_info_hostname][1]
#         print("[{}],high:{},medium:{}".format(host_info_hostname, host_info_high, host_info_medium))


def str_base64(str_str):
    str_tmp = base64.b64encode(str_str.encode('utf-8'))
    str_encoded = str(str_tmp, 'utf-8')
    return str_encoded
