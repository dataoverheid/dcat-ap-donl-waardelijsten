# encoding: utf-8


from argparse import ArgumentParser
import json
import logging
import os
import requests
from typing import Dict


logging.basicConfig(format='%(asctime)s \t %(levelname)s \t %(message)s',
                    level=logging.DEBUG)


def load_config(config_name: str) -> Dict:
    config_root = os.path.join(os.path.dirname(__file__), '..', 'config')

    with open(os.path.join(config_root, config_name), 'r') as config_contents:
        return json.load(config_contents)


def transform_to_list_format(raw_data: str) -> Dict[str, any]:
    raw_json = json.loads(raw_data)
    transformed_data = {}
    optional_fields = load_config(config_name='optional_fields.json')

    for item in raw_json:
        transformed_item = {
            "labels": {
                "nl-NL": item['label_nl'],
                "en-US": item['label_en']
            }
        }

        for of in optional_fields:
            try:
                transformed_item[of['target']] = item[of['source']]
            except KeyError:
                pass

        transformed_data[item['identifier']] = transformed_item

    return transformed_data


def transform_to_license_format(raw_data: str) -> list:
    raw_json = json.loads(raw_data)
    transformed_data = []

    for item in raw_json:
        transformed_data.append({
            'id': item['identifier'],
            'url': item['identifier'],
            'title': item['label_nl'],
            'domain_content': False,
            'domain_data': False,
            'domain_software': False,
            'family': '',
            'is_generic': True,
            'maintainer': '',
            'od_conformance': 'not reviewed',
            'osd_conformance': 'not reviewed',
            'status': 'active'
        })

    return transformed_data


if __name__ == '__main__':
    parser = ArgumentParser(description='Generate the DCAT-AP-DONL valuelists')
    parser.add_argument('target', metavar='t', type=str,
                        help='The directory where the valuelists are stored')
    target = parser.parse_args().target
    this_file = os.path.basename(__file__)

    logging.info('%s starting', this_file)

    value_lists = load_config(config_name='lists.json')

    for vl_name, vl_data in value_lists.items():
        try:
            logging.info('%s %s', vl_name, vl_data)
            source_data = requests.get(vl_data.get('source')).text
            transformed_source_data = transform_to_list_format(source_data)
            target_path = os.path.join(target, vl_data.get('target'))

            with open(target_path, 'w', encoding='utf-8') as tfh:
                json.dump(transformed_source_data, tfh, ensure_ascii=False,
                          indent=4)

            logging.info(' > updated')
        except Exception as e:
            logging.info(' > error; %s', e)
    
    license_lists = load_config(config_name='license_lists.json')
    
    for vl_name, vl_data in license_lists.items():
        try:
            logging.info('%s %s', vl_name, vl_data)
            source_data = requests.get(vl_data.get('source')).text
            transformed_source_data = transform_to_license_format(source_data)
            target_path = os.path.join(target, vl_data.get('target'))

            with open(target_path, 'w', encoding='utf-8') as tfh:
                json.dump(transformed_source_data, tfh, ensure_ascii=False,
                          indent=4)
                
            logging.info(' > updated')
        except Exception as e:
            logging.info(' > error; %s', e)
    
    logging.info('%s finished', this_file)
