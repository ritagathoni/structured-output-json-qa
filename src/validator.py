"""Small transparent JSON/schema validator with business-rule extensions."""
import json
from pathlib import Path

def _type_ok(value,t):
    return {'string':lambda:isinstance(value,str),'number':lambda:isinstance(value,(int,float)) and not isinstance(value,bool),'integer':lambda:isinstance(value,int) and not isinstance(value,bool),'boolean':lambda:isinstance(value,bool),'array':lambda:isinstance(value,list),'object':lambda:isinstance(value,dict),'null':lambda:value is None}[t]()

def validate(value,schema,path='$'):
    errors=[]
    if 'type' in schema and not _type_ok(value,schema['type']):
        return [f"{path}: expected {schema['type']}, received {type(value).__name__}"]
    if 'enum' in schema and value not in schema['enum']:errors.append(f'{path}: value not in enum')
    if isinstance(value,dict):
        for req in schema.get('required',[]):
            if req not in value:errors.append(f'{path}.{req}: required field missing')
        allowed=schema.get('properties',{})
        if schema.get('additionalProperties') is False:
            for key in value:
                if key not in allowed:errors.append(f'{path}.{key}: unknown field')
        for key,sub in allowed.items():
            if key in value:errors+=validate(value[key],sub,f'{path}.{key}')
    if isinstance(value,list) and 'items' in schema:
        for i,item in enumerate(value):errors+=validate(item,schema['items'],f'{path}[{i}]')
    return errors

def business_rules(record):
    errors=[]
    if record.get('status')=='approved' and record.get('approved_by') in (None,''):
        errors.append('business rule: approved requires approved_by')
    if record.get('discount_pct',0)>10 and not record.get('tier1_approval',False):
        errors.append('business rule: discounts above 10% require tier1_approval')
    return errors

def check_tool_call(call,expected_tool,required_args):
    errors=[]
    if call.get('name')!=expected_tool:errors.append('tool selection mismatch')
    args=call.get('arguments',{})
    if not isinstance(args,dict):return errors+['arguments must be object']
    errors += [f'missing argument: {key}' for key in required_args if key not in args]
    return errors

if __name__=='__main__':
    schema=json.loads(Path('data/schema.json').read_text())
    for record in json.loads(Path('data/outputs.json').read_text()):
        print(json.dumps({'id':record['id'],'errors':validate(record['payload'],schema)+business_rules(record['payload'])},indent=2))
