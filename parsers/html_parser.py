from bs4 import BeautifulSoup
import requests
import json

from core.utils import retrieve_json_data

def parse_lab_info(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    name_lab = soup.head.title.text
    link_lab = soup.find('a', class_='link-back')

    # retrieve objective of the lab 
    response_lab = requests.get(link_lab['href'])
    soup_lab = BeautifulSoup(response_lab.text, 'html.parser')
    paragraphs = soup_lab.find_all('p')

    for p in paragraphs:
        if "To solve the lab" in p.get_text():
            objective_lab = p.get_text()[30:]
            break

    # retrieve dificulty of the lab
    p_dif = soup_lab.find('p', class_='widget-container-labelevel')
    dificulty = p_dif.find('span').get_text()
    if dificulty == "APPRENTICE":
        dificulty = r"[bold green]APPRENTICE[/bold green]"
    elif dificulty == "PRACTITIONER":
        dificulty = r"[bold yellow]PRACTITIONER[/bold yellow]"
    else:
        dificulty = r"[bold red]EXPERT[/bold red]"
    
    # retrieve type of vulnerability
    data_vuln = retrieve_json_data()
    for vulns in data_vuln['listVuln']:
        for vuln in vulns['listLab']:
            if vuln['name'] == name_lab:
                type_vuln = vulns['nameVuln']
                break
    
    # recolor
    type_vuln = r"[bold white]" + type_vuln + r"[/bold white]"
    name_lab = r"[bold white]" + name_lab + r"[/bold white]"
    link_lab['href'] = r"[bold white]" + link_lab['href'] + r"[/bold white]"
    objective_lab = r"[bold white]" + objective_lab[:-9] + r"[/bold white]"

    return  type_vuln, name_lab, link_lab['href'], objective_lab, dificulty
