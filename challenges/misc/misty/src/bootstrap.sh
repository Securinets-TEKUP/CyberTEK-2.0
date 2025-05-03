#!/usr/bin/env bash

set -euo pipefail

ENDPOINT="https://dev-minio.tekup-securinets.tech/"

ADMIN_ACCESS_KEY="${ADMIN_ACCESS_KEY:?Environment variable ADMIN_ACCESS_KEY is required}"
ADMIN_SECRET_KEY="${ADMIN_SECRET_KEY:?Environment variable ADMIN_SECRET_KEY is required}"
ADMIN_ALIAS="admin"

USER_ALIAS="tmp-user"
USERNAME="chx-dev037"
USER_ACCESS_KEY="${USER_ACCESS_KEY:?Environment variable UPLOAD_ACCESS_KEY is required}"
USER_SECRET_KEY="${USER_SECRET_KEY:?Environment variable UPLOAD_SECRET_KEY is required}"

POLICY_NAME="TMP Policy"
POLICY_FILE_PATH="./policy.json"
BUCKET_NAME="tmp-vault"
FILE_TO_UPLOAD="./flag.txt"
FILE_TO_UPLOAD_SECOND="./key"
OBJECT_NAME="key"

function create_minio_user() {
    mc alias set "$ADMIN_ALIAS" "$ADMIN_ENDPOINT" "$ADMIN_ACCESS_KEY" "$ADMIN_SECRET_KEY"
    mc admin user add "$ADMIN_ALIAS" "$UPLOAD_USERNAME" "$UPLOAD_SECRET_KEY"
}

function create_and_attach_minio_policy() {
    mc admin policy create "$ADMIN_ALIAS" "$POLICY_NAME" "$POLICY_FILE_PATH"
    mc admin policy attach "$ADMIN_ALIAS" "$POLICY_NAME" --user="$UPLOAD_USERNAME"
}

function put_secret() {
    mc alias set "$UPLOAD_USER_ALIAS" "http://$ADMIN_ENDPOINT" "$UPLOAD_USERNAME" "$UPLOAD_SECRET_KEY"

    mc version enable "$UPLOAD_USER_ALIAS/$BUCKET_NAME"
    mc cp "$FILE_TO_UPLOAD" "$UPLOAD_USER_ALIAS/$BUCKET_NAME/$OBJECT_NAME"
    mc cp "$FILE_TO_UPLOAD_SECOND" "$UPLOAD_USER_ALIAS/$BUCKET_NAME/$OBJECT_NAME"
}

function main() {
    create_minio_user
    create_and_attach_minio_policy
    put_secret
}

main
