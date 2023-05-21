import requests


def getData(cities_list):
    s="SP"
    c= "br"
    data = []

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Brave\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "cookie": "_osm_totp_token=114327"
    }


    for city in cities_list:
        data.append( {"state":"SP","city":city,"country":"br"})

    results = []
    print("Please wait...\nLoading OpenStreeMap's API data....\n\n")
    for row in data:
                # Remove parenteses e abreviação de estado (se existir) do nome da cidade
        city = (row['city']).split("(")[0].strip().rstrip(", MA") # examplo MA
        state = (row['state']).split("(")[0].strip()
        country = (row['country']).split("()")[0].strip()

        url = f"https://nominatim.openstreetmap.org/search.php?city={city}&state={state}&country={country}&format=jsonv2&addressdetails=1&limit=1"
        response = requests.get(url, headers=headers)
        data = response.json()
        if data:
            # Extrai latitude e longitude do primeiro resultado
            nam = str(data[0]['display_name']).split(',', 1)[0]
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            # Adiciona a cidade, latitude, e longitude para a lista de resultado
            results.append({"nam":nam,"lat": lat, "lon": lon})

    return(results)
