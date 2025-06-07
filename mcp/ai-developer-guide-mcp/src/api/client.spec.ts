import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { ApiClient } from './client.js';

describe('ApiClient', () => {
  let apiClient: ApiClient;
  const mockFetch = fetch as jest.MockedFunction<typeof fetch>;

  beforeEach(() => {
    apiClient = new ApiClient('http://test.example.com');
    mockFetch.mockClear();
  });

  describe('constructor', () => {
    it('should create instance with default base URL', () => {
      const client = new ApiClient();
      expect(client).toBeInstanceOf(ApiClient);
    });

    it('should create instance with custom base URL', () => {
      const client = new ApiClient('http://custom.example.com');
      expect(client).toBeInstanceOf(ApiClient);
    });
  });

  describe('fetchApiIndex', () => {
    it('should fetch API index successfully', async () => {
      const mockResponse = {
        name: 'AI Developer Guide API',
        description: 'API for AI Developer Guide',
        version: '1.0.0',
        source: 'https://github.com/dwmkerr/ai-developer-guide',
        lastUpdated: '2024-01-01',
        endpoints: {
          main_guide: {
            path: '/api/guide.json',
            description: 'Main guide content',
          },
        },
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      } as Response);

      const result = await apiClient.fetchApiIndex();

      expect(mockFetch).toHaveBeenCalledWith('http://test.example.com/api.json');
      expect(result).toEqual(mockResponse);
    });

    it('should throw error when fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        statusText: 'Not Found',
      } as Response);

      await expect(apiClient.fetchApiIndex()).rejects.toThrow('Failed to fetch API index: Not Found');
    });
  });

  describe('fetchMainGuide', () => {
    it('should fetch main guide successfully', async () => {
      const mockResponse = {
        title: 'AI Developer Guide',
        content: 'This is the main guide content',
        sections: [],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      } as Response);

      const result = await apiClient.fetchMainGuide();

      expect(mockFetch).toHaveBeenCalledWith('http://test.example.com/api/guide.json');
      expect(result).toEqual(mockResponse);
    });

    it('should throw error when fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        statusText: 'Not Found',
      } as Response);

      await expect(apiClient.fetchMainGuide()).rejects.toThrow('Failed to fetch main guide: Not Found');
    });
  });

  describe('fetchGuide', () => {
    it('should fetch guide successfully', async () => {
      const mockResponse = {
        title: 'Python Guide',
        content: 'Python guide content',
        sections: [],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      } as Response);

      const result = await apiClient.fetchGuide('languages', 'python');

      expect(mockFetch).toHaveBeenCalledWith('http://test.example.com/api/guides/languages/python.json');
      expect(result).toEqual(mockResponse);
    });

    it('should throw error when fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        statusText: 'Internal Server Error',
      } as Response);

      await expect(apiClient.fetchGuide('languages', 'python')).rejects.toThrow('Failed to fetch guide languages/python: Internal Server Error');
    });
  });

  describe('listAvailableGuides', () => {
    it('should list available guides successfully', async () => {
      const mockApiIndex = {
        name: 'AI Developer Guide API',
        description: 'API for AI Developer Guide',
        version: '1.0.0',
        source: 'https://github.com/dwmkerr/ai-developer-guide',
        lastUpdated: '2024-01-01',
        endpoints: {
          main_guide: {
            path: '/api/guide.json',
            description: 'Main guide content',
          },
          language_guides: {
            python: { path: '/api/guides/languages/python.json', description: 'Python guide' },
          },
          platform_guides: {
            postgresql: { path: '/api/guides/platforms/postgresql.json', description: 'PostgreSQL guide' },
          },
        },
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockApiIndex),
      } as Response);

      const result = await apiClient.listAvailableGuides();

      expect(mockFetch).toHaveBeenCalledWith('http://test.example.com/api.json');
      expect(result).toEqual([
        { category: 'languages', topic: 'python', description: 'Python guide', path: '/api/guides/languages/python.json' },
        { category: 'platforms', topic: 'postgresql', description: 'PostgreSQL guide', path: '/api/guides/platforms/postgresql.json' },
      ]);
    });

    it('should return empty array when API index fails', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
      
      mockFetch.mockResolvedValueOnce({
        ok: false,
        statusText: 'Forbidden',
      } as Response);

      const result = await apiClient.listAvailableGuides();

      expect(result).toEqual([]);
      expect(consoleSpy).toHaveBeenCalledWith('Failed to list guides:', expect.any(Error));
      
      consoleSpy.mockRestore();
    });
  });
}); 