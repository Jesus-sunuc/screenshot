import { useState } from 'react'
import axios, { AxiosError } from 'axios'
import { Container, Row, Col, Card, Button, Alert, Form, Spinner } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

type MessageType = 'success' | 'danger' | 'info'

interface ApiErrorResponse {
  detail: string
}

function App() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState<MessageType>('info')
  const [downloadUrl, setDownloadUrl] = useState('')

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files && files.length > 0) {
      setSelectedFiles(Array.from(files))
      setMessage('')
      setDownloadUrl('')
    }
  }

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setMessage('Please select at least one file')
      setMessageType('danger')
      return
    }

    setUploading(true)
    setMessage(`Processing ${selectedFiles.length} screenshot${selectedFiles.length > 1 ? 's' : ''}...`)
    setMessageType('info')

    const formData = new FormData()
    selectedFiles.forEach(file => {
      formData.append('files', file)
    })

    try {
      const response = await axios.post(`${API_URL}/process-screenshots`, formData)

      if (response.data.success) {
        setMessage(`Successfully processed ${response.data.processed_count} screenshot${response.data.processed_count > 1 ? 's' : ''}!`)
        setMessageType('success')
        setDownloadUrl(`${API_URL}${response.data.download_url}`)
      }
    } catch (error) {
      const axiosError = error as AxiosError<ApiErrorResponse>
      const errorMessage = axiosError.response?.data?.detail || axiosError.message || 'An unexpected error occurred'
      setMessage(`Error: ${errorMessage}`)
      setMessageType('danger')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="app-wrapper">
      <Container className="py-5">
        <Row className="justify-content-center">
          <Col lg={7} xl={6}>
            <div className="mb-5">
              <h1 className="display-6 fw-normal mb-2" style={{ color: '#e0e0e0' }}>
                Screenshots to Word
              </h1>
              <p className="mb-0" style={{ color: '#9a9a9a' }}>
                Upload multiple screenshots and convert them into one document
              </p>
            </div>

            <Card className="border-0 mb-4 dark-card">
              <Card.Body className="p-4">
                <Form>
                  <Form.Group className="mb-3">
                    <Form.Label className="mb-2 small" style={{ color: '#c0c0c0' }}>
                      Select Screenshots
                    </Form.Label>
                    <Form.Control
                      type="file"
                      accept="image/*"
                      multiple
                      onChange={handleFileSelect}
                      disabled={uploading}
                    />
                    {selectedFiles.length > 0 && (
                      <Form.Text className="d-block mt-2" style={{ color: '#8a8a8a' }}>
                        {selectedFiles.length} file{selectedFiles.length > 1 ? 's' : ''} selected
                        {' '}({(selectedFiles.reduce((sum, f) => sum + f.size, 0) / 1024).toFixed(2)} KB total)
                      </Form.Text>
                    )}
                  </Form.Group>

                  <div className="d-grid">
                    <Button
                      variant="light"
                      onClick={handleUpload}
                      disabled={selectedFiles.length === 0 || uploading}
                      className="btn-dark-theme"
                    >
                      {uploading ? (
                        <>
                          <Spinner
                            as="span"
                            animation="border"
                            size="sm"
                            className="me-2"
                          />
                          Processing...
                        </>
                      ) : (
                        'Convert to Word'
                      )}
                    </Button>
                  </div>
                </Form>

                {message && (
                  <Alert variant={messageType} className="mt-3 mb-0 dark-alert">
                    {message}
                  </Alert>
                )}

                {downloadUrl && (
                  <div className="d-grid mt-3">
                    <Button
                      variant="outline-light"
                      onClick={() => window.open(downloadUrl, '_blank')}
                      className="btn-outline-dark-theme"
                    >
                      Download Document
                    </Button>
                  </div>
                )}
              </Card.Body>
            </Card>

            <div className="text-center">
              <p className="small mb-0" style={{ color: '#7a7a7a' }}>
                Powered by Tesseract OCR
              </p>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  )
}

export default App
