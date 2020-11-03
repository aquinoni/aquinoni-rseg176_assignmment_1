import json
import urllib.parse
import boto3
import psycopg2
import time

print('Loading function')

dbname = ''
host =''
port = ''
user = ''
password = ''
iam_role = ''
s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    company_id = key.split('/')[0]
    print("KEY: "+key)
    print("BUCKET: "+bucket)
    print("COMPANY: "+company_id)
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("KEY: "+key)
        print("BUCKET: "+bucket)
        
    except Exception as e:
        print(e)
        print(f'Error getting object {key} from bucket {bucket}')
        raise e
    
    try:
        con=psycopg2.connect(dbname=dbname, host=host, 
        port=port, user=user, password=password)
        cur = con.cursor()
        copy_command= f"copy SUPERMARKET_SALES_IN from \
        's3://{bucket}/{key}' \
        iam_role '{iam_role}' \
        delimiter ',' IGNOREHEADER 1"
        cur.execute(copy_command)
        con.commit()
        cur.close() 
        con.close()
        
    except Exception as e:
        print(e)
        print(f'Error copying csv "{key}" to table.')
        raise e
    
    try:
        print('BACKING UP SALES DATA')
        millis = int(round(time.time() * 1000))
        backup_file=f"internal-backups/{company_id}_sales_{millis}.csv"
        
        # Copy object A as object B
        s3.copy_object(Bucket=bucket, Key=backup_file, CopySource=f"{bucket}/{key}")
         
        # Delete the former object A
        s3.delete_object(Bucket=bucket,Key=key)
        
    except Exception as e:
        print(e)
        print(f'Error backing up csv "{key}" to "{backup_file}"".')
        raise e
    
    print('COMPLETE')
    return {'company_id':company_id}
