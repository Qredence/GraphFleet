'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { useMutation } from '@tanstack/react-query'
import GraphFleetAPI from '@/lib/api'
import type { QueryResponse } from '@/types'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<QueryResponse | null>(null)

  const searchMutation = useMutation({
    mutationFn: (query: string) =>
      GraphFleetAPI.query.search({
        query,
        options: {
          maxResults: 10,
          minScore: 0.5,
          includeMetadata: true,
        },
      }),
    onSuccess: (data) => {
      setResults(data)
    },
  })

  const handleSearch = () => {
    if (!query.trim()) return
    searchMutation.mutate(query)
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Search</h1>
        <p className="text-muted-foreground mt-2">
          Search through your documents using natural language
        </p>
      </div>

      <div className="flex gap-4">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your search query..."
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <Button onClick={handleSearch} disabled={!query.trim()}>
          Search
        </Button>
      </div>

      {searchMutation.isPending && <div>Searching...</div>}

      {results && (
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Found {results.totalResults} results in{' '}
            {results.executionTime.toFixed(2)}ms
          </p>

          {results.results.map((result) => (
            <Card key={result.id}>
              <CardContent className="p-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <h3 className="font-semibold">
                      {result.document.title}
                    </h3>
                    <span className="text-sm text-muted-foreground">
                      Score: {result.score.toFixed(2)}
                    </span>
                  </div>
                  <p className="text-sm">{result.content}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
