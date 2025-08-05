import requests
import shutil
import os


def get_releases():
    """
    url = 'https://github.com/breuner/elbencho/releases'
    elbencho-static.x86_64.rpm
    elbencho-static_amd64.deb
    elbencho-windows.zip
    """

    script_folder = os.path.dirname(os.path.abspath(__file__))

    base_url = 'https://github.com'
    ep_releases = 'breuner/elbencho/releases'

    installs_folder = os.path.join(script_folder, 'installers')
    os.makedirs(installs_folder, exist_ok=True)

    releases_file_name = os.path.join(installs_folder, 'releases.html')
    versions_file_name = os.path.join(installs_folder, 'versions.html')

    rpm_release = os.path.join(installs_folder, 'elbencho-static.x86_64.rpm')
    deb_release = os.path.join(installs_folder, 'elbencho-static_amd64.deb')
    zip_release = os.path.join(installs_folder, 'elbencho-windows.zip')

    if not os.path.exists(rpm_release) or not os.path.exists(deb_release) or not os.path.exists(zip_release):
        print('Retrieving New Downloads Listing ..... ')
        response = requests.get(f'{base_url}/{ep_releases}')
        if response.status_code == 200:
            html_content = response.text
            with open(releases_file_name, "w", encoding="utf-8") as file:
                file.write(html_content)

            release_urls = []
            for line in html_content.split('\n'):
                if 'releases/expanded_assets' in line:
                    dd = line.split('src=')[1].split(' ')[0].replace('"', '')
                    if dd not in release_urls:
                        print(f'Found Release url. {dd}')
                        release_urls.append(dd)
            release_urls = sorted(release_urls, reverse=True)
            latest_release_url = release_urls[0]

            print(f'Getting file list from url. {latest_release_url}')
            response = requests.get(latest_release_url)
            if response.status_code == 200:
                html_content = response.text
                with open(versions_file_name, "w", encoding="utf-8") as file:
                    file.write(html_content)

            downloads_list = []
            for line in html_content.split('\n'):
                line = line.strip()
                if 'elbencho-static.x86_64.rpm' in line and 'href' in line:
                    ff = line.split('href=')[1].split(' ')[0].replace('"', '').lstrip('/')
                    dl_url = f'{base_url}/{ff}'
                    if dl_url not in downloads_list:
                        downloads_list.append(dl_url)

                elif 'elbencho-static_amd64.deb' in line and 'href' in line:
                    ff = line.split('href=')[1].split(' ')[0].replace('"', '').lstrip('/')
                    dl_url = f'{base_url}/{ff}'
                    if dl_url not in downloads_list:
                        downloads_list.append(dl_url)

                elif 'elbencho-windows.zip' in line and 'href' in line:
                    ff = line.split('href=')[1].split(' ')[0].replace('"', '').lstrip('/')
                    dl_url = f'{base_url}/{ff}'
                    if dl_url not in downloads_list:
                        downloads_list.append(dl_url)

            file_array = []
            for download_url in downloads_list:
                file_name = os.path.basename(download_url)
                local_file_path = os.path.join(installs_folder, file_name)
                file_array.append(local_file_path)
                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
                    with open(local_file_path, 'wb') as file_out:
                        shutil.copyfileobj(r.raw, file_out)
                print(f"File '{file_name}' downloaded successfully!")
            return file_array
    else:
        file_array = [rpm_release, rpm_release, zip_release]
        return file_array
