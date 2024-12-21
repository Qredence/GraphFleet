'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { useQuery } from '@tanstack/react-query'
import GraphFleetAPI from '@/lib/api'
import { formatDate, formatFileSize } from '@/lib/utils'

export default function DocumentsPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  
  const { data: documents, isLoading } = useQuery({
    queryKey: ['documents'],
    queryFn: () => GraphFleetAPI.documents.list(),
  })

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return
    try {
      await GraphFleetAPI.documents.upload(selectedFile)
      setSelectedFile(null)
    } catch (error) {
      console.error('Error uploading file:', error)
    }
  }

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Documents</h1>
        <p className="text-muted-foreground mt-2">
          Upload and manage your documents
        </p>
      </div>

      <div className="flex gap-4">
        <Input
          type="file"
          onChange={handleFileChange}
          accept=".txt,.md,.pdf,.doc,.docx"
        />
        <Button onClick={handleUpload} disabled={!selectedFile}>
          Upload
        </Button>
      </div>

      <div className="grid gap-4">
        {documents?.map((doc) => (
          <Card key={doc.id}>
            <CardContent className="p-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold">{doc.title}</h3>
                  <p className="text-sm text-muted-foreground">
                    Added {formatDate(doc.createdAt)}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => GraphFleetAPI.documents.delete(doc.id)}
                >
                  Delete
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
