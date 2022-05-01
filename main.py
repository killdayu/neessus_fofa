import api


def logo():
    print("hello")


def main():
    logo()

    nessus_scans_dict = api.nesssus_scans()
    api.print_nessus_scans(nessus_scans_dict)

    nessus_scan_id = api.input_nessus_scan_id()
    nessus_scan_id_host_info_dict = api.nessus_scan_info(nessus_scan_id)

    api.fofa_scans(nessus_scan_id_host_info_dict)


if __name__ == '__main__':
    main()
