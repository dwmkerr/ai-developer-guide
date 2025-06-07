export interface GuideContent {
  title: string;
  content: string;
  sections?: Array<{
    title: string;
    content: string;
  }>;
}

export interface ApiIndex {
  name: string;
  description: string;
  version: string;
  source: string;
  lastUpdated: string;
  endpoints: {
    main_guide: {
      path: string;
      description: string;
    };
    language_guides?: Record<string, { path: string; description: string }>;
    pattern_guides?: Record<string, { path: string; description: string }>;
    platform_guides?: Record<string, { path: string; description: string }>;
    other_guides?: Record<string, { path: string; description: string }>;
  };
}

export interface AvailableGuide {
  category: string;
  topic: string;
  description: string;
  path: string;
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl = 'https://dwmkerr.github.io/ai-developer-guide') {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
  }

  async fetchApiIndex(): Promise<ApiIndex> {
    const response = await fetch(`${this.baseUrl}/api.json`);
    if (!response.ok) {
      throw new Error(`Failed to fetch API index: ${response.statusText}`);
    }
    return response.json();
  }

  async fetchMainGuide(): Promise<GuideContent> {
    const response = await fetch(`${this.baseUrl}/api/guide.json`);
    if (!response.ok) {
      throw new Error(`Failed to fetch main guide: ${response.statusText}`);
    }
    return response.json();
  }

  async fetchGuide(category: string, topic: string): Promise<GuideContent> {
    const response = await fetch(`${this.baseUrl}/api/guides/${category}/${topic}.json`);
    if (!response.ok) {
      throw new Error(`Failed to fetch guide ${category}/${topic}: ${response.statusText}`);
    }
    return response.json();
  }

  async listAvailableGuides(): Promise<AvailableGuide[]> {
    try {
      const index = await this.fetchApiIndex();
      const guides: AvailableGuide[] = [];

      // Parse language guides
      if (index.endpoints.language_guides) {
        for (const [topic, info] of Object.entries(index.endpoints.language_guides)) {
          guides.push({
            category: 'languages',
            topic,
            description: info.description,
            path: info.path,
          });
        }
      }

      // Parse pattern guides
      if (index.endpoints.pattern_guides) {
        for (const [topic, info] of Object.entries(index.endpoints.pattern_guides)) {
          guides.push({
            category: 'patterns',
            topic,
            description: info.description,
            path: info.path,
          });
        }
      }

      // Parse platform guides
      if (index.endpoints.platform_guides) {
        for (const [topic, info] of Object.entries(index.endpoints.platform_guides)) {
          guides.push({
            category: 'platforms',
            topic,
            description: info.description,
            path: info.path,
          });
        }
      }

      // Parse other guides
      if (index.endpoints.other_guides) {
        for (const [topic, info] of Object.entries(index.endpoints.other_guides)) {
          guides.push({
            category: 'others',
            topic,
            description: info.description,
            path: info.path,
          });
        }
      }

      return guides;
    } catch (error) {
      console.error('Failed to list guides:', error);
      return [];
    }
  }
} 