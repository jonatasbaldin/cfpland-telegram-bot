# CFP Land, the Telegram Bot
Runs the [CFP Land Bot](https://t.me/cfplandbot) and send new CFPs to the [CFP Land](https://t.me/cfpland) channel.

## Environment Variables
The environment variables are managed with AWS SSM and encrypted with an AWS KMS key. They are loaded during _runtime_ to avoid unnecessary function redeploys.

First, create a KMS key:
```bash
$ aws kms create-key
```

Add the `KeyId` to the `custom.KMS_KEY_ID.{env}` key at `serverless.yml` file.

Create _all_ the environment variables necessary – using the `KeyId` from the KMS key generate before:
```bash
$ aws ssm put-parameter --name /CFPLAND/PROD/DATABASE_URL --type String --value <url> --key-id <key-id>
$ aws ssm put-parameter --name /CFPLAND/PROD/TELEGRAM_TOKEN --type String --value <url> --key-id <key-id>
$ aws ssm put-parameter --name /CFPLAND/PROD/IOPIPE_TOKEN --type String --value <url> --key-id <key-id>
```

## License
[MIT](./LICENSE).