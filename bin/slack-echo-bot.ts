#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { SlackEchoBotStack } from '../lib/slack-echo-bot-stack';

const app = new cdk.App();
new SlackEchoBotStack(app, 'SlackEchoBotStack');
