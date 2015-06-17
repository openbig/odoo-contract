# -*- coding: utf-8 -*-
from hashlib import sha1
from phpserialize import dumps
from calendar import timegm
from time import strptime
import zlib
#calendar.timegm(time.strptime('01/12/2011', '%d/%m/%Y'))


def create(data):
    assert isinstance(data, dict)
    assert 'request_data' in data
    assert 'contract_data' in data['request_data']
    assert 'product_data' in data['request_data']
    assert isinstance(data['request_data']['product_data'], list)

    mod_identifiers = {
        'viva': 'viva',
        'rfc': 'rfc',
        'relocate_ci': 'CI-Umzug',
        'swapci': 'Geräteaustausch',
    }

    contract_data = data['request_data']['contract_data']
    product_data = data['request_data']['product_data']
    license_data = {
        'C__LICENCE__OBJECT_COUNT': 0,
        'C__LICENCE__DB_NAME': contract_data['db_name'] or '',
        'C__LICENCE__CUSTOMER_NAME': contract_data['customer_name'],
        'C__LICENCE__REG_DATE': timegm(strptime(contract_data['date_start'], '%d/%m/%Y')),
        'C__LICENCE__RUNTIME': timegm(strptime(contract_data['end_date'], '%d/%m/%Y')) - timegm(strptime(contract_data['date_start'], '%d/%m/%Y')),
        'C__LICENCE__EMAIL': ''.join('i-doit@', contract_data['customer_name']),
        'C__LICENCE__TYPE': 'Einzellizenz Subskription',
        'C__LICENCE__DATA': {},
    }

    for product in product_data:
        if 'Objektanzahl' in product:
            license_data['C__LICENCE__OBJECT_COUNT'] += product[
                'Objektanzahl'].isdigit() and int(product['Objektanzahl']) or 0
        if 'Multitenancy' in product:
            if product['Multitenancy'] == 'Single':
                license_data['C__LICENCE__TYPE'] = 'Einzellizenz Subskription'
            elif product['Multitenancy'] == 'Multi':
                license_data['C__LICENCE__TYPE'] = 'Hosting'
            if 'Lizenztyp' in product and product['Lizenztyp'] == 'Kaufversion':
                license_data['C__LICENCE__TYPE'] = 'Kauflizenz'
            if 'Produkttyp' in product and product['Produkttyp'] == 'Modul':
                if 'identifier' in product:
                    license_data['C__LICENCE__DATA'][
                        product['identifier']] = True
                for key in mod_identifiers:
                    if mod_identifiers[key] in product['name'].lower():
                        license_data['C__LICENCE__DATA'][key] = True

    if license_data['C__LICENCE__TYPE'] == 'Hosting':
        license_data['C__LICENCE__DB_NAME'] == ''
    elif license_data['C__LICENCE__TYPE'] == 'Kauflizenz':
        license_data['C__LICENCE__DB_NAME'] == ''
        del license_data['C__LICENCE__RUNTIME']

    license_key = sha1(dumps(license_data))
    #sort
    #serialize with phpserialize.dumps
    #gzip with zlib.compress


    #reverse:
    # f = open('license.key','rb')
    # f_unzipped = zlib.decompress(f.read())
    # license_dict = phpserialize.loads(f_unzipped)

    # return license encoded in base_64
    return True
