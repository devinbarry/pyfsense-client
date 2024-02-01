def get_response_json():
    return {
        "status": "ok",
        "code": 200,
        "return": 0,
        "message": "Success",
        "data": {
            "system_platform": "Netgate pfSense Plus",
            "system_serial": "1234567890",
            "system_netgate_id": "73hdy57agetd86jhgfd4",
            "bios_vendor": "American Megatrends Inc.",
            "bios_version": "1.3a",
            "bios_date": "04/23/2019",
            "cpu_model": "Intel(R) Xeon(R) D-2123IT CPU @ 2.20GHz",
            "kernel_pti": True,
            "mds_mitigation": "inactive",
            "temp_c": 60,
            "temp_f": 136.4,
            "load_avg": [0.01, 0.05, 0.01],
            "cpu_count": 8,
            "mbuf_usage": 0.04,
            "mem_usage": 0.06,
            "swap_usage": 0,
            "disk_usage": 0.01
        }
    }