import { useCallback, useState, type ChangeEvent } from "react";

import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import { Box, Button, Chip, Stack } from "@mui/material";
import type { UploadStatus } from "../../../../types/file";
import { fileUploaderStyles } from "./FileUploader.styles";
import { useDropzone } from "react-dropzone";

const FileUploader = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<UploadStatus>("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const onDrop = useCallback((acceptedFiles: File[]) => {
    console.log(acceptedFiles);
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    const formData = new FormData();
    formData.append("file", file);
    //TODO: Attach the progress to the axios file stream uploader
  };

  return (
    <Box sx={fileUploaderStyles.container}>
      <Stack {...getRootProps()}>
        {/* <input type="file" onChange={handleFileChange} /> */}
        <input {...getInputProps()} />
        <Stack
          direction="row"
          spacing={1}
          alignItems="center"
          justifyContent="space-between"
        >
          {file ? (
            <Chip
              label={file.name}
              //   onDelete={clearFile}
              deleteIcon={<DeleteOutlineIcon />}
            />
          ) : (
            <Chip label="No file selected" />
          )}
          
          <Button
            onClick={handleFileUpload}
            variant="contained"
            disabled={status == "uploading" || !file}
          >
            {status == "uploading" ? "Uploading..." : "Upload"}
          </Button>
        </Stack>
      </Stack>
    </Box>
  );
};

export default FileUploader;
