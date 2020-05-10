import * as cdk from '@aws-cdk/core';
import {PolicyStatement} from '@aws-cdk/aws-iam'
import * as lambda from '@aws-cdk/aws-lambda';
import * as apigw from '@aws-cdk/aws-apigateway';

export class SlackEchoBotStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const helloLambda = this.createSlackEchoBotLambda();
    const invokerLambda = this.createInvokerLambda(helloLambda);
    this.createApiGateway(invokerLambda);
  }

  private createSlackEchoBotLambda(): lambda.Function {
    const createEnvironment = (): { [p: string]: string } => {
      return {
        'SLACK_BOT_USER_ACCESS_TOKEN': this.node.tryGetContext('SLACK_BOT_USER_ACCESS_TOKEN'),
        'SLACK_SIGNING_SECRET': this.node.tryGetContext('SLACK_SIGNING_SECRET'),
      };
    }

    return new lambda.Function(this, 'slack-bot-function', {
      functionName: 'SlackEchoBot',
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'slack_bot.lambda_handler',
      environment: createEnvironment(),
    });
  }

  private createInvokerLambda(target: lambda.Function): lambda.Function {
    const fn = new lambda.Function(this, 'invoker-function', {
      functionName: 'LambdaInvoker',
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'lambda_invoker.lambda_handler',
      environment: {'INVOCATION_FUNCTION_NAME': target.functionName},
    });
    fn.role?.addToPolicy(new PolicyStatement({
      actions: ["lambda:InvokeFunction"],
      resources: [target.functionArn]
    }))
    return fn;
  }

  private createApiGateway(fn: lambda.Function) {
    const api = new apigw.RestApi(this, 'slack-bot-endpoint', {
      restApiName: 'SlackBot',
      endpointConfiguration: {types: [apigw.EndpointType.REGIONAL]}
    });
    const integration = new apigw.LambdaIntegration(fn, {proxy: true});
    api.root.addMethod('POST', integration, {});
  }
}
