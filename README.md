[English](README.md) | [日本語](README_ja.md)

# Slack echo bot

![Screenshots](https://raw.githubusercontent.com/ebc-2in2crc/slack-echo-bot/master/images/screenshot.png)

The [AWS CDK](https://aws.amazon.com/cdk/) stack that builds Slack's echo bot on AWS.

## Description

The [AWS CDK](https://aws.amazon.com/cdk/) stack that builds Slack's echo bot on AWS.

The Slack echo bot uses the following AWS services.

- API Gateway
- Lambda
- IAM

## Usage

### Deploy

Execute the `cdk deploy` command to deploy the Slack echo bot to AWS.

`SLACK_BOT_USER_ACCESS_TOKEN` is inputted with the `Bot User OAuth Access Token` of `https://api.slack.com/apps/your-app-id/general`.
`SLACK_SIGNING_SECRET` is set to the `Signing Secret` of `https://api.slack.com/apps/your-app-id/oauth`.

Note the URL of `SlackEchoBotStack.slackbotendpointEndpointxxxxxxxxxxxx` of the output of the `cdk deploy` command.

```
$ cdk deploy --context SLACK_BOT_USER_ACCESS_TOKEN=your-app-access-token --context SLACK_SIGNING_SECRET=your-app-signing-secret

Outputs:
SlackEchoBotStack.slackbotendpointEndpointxxxxxxxx  = https://xxxxxxxxxx.execute-api.any-region.amazonaws.com/prod/
```

### Verify Request URL

Display `https://api.slack.com/apps/your-app-id/event-subscriptions` with a browser.

Set `Enable Events` to `On` and enter the URL of `Outputs` into the `Request URL`, which we wrote down earlier.
It is OK if `Verified` is displayed.

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

The Slack echo bot requires the following OAuth scopes.

- `app_mentions:read`
- `chat:write`

The Slack echo bot should subscribe to the following events.

- `app_mention`

## Notes

The Slack echo bot is experimental.

When actually running the BOT, we strongly recommend that the BOT user's OAuth Access Token and Signing Secret used for signing be stored in [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) or encrypted in [KMS](https://aws.amazon.com/kms/).

## Licence

[MIT](https://github.com/ebc-2in2crc/slack-echo-bot/blob/master/LICENSE)

## Author

[ebc-2in2crc](https://github.com/ebc-2in2crc)
