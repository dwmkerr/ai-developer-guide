#!/usr/bin/env node

import { Command } from 'commander';
import { DeveloperGuideMcpServer } from './server/mcp-server.js';

const program = new Command();

// Get base URL from environment variable or use default
const getBaseUrl = (optionUrl?: string): string => {
  return optionUrl || process.env.AI_DEVELOPER_GUIDE_URL || 'https://dwmkerr.github.io/ai-developer-guide';
};

program
  .name('ai-developer-guide-mcp')
  .description('MCP server for the AI Developer Guide')
  .version('0.1.0');

program
  .command('start')
  .description('Start the MCP server')
  .option('--base-url <url>', 'Base URL for the API (default: env AI_DEVELOPER_GUIDE_URL or https://dwmkerr.github.io/ai-developer-guide)')
  .action(async (options) => {
    try {
      const baseUrl = getBaseUrl(options.baseUrl);
      console.error(`AI Developer Guide MCP Server starting with base URL: ${baseUrl}`);
      const server = new DeveloperGuideMcpServer(baseUrl);
      await server.start();
    } catch (error) {
      console.error('Failed to start server:', error);
      process.exit(1);
    }
  });

program
  .command('check')
  .description('Check API connectivity')
  .option('--base-url <url>', 'Base URL for the API (default: env AI_DEVELOPER_GUIDE_URL or https://dwmkerr.github.io/ai-developer-guide)')
  .action(async (options) => {
    try {
      const { ApiClient } = await import('./api/client.js');
      const baseUrl = getBaseUrl(options.baseUrl);
      const client = new ApiClient(baseUrl);
      
      console.log(`Testing API connectivity to: ${baseUrl}`);
      const index = await client.fetchApiIndex();
      console.log(`✓ Connected to API version ${index.version}`);
      console.log(`✓ API: ${index.name}`);
      
      const guides = await client.listAvailableGuides();
      console.log(`✓ Found ${guides.length} available guides`);
      
      console.log('API test successful!');
    } catch (error) {
      console.error('API test failed:', error);
      process.exit(1);
    }
  });

// Default action is to start the server
program.action(async () => {
  try {
    const baseUrl = getBaseUrl();
    console.error(`AI Developer Guide MCP Server starting with base URL: ${baseUrl}`);
    const server = new DeveloperGuideMcpServer(baseUrl);
    await server.start();
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
});

program.parse(); 