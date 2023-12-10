import requests

def get_current_heads_of_state():
    url = "https://query.wikidata.org/sparql"
    query = """
    SELECT DISTINCT ?country ?countryLabel ?hstate ?hstateLabel ?hstateParty ?hstatePartyLabel ?hgov ?hgovLabel ?hgovParty ?hgovPartyLabel 
        WHERE {
        ?country wdt:P31 wd:Q3624078.
        FILTER(NOT EXISTS { ?country wdt:P31 wd:Q3024240. })

        # Retrieve information about the current head of state
        ?country p:P35 ?stateStatement.
        ?stateStatement ps:P35 ?hstate.
        MINUS { ?stateStatement pq:P582 ?partyEnd. } # Exclude those who are no longer head of state

        OPTIONAL {
            # Retrieve information about the political party of the head of state
            ?hstate p:P102 ?hstatePartyStatement.
            ?hstatePartyStatement ps:P102 ?hstateParty.
            FILTER EXISTS {
            ?hstatePartyStatement pq:P580 ?start.
            }
            MINUS { ?hstatePartyStatement pq:P582 ?end. } # Exclude parties they are no longer a member of
        }

        # Retrieve information about the current head of government
        ?country p:P6 ?hgovStatement.
        ?hgovStatement ps:P6 ?hgov.
        FILTER EXISTS {
            ?hgovStatement pq:P580 ?partyStart.
        }
        MINUS { ?hgovStatement pq:P582 ?partyEnd. } # Exclude those who are no longer head of government

        OPTIONAL {
            # Retrieve information about the political party of the head of government
            ?hgov p:P102 ?hgovPartyStatement.
            ?hgovPartyStatement ps:P102 ?hgovParty.
            FILTER EXISTS {
                ?hgovPartyStatement pq:P580 ?start.
            }
            MINUS { ?hgovPartyStatement pq:P582 ?end. } # Exclude parties they are no longer a member of
        }

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
    ORDER BY DESC (?country)
    """
    response = requests.get(url, params={'format': 'json', 'query': query})
    data = response.json()

    heads_of_state = []
    for item in data['results']['bindings']:
        info = {
            'country': item['countryLabel']['value'],
            'name': item['presidentLabel']['value'],
            'party': item.get('partyLabel', {}).get('value', 'N/A'),  # Some heads of state might not have a party
            'start': item['start']['value']
        }
        heads_of_state.append(info)

    return heads_of_state