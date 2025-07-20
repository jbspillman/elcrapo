from configuration_tools import configuration_details
from elbencho_app import start_services
from elbencho_app import launch_storage_tests




def main():

    servers_list, file_systems, elbencho_client = configuration_details()
    services_status = start_services(servers_list)

    if services_status:
        launch_storage_tests(elbencho_client, servers_list, file_systems)



if __name__ == "__main__":
    main()
