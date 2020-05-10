[English](README.md) | [日本語](README_ja.md)

# Slack echo bot

![Screenshots](https://raw.githubusercontent.com/ebc-2in2crc/slack-echo-bot/master/images/screenshot.png)

Slack の echo bot を AWS 上に構築する [AWS CDK](https://aws.amazon.com/cdk/) スタックです。

## Description

Slack の echo bot を AWS 上に構築する [AWS CDK](https://aws.amazon.com/cdk/) スタックです。

Slack echo bot は以下の AWS サービスを利用します。

- API Gateway
- Lambda
- IAM

## Usage

### Deploy

`cdk deploy` コマンドを実行して Slack echo bot を AWS にデプロイします。

`SLACK_BOT_USER_ACCESS_TOKEN` は `https://api.slack.com/apps/your-app-id/general` の `Bot User OAuth Access Token` を入力します。
`SLACK_SIGNING_SECRET` は `https://api.slack.com/apps/your-app-id/oauth` の `Signing Secret` を入力します。

`cdk deploy` コマンドの出力の `Outputs` の `SlackEchoBotStack.slackbotendpointEndpointxxxxxxxx ` の URL をメモしておきます。

```
$ cdk deploy --context SLACK_BOT_USER_ACCESS_TOKEN=your-app-access-token --context SLACK_SIGNING_SECRET=your-app-signing-secret

Outputs:
SlackEchoBotStack.slackbotendpointEndpointxxxxxxxx  = https://xxxxxxxxxx.execute-api.any-region.amazonaws.com/prod/
```

### Verify Request URL

ブラウザーで `https://api.slack.com/apps/your-app-id/event-subscriptions` を表示します。

`Enable Events` を `On` にしてさきほどメモしておいた `Outputs` の URL を `Request URL` に入力します。
`Verified` が表示すれば OK です。

### Useful commands

- `npm run build`   compile typescript to js
- `npm run watch`   watch for changes and compile
- `npm run test`    perform the jest unit tests
- `cdk deploy`      deploy this stack to your default AWS account/region
- `cdk diff`        compare deployed stack with current state
- `cdk synth`       emits the synthesized CloudFormation template

## Requirement

- AWS Account and User
- Slack App
- [AWS CLI](https://docs.aws.amazon.com/cli/index.html)
- [AWS CDK Toolkit](https://github.com/aws/aws-cdk)

## Slack App

Slack echo bot は以下の OAuth scopes が必要です。

- `app_mentions:read`
- `chat:write`

Slack echo bot は以下のイベントをサブスクリプションしてください。

- `app_mention`

## Notes

Slack echo bot は実験的なものです。

bot を実際に運用するときは bot ユーザーの OAuth Access Token や署名に使う Signing Secret は [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) を利用するか [KMS](https://aws.amazon.com/kms/) で暗号化することを強く推奨します。

## Licence

[MIT](https://github.com/ebc-2in2crc/slack-echo-bot/blob/master/LICENSE)

## Author

[ebc-2in2crc](https://github.com/ebc-2in2crc)
