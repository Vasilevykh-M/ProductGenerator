import React, { useState, useRef } from "react";
import { Container, Form, Button, Row, Col, Spinner } from "react-bootstrap";
import { useDropzone } from "react-dropzone";
import './App.css'; // Подключаем стили


function ImageGenerator() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [preview, setPreview] = useState(null);
  const [selectedBg, setSelectedBg] = useState(null);
  const [position, setPosition] = useState(0.5);  // Значение по умолчанию для положения объекта
  const [bgSize, setBgSize] = useState(0.5);  // Значение по умолчанию для размера фона
  const [result, setResult] = useState(null);
  const [loadingResult, setLoadingResult] = useState(false);
  const [loadingBackgrounds, setLoadingBackgrounds] = useState(false);
  const resultRef = useRef(null);

  const onDrop = (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    setFile(uploadedFile);
    setFileName(uploadedFile.name);
    setPreview(URL.createObjectURL(uploadedFile));
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  const handleBackgroundChange = (e) => {
    setSelectedBg(e.target.value);
  };

  const handleGenerate = async() => {
    setLoadingResult(true);

    
    const formData =  new FormData();
    formData.append('img_file', file);
    formData.append('y_pos', position);
    formData.append('scale', bgSize);
    formData.append('prompt', selectedBg);

    const response = await fetch('http://localhost:80/generate_background', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    setTimeout(() => {
      const finalImage = data.img;
      const description = `Position: ${position}, Background Size: ${bgSize}`;
      setResult({ image: finalImage, description: description, objectDescription: data.description});
      setLoadingResult(false);

      if (resultRef.current) {
        resultRef.current.scrollIntoView({ behavior: "smooth" });
      }
    }, 5);
  };

  const handleFetchBackgrounds = async () => {
    setLoadingBackgrounds(true);

    const formData = new FormData();
    formData.append('img_file', file);

    const response = await fetch('http://localhost:80/get_background_result', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();

    setTimeout(() => {

      setSelectedBg(data.prompt);
      setPosition(data.y_pos);
      setBgSize(data.scale);
      
      setLoadingBackgrounds(false);
    }, 5);
  };

  return (
    <Container className="mt-5 container">
      <h2>Upload Image with Background and Position Choice</h2>

      {/* Загрузка файла */}
      <div {...getRootProps()} className="border p-3 mb-3 text-center">
        <input {...getInputProps()} />
        <p>Drag 'n' drop a file here, or click to select one</p>
        {fileName && <p><strong>Uploaded file:</strong> {fileName}</p>} {/* Имя файла */}
      </div>

      {/* Превью изображения */}
      {preview && (
        <div className="mb-3 text-center">
          <h5>Uploaded Image Preview:</h5>
          <img src={preview} alt="Preview" className="result-image" /> {/* Измененный класс */}
        </div>
      )}

      {/* Кнопка для получения фонов */}
      {file && (
        <div className="mb-3 text-center">
          <Button className="small-btn" onClick={handleFetchBackgrounds} disabled={loadingBackgrounds}>
            {loadingBackgrounds ? (
              <>
                <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                Fetching Backgrounds...
              </>
            ) : (
              "Fetch Possible Backgrounds"
            )}
          </Button>
        </div>
      )}

      {/* Выбор фона и бегунки */}
      <Row className="mb-3">

        <Col xs={12} md={6}>
          <Form.Group>
            <Form.Label>Enter Custom Background Description:</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter background description"
              value={selectedBg}
              onChange={handleBackgroundChange}
            />
          </Form.Group>
        </Col>

        {/* Группировка бегунков */}
        <Col xs={12} className="mt-3">
          <h5 className="text-center">Adjust Background Size and Position</h5>
        </Col>

        <Col xs={12} className="d-flex align-items-center justify-content-between mt-3">
          <Form.Label className="me-2">Меньше</Form.Label>
          <Form.Range
            min={0}
            max={1}
            step={0.1}
            value={bgSize}
            onChange={(e) => setBgSize(e.target.value)}
            className="flex-grow-1"
          />
          <Form.Label className="ms-2">Больше</Form.Label>
        </Col>

        <Col xs={12} className="d-flex align-items-center justify-content-between mt-3">
          <Form.Label className="me-2">Ниже</Form.Label>
          <Form.Range
            min={0}
            max={1}
            step={0.1}
            value={position}
            onChange={(e) => setPosition(e.target.value)}
            className="flex-grow-1"
          />
          <Form.Label className="ms-2">Выше</Form.Label>
        </Col>
      </Row>

      {/* Кнопка генерации результата */}
      <div className="text-center">
        <Button variant="primary" className="small-btn" onClick={handleGenerate} disabled={!file || loadingResult}>
          {loadingResult ? (
            <>
              <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
              Generating...
            </>
          ) : (
            "Generate Result"
          )}
        </Button>
      </div>

      {/* Результат */}
      {result && (
        <div ref={resultRef} className="mt-5 text-center">
          <h5>Generated Image:</h5>
          <img src={`data:image/png;base64,${result.image}`} alt="Result" style={{ maxWidth: "100%", height: "auto" }} />
          <p><strong>Description:</strong> {result.description}</p>
          <p><strong>Object Description:</strong> {result.objectDescription}</p>
        </div>
      )}
    </Container>
  );
}

export default ImageGenerator;
