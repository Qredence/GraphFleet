export interface Document {
  id: string;
  title: string;
  content: string;
  metadata: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

export interface QueryRequest {
  query: string;
  filters?: Record<string, any>;
  options?: {
    maxResults?: number;
    minScore?: number;
    includeMetadata?: boolean;
  };
}

export interface QueryResult {
  id: string;
  score: number;
  content: string;
  metadata: Record<string, any>;
  document: Document;
}

export interface QueryResponse {
  results: QueryResult[];
  totalResults: number;
  executionTime: number;
  metadata: {
    query: string;
    filters?: Record<string, any>;
    options?: Record<string, any>;
  };
}

export interface IndexStats {
  totalDocuments: number;
  totalChunks: number;
  lastUpdated: string;
  indexSize: number;
}

export interface ErrorResponse {
  error: string;
  code: string;
  details?: Record<string, any>;
}
