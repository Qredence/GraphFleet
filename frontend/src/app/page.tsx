import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight">
          Welcome to GraphFleet
        </h1>
        <p className="mt-4 text-lg text-muted-foreground">
          Powerful document search and analysis powered by GraphRAG
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Upload Documents</CardTitle>
            <CardDescription>
              Add your documents to the knowledge base
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild>
              <a href="/documents">Get Started</a>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Search & Query</CardTitle>
            <CardDescription>
              Search through your documents with natural language
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild>
              <a href="/search">Start Searching</a>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Analyze</CardTitle>
            <CardDescription>
              Get insights and analyze document relationships
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild>
              <a href="/analyze">View Analytics</a>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
