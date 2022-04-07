#!/usr/bin/env bash

INI_FILE=~/.aws/credentials
AWSVARS=~/.aws/awsvars
while IFS=' = ' read key value
do
    if [[ $key == \[*] ]]; then
        section=$key
    elif [[ $value ]] && [[ $section == '[default]' ]]; then
        if [[ $key == 'aws_access_key_id' ]]; then
            AWS_ACCESS_KEY_ID=$value
        elif [[ $key == 'aws_secret_access_key' ]]; then
            AWS_SECRET_ACCESS_KEY=$value
        fi
    fi
done < $INI_FILE

>$AWSVARS

# echo $AWS_ACCESS_KEY_ID
# echo $AWS_SECRET_ACCESS_KEY

echo "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" >> $AWSVARS
echo "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" >> $AWSVARS