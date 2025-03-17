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
        records["A"] = ["Erro ao obter registros de ip"]
    
    #MX
    try:
        mx_records = resolver.resolve(domain, 'MX')
        records["MX"] = [record.to_text() for record in mx_records]
    except Exception as e:
        records["MX"] = ["Erro ao obter os registros de mail exchange"]
        

    
    #NS 
    try:
        ns_records = resolver.resolve(domain, 'NS')
        records["NS"] = [record.to_text() for record in ns_records]
    except Exception as e:
        records["NS"] = ["Erro ao obter os registros do nameserver"]

 

    return records
    
