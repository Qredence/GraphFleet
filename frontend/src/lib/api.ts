import axios from 'axios';
import type {
  Document,
  QueryRequest,
  QueryResponse,
  IndexStats,
  ErrorResponse,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorResponse: ErrorResponse = {
      error: error.response?.data?.error || 'An unknown error occurred',
      code: error.response?.data?.code || 'UNKNOWN_ERROR',
      details: error.response?.data?.details,
    };
    return Promise.reject(errorResponse);
  }
);

export const GraphFleetAPI = {
  // Document operations
  documents: {
    list: async () => {
      const { data } = await api.get<Document[]>('/api/v1/documents');
      return data;
    },
    
    get: async (id: string) => {
      const { data } = await api.get<Document>(`/api/v1/documents/${id}`);
      return data;
    },
    
    upload: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      const { data } = await api.post<Document>('/api/v1/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return data;
    },
    
    delete: async (id: string) => {
      await api.delete(`/api/v1/documents/${id}`);
    },
  },

  // Query operations
  query: {
    search: async (request: QueryRequest) => {
      const { data } = await api.post<QueryResponse>('/api/v1/query', request);
      return data;
    },
    
    similar: async (documentId: string, options?: QueryRequest['options']) => {
      const { data } = await api.get<QueryResponse>(`/api/v1/documents/${documentId}/similar`, {
        params: options,
      });
      return data;
    },
  },

  // Index operations
  index: {
    stats: async () => {
      const { data } = await api.get<IndexStats>('/api/v1/index/stats');
      return data;
    },
    
    rebuild: async () => {
      const { data } = await api.post<{ status: string }>('/api/v1/index/rebuild');
      return data;
    },
  },
};

export default GraphFleetAPI;
