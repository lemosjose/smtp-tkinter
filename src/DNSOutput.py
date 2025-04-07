import dns.resolver
import typing

def getRecords(domain: str) -> typing.Dict[str, typing.List[str]]:
    
    records = {}

    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2
    
    try:
       a_records = resolver.resolve(domain, "A")
       records["A"] = [record.to_text() for record in a_records]
    except Exception as e:
        print(f"erro {e} ao obter os registros A")
        records["A"] = ["Erro ao obter registros de ip"]
    
    #MX
    try:
        mx_records = resolver.resolve(domain, 'MX')
        records["MX"] = [record.to_text() for record in mx_records]
    except Exception as e:
        print(f"Erro {e} ao obter os registros MX")
        records["MX"] = ["Erro ao obter os registros de mail exchange"]
        

    
    #NS 
    try:
        ns_records = resolver.resolve(domain, 'NS')
        records["NS"] = [record.to_text() for record in ns_records]
    except Exception as e:
        print(f"Erro {e} ao obter os registros NS")
        records["NS"] = ["Erro ao obter os registros do nameserver"]

    try:
        txt_records = resolver.resolve(domain, "TXT")
        txt_values = [record.to_text().strip('"') for record in txt_records]
        records["TXT"] = txt_values

        # Extract SPF
        spf_records = [txt for txt in txt_values if txt.startswith("v=spf1")]
        records["SPF"] = spf_records if spf_records else ["Nenhum registro SPF encontrado"]

    except Exception:
        records["TXT"] = ["Erro ao obter registros TXT"]
        records["SPF"] = ["Erro ao obter registros SPF"]

    # DMARC Record (_dmarc.example.com)
    try:
        dmarc_records = resolver.resolve(f"_dmarc.{domain}", "TXT")
        records["DMARC"] = [record.to_text().strip('"') for record in dmarc_records]
    except Exception:
        records["DMARC"] = ["Nenhum registro DMARC encontrado"]

    # DKIM Record (Assume 'default' selector, may vary
        dkim_selector = "default"
    try:
        dkim_records = resolver.resolve(f"{dkim_selector}._domainkey.{domain}", "TXT")
        records["DKIM"] = [record.to_text().strip('"') for record in dkim_records]
    except Exception:
        records["DKIM"] = ["Nenhum registro DKIM encontrado"]

    return records

 

