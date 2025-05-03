import os
import boto3
import subprocess
import urllib.parse
import os, boto3, subprocess, urllib.parse, logging
import re


# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
bucket = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):

    try:
        # logger.info(f"Received event: {event!r}")
        action = event.get('action', '').lower()

        # ————————— HELP / FIRST INVOCATION —————————
        if action in ('', 'help'):
            help_msg = (
                "Available actions:\n"
                "1. upload — send a file to the S3 bucket (and it's also written to /tmp)\n"
                "2. list   — list backup files in /tmp (uploaded files live in the S3 bucket)\n\n"
                "To use, invoke with JSON:\n"
                '  { "action":"upload", "file_name":"uploads/foo.txt", "file_content":"…"}\n'
                '  { "action":"list",   "prefix":"uploads/..."}\n'
            )
            return {
                'statusCode': 200,
                'body': help_msg
            }

        if action == 'upload':
            file_name    = event.get('file_name', 'default.txt')
            file_content = event.get('file_content', '')
            s3.put_object(Bucket=bucket, Key=file_name, Body=file_content)

            return {
                'statusCode': 200,
                'body': f'File {file_name} uploaded.'
            }

        elif action == 'list':
            prefix_enc = event.get('prefix', '')

            if not prefix_enc.startswith('uploads/'):
                return {'statusCode':400,'body':'Invalid prefix'}

            prefix_raw = urllib.parse.unquote(prefix_enc)


            prefix_nowhitespace = ''.join(prefix_raw.split())

            prefix_masked = (prefix_nowhitespace
                .replace('||', '<OR_OP>')
                .replace('${IFS}', '<IFS>') )

            prefix_clean = re.sub(r'[^A-Za-z0-9/_\.\-%<>]', '', prefix_masked)

            prefix = (prefix_clean
                .replace('<OR_OP>', '||')
                .replace('<IFS>', '${IFS}') )

            # logger.info(f"Sanitized prefix ▶ {prefix}")


            cmd = f"ls /tmp/{prefix}"

            output = subprocess.check_output(cmd, shell=True, text=True)

            return {'statusCode':200,'body':output}

        else:
            return {'statusCode':400,'body':'Bad request'}

    except Exception:
        # logger.exception("list failed")
        return {'statusCode':500,'body':'Internal server error'}