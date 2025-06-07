import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  CallToolRequest,
} from '@modelcontextprotocol/sdk/types.js';
import { ApiClient } from '../api/client.js';

export class DeveloperGuideMcpServer {
  private server: Server;
  private apiClient: ApiClient;

  constructor(baseUrl?: string) {
    this.log(`Initializing AI Developer Guide MCP Server with baseUrl: ${baseUrl || 'default'}`);
    
    this.server = new Server(
      {
        name: 'ai-developer-guide-mcp',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.apiClient = new ApiClient(baseUrl);
    this.setupToolHandlers();
    this.log('Initialization complete');
  }

  private log(message: string) {
    const timestamp = new Date().toISOString();
    console.error(`${timestamp} [MCP Server] ${message}`);
  }

  private setupToolHandlers() {
    this.log('Setting up tool handlers...');
    
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      this.log('ListTools request received');
      const tools = {
        tools: [
          {
            name: 'fetch_main_guide',
            description: 'Fetch the main AI Developer Guide content with core development principles and practices',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
          {
            name: 'fetch_guide',
            description: 'Fetch a specific guide (e.g., Python, Shell Scripts, Make, PostgreSQL)',
            inputSchema: {
              type: 'object',
              properties: {
                category: {
                  type: 'string',
                  description: 'Category of the guide (languages, patterns, platforms, others)',
                  enum: ['languages', 'patterns', 'platforms', 'others'],
                },
                topic: {
                  type: 'string',
                  description: 'Specific topic (e.g., python, shell-scripts, make, postgresql, cicd)',
                },
              },
              required: ['category', 'topic'],
            },
          },
          {
            name: 'list_available_guides',
            description: 'List all available guides with their categories and descriptions',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
        ],
      };
      this.log(`Returning ${tools.tools.length} available tools`);
      return tools;
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request: CallToolRequest) => {
      const { name, arguments: args } = request.params;
      this.log(`Tool called: "${name}" with args: ${JSON.stringify(args)}`);

      try {
        switch (name) {
          case 'fetch_main_guide': {
            this.log('Fetching main guide...');
            const startTime = Date.now();
            const guide = await this.apiClient.fetchMainGuide();
            const duration = Date.now() - startTime;
            this.log(`Main guide fetched successfully in ${duration}ms (${guide.content.length} chars)`);
            
            return {
              content: [
                {
                  type: 'text',
                  text: `# ${guide.title}\n\n${guide.content}${
                    guide.sections
                      ? '\n\n' + guide.sections.map(s => `## ${s.title}\n\n${s.content}`).join('\n\n')
                      : ''
                  }`,
                },
              ],
            };
          }

          case 'fetch_guide': {
            const { category, topic } = args as { category: string; topic: string };
            this.log(`Fetching guide: category="${category}", topic="${topic}"`);
            const startTime = Date.now();
            const guide = await this.apiClient.fetchGuide(category, topic);
            const duration = Date.now() - startTime;
            this.log(`Guide fetched successfully in ${duration}ms (${guide.content.length} chars)`);
            
            return {
              content: [
                {
                  type: 'text',
                  text: `# ${guide.title}\n\n${guide.content}${
                    guide.sections
                      ? '\n\n' + guide.sections.map(s => `## ${s.title}\n\n${s.content}`).join('\n\n')
                      : ''
                  }`,
                },
              ],
            };
          }

          case 'list_available_guides': {
            this.log('Listing available guides...');
            const startTime = Date.now();
            const guides = await this.apiClient.listAvailableGuides();
            const duration = Date.now() - startTime;
            this.log(`Available guides listed successfully in ${duration}ms (${guides.length} guides found)`);
            
            const guidesByCategory = guides.reduce((acc, guide) => {
              if (!acc[guide.category]) {
                acc[guide.category] = [];
              }
              acc[guide.category].push(guide);
              return acc;
            }, {} as Record<string, typeof guides>);

            let text = 'Available Guides:\n\n';
            for (const [category, categoryGuides] of Object.entries(guidesByCategory)) {
              text += `**${category.charAt(0).toUpperCase() + category.slice(1)}:**\n`;
              for (const guide of categoryGuides) {
                text += `- ${guide.topic}: ${guide.description}\n`;
              }
              text += '\n';
            }

            return {
              content: [
                {
                  type: 'text',
                  text,
                },
              ],
            };
          }

          default:
            this.log(`Unknown tool requested: "${name}"`);
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        this.log(`Tool execution failed for "${name}": ${errorMessage}`);
        throw new Error(`Tool execution failed: ${errorMessage}`);
      }
    });
    
    this.log('Tool handlers setup complete');
  }

  async start() {
    const transport = new StdioServerTransport();
    this.log('AI Developer Guide MCP Server starting on stdio transport...');
    await this.server.connect(transport);
    this.log('Server connected and ready for requests');
  }

  getServer() {
    return this.server;
  }
} 